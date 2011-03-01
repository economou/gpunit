#include "clusterview.hpp"
#include "ui_clusterview.h"

ClusterView::ClusterView(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::ClusterView)
{
    ui->setupUi(this);
}

ClusterView::~ClusterView()
{
    delete ui;
}
