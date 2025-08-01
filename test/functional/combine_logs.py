#!/usr/bin/env python3
"""Combine logs from multiple bitcoin nodes as well as the test_framework log.

This streams the combined log output to stdout. Use combine_logs.py > outputfile
to write to an outputfile.

If no argument is provided, the most recent test directory will be used."""

import argparse
from collections import defaultdict, namedtuple
import heapq
import itertools
import os
import re
import sys
import tempfile

# N.B.: don't import any local modules here - this script must remain executable
# without the parent module installed.

# Should match same symbol in `test_framework.test_framework`.
TMPDIR_PREFIX = "krypton_func_test_"

# Matches on the date format at the start of the log event
TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{6})?Z")

LogEvent = namedtuple('LogEvent', ['timestamp', 'source', 'event'])

def main():
    """Main function. Parses args, reads the log files and renders them as text or html."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        'testdir', nargs='?', default='',
        help=('temporary test directory to combine logs from. '
              'Defaults to the most recent'))
    parser.add_argument('-c', '--color', dest='color', action='store_true', help='outputs the combined log with events colored by source (requires posix terminal colors. Use less -r for viewing)')
    parser.add_argument('--html', dest='html', action='store_true', help='outputs the combined log as html. Requires jinja2. pip install jinja2')
    args = parser.parse_args()

    if args.html and args.color:
        print("Only one out of --color or --html should be specified")
        sys.exit(1)

    testdir = args.testdir or find_latest_test_dir()

    if not testdir:
        print("No test directories found")
        sys.exit(1)

    if not args.testdir:
        print("Opening latest test directory: {}".format(testdir), file=sys.stderr)

    log_events = read_logs(testdir)

    print_logs(log_events, color=args.color, html=args.html)

def read_logs(tmp_dir):
    """Reads log files.

    Delegates to generator function get_log_events() to provide individual log events
    for each of the input log files."""

    files = [("test", "%s/test_framework.log" % tmp_dir)]
    for i in itertools.count():
        logfile = "{}/node{}/regtest/debug.log".format(tmp_dir, i)
        if not os.path.isfile(logfile):
            break
        files.append(("node%d" % i, logfile))

    return heapq.merge(*[get_log_events(source, f) for source, f in files])


def find_latest_test_dir():
    """Returns the latest tmpfile test directory prefix."""
    tmpdir = tempfile.gettempdir()

    def join_tmp(basename):
        return os.path.join(tmpdir, basename)

    def is_valid_test_tmpdir(basename):
        fullpath = join_tmp(basename)
        return (
            os.path.isdir(fullpath)
            and basename.startswith(TMPDIR_PREFIX)
            and os.access(fullpath, os.R_OK)
        )

    testdir_paths = [
        join_tmp(name) for name in os.listdir(tmpdir) if is_valid_test_tmpdir(name)
    ]

    return max(testdir_paths, key=os.path.getmtime) if testdir_paths else None


def get_log_events(source, logfile):
    """Generator function that returns individual log events.

    Log events may be split over multiple lines. We use the timestamp
    regex match as the marker for a new log event."""
    try:
        with open(logfile, 'r', encoding='utf-8') as infile:
            event = ''
            timestamp = ''
            for line in infile:
                # skip blank lines
                if line == '\n':
                    continue
                # if this line has a timestamp, it's the start of a new log event.
                time_match = TIMESTAMP_PATTERN.match(line)
                if time_match:
                    if event:
                        yield LogEvent(timestamp=timestamp, source=source, event=event.rstrip())
                    timestamp = time_match.group()
                    if time_match.group(1) is None:
                        # timestamp does not have microseconds. Add zeroes.
                        timestamp_micro = timestamp.replace("Z", ".000000Z")
                        line = line.replace(timestamp, timestamp_micro)
                        timestamp = timestamp_micro
                    event = line
                # if it doesn't have a timestamp, it's a continuation line of the previous log.
                else:
                    # Add the line. Prefix with space equivalent to the source + timestamp so log lines are aligned
                    event += "                                   " + line
            # Flush the final event
            yield LogEvent(timestamp=timestamp, source=source, event=event.rstrip())
    except FileNotFoundError:
        print("File %s could not be opened. Continuing without it." % logfile, file=sys.stderr)

def print_logs(log_events, color=False, html=False):
    """Renders the iterator of log events into text or html."""
    if not html:
        colors = defaultdict(lambda: '')
        if color:
            colors["test"] = "\033[0;36m"   # CYAN
            colors["node0"] = "\033[0;34m"  # BLUE
            colors["node1"] = "\033[0;32m"  # GREEN
            colors["node2"] = "\033[0;31m"  # RED
            colors["node3"] = "\033[0;33m"  # YELLOW
            colors["reset"] = "\033[0m"     # Reset font color

        for event in log_events:
            lines = event.event.splitlines()
            print("{0} {1: <5} {2} {3}".format(colors[event.source.rstrip()], event.source, lines[0], colors["reset"]))
            if len(lines) > 1:
                for line in lines[1:]:
                    print("{0}{1}{2}".format(colors[event.source.rstrip()], line, colors["reset"]))

    else:
        try:
            import jinja2
        except ImportError:
            print("jinja2 not found. Try `pip install jinja2`")
            sys.exit(1)
        print(jinja2.Environment(loader=jinja2.FileSystemLoader('./'))
                    .get_template('combined_log_template.html')
                    .render(title="Combined Logs from testcase", log_events=[event._asdict() for event in log_events]))

if __name__ == '__main__':
    main()
