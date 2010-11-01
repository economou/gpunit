#include "mainwindow.h"
#include "moduleeditor.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    editor(new ModuleEditor(this))
{
    ui->setupUi(this);
}

MainWindow::~MainWindow() {
    delete ui;
    delete editor;
}

void MainWindow::on_actionEdit_Modules_triggered() {
    if(!editor->isVisible()){
        editor->show();
    }
}
