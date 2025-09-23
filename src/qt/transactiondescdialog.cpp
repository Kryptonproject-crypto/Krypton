// Copyright (c) 2011-2018 The Bitcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <qt/transactiondescdialog.h>
#include <qt/forms/ui_transactiondescdialog.h>

#include <qt/transactiontablemodel.h>

#include <QModelIndex>

#include <QDesktopServices>

#include <QUrl>

TransactionDescDialog::TransactionDescDialog(const QModelIndex &idx, QWidget *parent) :
    QDialog(parent),
    ui(new Ui::TransactionDescDialog)
{
    ui->setupUi(this);
    QString txid = idx.data(TransactionTableModel::TxHashRole).toString();
setWindowTitle(tr("Details for %1").arg(txid));

// lien vers l'explorateur
QString url = "https://explorer.krypton-project.com/search.php?q=" + txid;

// récupère la description longue (comme avant)
QString desc = idx.data(TransactionTableModel::LongDescriptionRole).toString();

// ajoute le lien cliquable au-dessus de la description
QString html = QString("<b>Explorer link:</b> <a href=\"%1\">%2</a><br><br>%3")
        .arg(url, txid, desc);

ui->detailText->setOpenExternalLinks(true);
ui->detailText->setTextInteractionFlags(Qt::TextBrowserInteraction);
ui->detailText->setHtml(html);
}

TransactionDescDialog::~TransactionDescDialog()
{
    delete ui;
}
