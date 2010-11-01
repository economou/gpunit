#include "modulestoolbox.h"
#include "ui_modulestoolbox.h"

ModulesToolBox::ModulesToolBox(QWidget *parent) :
    QToolBox(parent),
    ui(new Ui::ModulesToolBox)
{
    ui->setupUi(this);
}

ModulesToolBox::~ModulesToolBox()
{
    delete ui;
}
