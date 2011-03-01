#include "modulestoolbox.hpp"
#include "ui_modulestoolbox.h"

ModulesToolBox::ModulesToolBox(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::ModulesToolBox)
{
    ui->setupUi(this);
}

ModulesToolBox::~ModulesToolBox()
{
    delete ui;
}
