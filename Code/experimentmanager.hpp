#ifndef EXPERIMENTMANAGER_H
#define EXPERIMENTMANAGER_H

#include <QMainWindow>
#include<vector>
using std::vector;

#include "moduleeditor.hpp"

namespace Ui {
    class ExperimentManager;
}

class ExperimentManager : public QMainWindow {
    Q_OBJECT

public:
    explicit ExperimentManager(QWidget *parent = 0);
    ~ExperimentManager();

private:
    Ui::ExperimentManager *ui;
    ModuleEditor* editor;
    void openNewManager();

    vector<ExperimentManager*> managers;

public slots:
    void on_actionEdit_Modules_triggered();
    void on_actionOpen_Experiment_triggered();
    void on_actionRun_Experiment_triggered();
    void on_actionSave_Experiment_triggered();
};

#endif // EXPERIMENTMANAGER_H
