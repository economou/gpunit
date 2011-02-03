#ifndef MODULEEDITOR_H
#define MODULEEDITOR_H

#include <QMainWindow>

namespace Ui {
    class ModuleEditor;
}

class ModuleEditor : public QMainWindow {
    Q_OBJECT

public:
    explicit ModuleEditor(QWidget *parent = 0);
    ~ModuleEditor();

private:
    Ui::ModuleEditor *ui;
};

#endif // MODULEEDITOR_H
