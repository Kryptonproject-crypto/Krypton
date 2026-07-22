# Krypton (KYP)

Krypton is an open-source cryptocurrency based on **Litecoin**.
Launched on **July 24, 2025**, Krypton's goal is to be **fast, lightweight, and accessible to everyone**.
No premine, no VC funding — just a **clean, community-driven blockchain**.

- 🌐 **Official website:** [krypton-explorer.org](https://krypton-explorer.org)
- 🔎 **Block Explorer:** [explorer.krypton-explorer.org](https://explorer.krypton-explorer.org)
- 💬 **Discord:** [join the community](https://discord.gg/g8c64BccQZ)
- 🐦 **X:** [@Krypton_KYP](https://x.com/Krypton_KYP)

---

## 📥 Download

Pre-built wallets for **Windows, macOS and Linux** are available on the
[Releases page](https://github.com/Kryptonproject-crypto/Krypton/releases).

| Platform | File | Notes |
|---|---|---|
| **Windows** | `krypton-<version>-win64-setup.exe` | Installer wizard (recommended) |
| **Windows** | `krypton-<version>-win64.zip` | Portable, no installation |
| **macOS (Apple Silicon)** | `krypton-<version>-arm64-apple-darwin-setup.dmg` | M1/M2/M3/M4 |
| **macOS (Intel)** | `krypton-<version>-x86_64-apple-darwin-setup.dmg` | Intel Macs |
| **Linux** | `krypton-<version>-x86_64-linux-gnu.tar.gz` | Needs Qt 5 runtime for the GUI |

Each package contains:

| Binary | Purpose |
|---|---|
| `krypton-qt` | Graphical wallet + node (what most users want) |
| `kryptond` | Headless node daemon (servers, mining, hosting) |
| `krypton-cli` | Command-line control of a running node/wallet |
| `krypton-tx` | Low-level transaction utility |

On Linux, the GUI needs the Qt 5 runtime:

```
sudo apt install libqt5widgets5 libqt5network5 libqt5dbus5
```

---

## 🆕 What's new in v1.6

Version 1.6 focuses on **security, chain stability and network responsiveness**.

### Faster difficulty adjustment — activates at block 527040 ⚠️

The LWMA retarget window narrows from **120 to 60 blocks** (about 1 hour instead of 2).
Difficulty then tracks hashrate swings roughly twice as fast, which shortens the periods
of very slow blocks after a large miner leaves the network.

> **This is a hard fork.** Every node and mining pool must run v1.6 or later
> **before block 527040**, otherwise it will be left behind on a dead chain.

### Deep-reorg (51%) protection — active immediately

Nodes now refuse any competing chain that would reorganize **more than 200 blocks
(~3h20)** below their current tip, even if that chain carries more proof-of-work.
This protects already-confirmed history against a hidden-chain / 51% style attack.

Design points:

- The check runs at **header acceptance**, so an over-deep chain is refused before its
  blocks are ever downloaded, and it can never stall the node's own chain.
- It is **disabled during initial block download**, so a node syncing from scratch
  is never affected.
- A peer on a legitimate old fork is **refused, not banned**.
- Tunable per node with `-maxreorgdepth=<n>` (`0` disables it entirely).

### P2P timings adapted to 60-second blocks

Stale-tip detection, extra-peer eviction and chain-sync timeouts were inherited from
Bitcoin and assumed **10-minute** blocks. They are now derived from Krypton's real
block interval, so the node reacts about **10× faster** to peers that stall or fall
behind.

### Consensus hardening

The block subsidy is now computed from an exact integer constant instead of a
floating-point literal. The **reward value is unchanged** (14.26940639 KYP), but the
result is now guaranteed bit-identical across every platform and compiler — floating
point in consensus code is a classic source of accidental chain splits.

### Wallet, fees and build

- The **graphical wallet ships on all three platforms**, including a Windows installer
  wizard and macOS `.dmg` bundles for both Intel and Apple Silicon.
- Wallet, transaction and fee logic were fully reviewed (relay fee, dust threshold,
  default wallet fee, `-maxtxfee` safety cap, fee estimator): all values are sound for
  Krypton's 60-second chain, so **no wallet behaviour was changed**.
- The codebase now builds cleanly with **modern toolchains** (GCC 13, current
  Xcode/clang, current mingw-w64) and on **Apple Silicon**.

---

## ⚙️ Technical Specifications

| Parameter | Value |
|---|---|
| **Name** | Krypton |
| **Ticker** | KYP |
| **Algorithm** | Scrypt (Proof-of-Work) |
| **Block Time** | 60 seconds |
| **Initial Block Reward** | 14.26940639 KYP |
| **Reward Halving** | 50% every 525,600 blocks (~1 year) |
| **Max Supply** | 14,999,999.9078 KYP (~15,000,000) |
| **Distribution Duration** | ~31 years (reward reaches 0 at block 16,293,600) |
| **Difficulty Algorithm** | LWMA — 120-block window, **60-block window from block 527040** |
| **Max Reorg Depth** | 200 blocks (~3h20), configurable via `-maxreorgdepth` |
| **Address Prefix** | `K...` (legacy), `A...` (P2SH), `kyp1...` (bech32) |
| **Premine** | None |
| **P2P Port** | 8369 (testnet: 18369) |
| **RPC Port** | 8370 (testnet: 18370) |

---

### Emission schedule

The reward halves every 525,600 blocks (~1 year), so most coins are created early:

| Time | Reward per block | Total mined |
|---|---|---|
| Year 1 | 14.26940639 KYP | 7,500,000 (50%) |
| Year 2 | 7.13470319 KYP | 11,250,000 (75%) |
| Year 3 | 3.56735159 KYP | 13,125,000 (87.5%) |
| Year 7 | 0.11147973 KYP | 14,941,406 (99.6%) |
| Year ~31 | 0 | 14,999,999.9078 (100%) |

The slightly-under-15,000,000 final figure is normal: each halving is an integer
right-shift, so a fraction of a satoshi is truncated every era.

---

## 💳 Using the wallet

### Graphical wallet

Launch `krypton-qt`. On first start it creates a wallet and begins syncing the
blockchain. Use the **Receive** tab to generate an address and the **Send** tab to
transfer KYP.

> 🔐 **Back up your wallet.** Use *File → Backup Wallet* and keep the copy somewhere
> safe and offline. If you lose `wallet.dat` and have no backup, your coins are gone —
> there is no password reset on a blockchain.

### Command line

Start the node, then talk to it with `krypton-cli`:

```
./kryptond -daemon
./krypton-cli getblockchaininfo      # sync status
./krypton-cli getnewaddress          # new receiving address
./krypton-cli getbalance             # current balance
./krypton-cli sendtoaddress <address> <amount>
./krypton-cli backupwallet /path/to/wallet-backup.dat
./krypton-cli stop                   # shut the node down cleanly
```

Full command list: `./krypton-cli help`

---

## 🛠️ Build from source

Building is only needed if you want to compile yourself — most users should simply
download a release.

### Requirements (Ubuntu 22.04 / 24.04, Debian)

```
sudo apt update && sudo apt install -y \
    build-essential libtool autotools-dev automake pkg-config \
    libssl-dev libevent-dev bsdmainutils libboost-all-dev \
    libminiupnpc-dev libzmq3-dev libprotobuf-dev protobuf-compiler \
    qtbase5-dev qttools5-dev qttools5-dev-tools libqrencode-dev git curl
```

### Install Berkeley DB 4.8

Krypton uses **Berkeley DB 4.8** for wallet compatibility. Distribution packages ship
5.x, which produces wallet files that are not portable to other Krypton builds — so
build 4.8 from source:

```
# download.oracle.com is often unreliable for scripted downloads; a mirror is used as fallback
curl -fL -O http://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz \
  || curl -fL -O https://bitcoincore.org/depends-sources/db-4.8.30.NC.tar.gz
tar -xzvf db-4.8.30.NC.tar.gz
cd db-4.8.30.NC/build_unix
../dist/configure --enable-cxx --disable-shared --with-pic --prefix=/usr/local
make -j$(nproc)
sudo make install
```

Set environment variables:

```
export BDB_PREFIX="/usr/local"
export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
```

> On very recent systems, Berkeley DB 4.8 (released 2010) may need two small fixes
> before it compiles: renaming its `__atomic_compare_exchange` / `atomic_init` helpers,
> which collide with modern compiler built-ins, and replacing its bundled
> `config.guess` / `config.sub`. The project's `depends/packages/bdb.mk` applies both
> automatically.

### Compile Krypton

```
git clone https://github.com/Kryptonproject-crypto/Krypton.git
cd Krypton
./autogen.sh
./configure LDFLAGS="-L/usr/local/lib" CPPFLAGS="-I/usr/local/include"
make -j$(nproc)
```

Useful `configure` flags:

| Flag | Effect |
|---|---|
| `--without-gui` | Node and CLI only, skip the Qt wallet |
| `--disable-wallet` | No wallet at all (Berkeley DB not required) |
| `--disable-tests --disable-bench` | Faster build |

Binaries land in `src/` (`kryptond`, `krypton-cli`, `krypton-tx`) and `src/qt/krypton-qt`.

### Cross-compile for Windows / macOS

The `depends/` system builds every dependency (including Berkeley DB 4.8 and a static
Qt) reproducibly:

```
cd depends && make HOST=x86_64-w64-mingw32 -j$(nproc)
cd .. && ./autogen.sh
CONFIG_SITE=$PWD/depends/x86_64-w64-mingw32/share/config.site ./configure --prefix=/
make -j$(nproc)
make deploy          # produces the Windows setup.exe installer
```

Official releases are built automatically by GitHub Actions
(`.github/workflows/main.yml`) for Windows, Linux, macOS Intel and macOS Apple Silicon.

---

## 🚀 Running Krypton

Start the daemon:

```
./src/kryptond -daemon
```

Check synchronization:

```
./src/krypton-cli getblockchaininfo
```

### Test networks

Two isolated networks are available for development and testing — coins there have
**no value**:

```
./src/kryptond -testnet -daemon     # public test network
./src/kryptond -regtest -daemon     # private local network, instant mining
```

Regtest is ideal for experimenting: you mine blocks on demand with
`generatetoaddress`, and difficulty stays at minimum.

### Useful node options

| Option | Description |
|---|---|
| `-daemon` | Run in the background |
| `-datadir=<dir>` | Use a custom data directory |
| `-maxreorgdepth=<n>` | Override the deep-reorg limit (0 = disabled) |
| `-addnode=<ip>` | Connect to a specific peer |
| `-help` | Full option list |

---

## 🌍 Community

Krypton is open to everyone. You are welcome to:

- 💡 Propose ideas
- 👩‍💻 Contribute to the code
- 💳 Launch new wallets
- 🖧 Run nodes
- ⛏️ Mine and help secure the chain

Join us on [GitHub](https://github.com/Kryptonproject-crypto/Krypton),
[Discord](https://discord.gg/g8c64BccQZ) or [X](https://x.com/Krypton_KYP) and help
grow Krypton!

---

## 📜 License

Krypton is an **open-source project** published under the
[MIT License](https://opensource.org/licenses/MIT).

---

## 🙏 Acknowledgements

Thanks to all who support Krypton and believe in a **simple, clean, and
community-first blockchain**.
