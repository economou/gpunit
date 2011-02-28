#include <QFileDialog>

#include "experimentmanager.hpp"
#include "moduleeditor.hpp"
#include "clusterview.hpp"
#include "ui_experimentmanager.h"

ExperimentManager::ExperimentManager(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::ExperimentManager),
    editor(new ModuleEditor(this)),
    clusterViewer(new ClusterView(this))
{
    ui->setupUi(this);
}

ExperimentManager::~ExperimentManager() {
    delete ui;
    delete editor;
}

void ExperimentManager::on_actionEdit_Modules_triggered() {
    if(!editor->isVisible()){
        editor->show();
    }
}

void ExperimentManager::on_actionOpen_Experiment_triggered() {
    QWidget* parent = parentWidget();
    if(!parent) {
        parent = this;
    }

    static_cast<ExperimentManager*>(parent)->openNewManager();
}

void ExperimentManager::on_actionSave_Experiment_triggered() {
    QFileDialog::getSaveFileName(this, "Save experiment as...");
}

void ExperimentManager::openNewManager() {
    managers.push_back(new ExperimentManager(this));
    managers[managers.size()-1]->show();
}

void ExperimentManager::on_actionRun_Experiment_triggered() {
    clusterViewer->show();
}
