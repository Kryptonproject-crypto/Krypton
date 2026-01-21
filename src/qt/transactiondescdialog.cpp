// Copyright (c) 2011-2018 The Bitcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <qt/transactiondescdialog.h>
#include <qt/forms/ui_transactiondescdialog.h>
#include <qt/transactiontablemodel.h>
#include <QModelIndex>
#include <QDesktopServices>
#include <QUrl>
#include <QMouseEvent>

TransactionDescDialog::TransactionDescDialog(const QModelIndex &idx, QWidget *parent) :
    QDialog(parent),
    ui(new Ui::TransactionDescDialog)
{
    ui->setupUi(this);
    QString txid = idx.data(TransactionTableModel::TxHashRole).toString();
setWindowTitle(tr("Details for %1").arg(txid));

// lien vers l'explorateur
QString url = "https://explorer.krypton-explorer.org/tx/" + txid;

// récupère la description longue (comme avant)
QString desc = idx.data(TransactionTableModel::LongDescriptionRole).toString();

// ajoute le lien cliquable au-dessus de la description
QString html = QString("<b>Explorer link:</b> <a href=\"%1\">%2</a><br><br>%3")
        .arg(url, txid, desc);

//ui->detailText->setOpenExternalLinks(true);
ui->detailText->setTextInteractionFlags(Qt::TextBrowserInteraction);
ui->detailText->viewport()->installEventFilter(this);
ui->detailText->viewport()->setMouseTracking(true);
ui->detailText->setHtml(html);
}

TransactionDescDialog::~TransactionDescDialog()
{
    delete ui;
}

bool TransactionDescDialog::eventFilter(QObject *obj, QEvent *event)
{
    if (obj == ui->detailText->viewport()) {
        
        // Clicks
        if (event->type() == QEvent::MouseButtonRelease) {
            QMouseEvent *mouseEvent = static_cast<QMouseEvent*>(event);
            QString anchor = ui->detailText->anchorAt(mouseEvent->pos());
            
            if (!anchor.isEmpty()) {
                QDesktopServices::openUrl(QUrl(anchor));
                return true; 
            }
        }
        
        // Hovering
        else if (event->type() == QEvent::MouseMove) {
            QMouseEvent *mouseEvent = static_cast<QMouseEvent*>(event);
            QString anchor = ui->detailText->anchorAt(mouseEvent->pos());
            
            if (!anchor.isEmpty()) {
                ui->detailText->viewport()->setCursor(Qt::PointingHandCursor);
            } else {
                ui->detailText->viewport()->setCursor(Qt::IBeamCursor);
            }
        }
    }
    
    return QDialog::eventFilter(obj, event);
}