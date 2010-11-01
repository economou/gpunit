#include "moduleeditor.h"
#include "ui_moduleeditor.h"

ModuleEditor::ModuleEditor(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::ModuleEditor)
{
    ui->setupUi(this);
}

ModuleEditor::~ModuleEditor() {
    delete ui;
}
