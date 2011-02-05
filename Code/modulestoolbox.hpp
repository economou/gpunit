#ifndef MODULESTOOLBOX_H
#define MODULESTOOLBOX_H

#include <QWidget>

namespace Ui {
    class ModulesToolBox;
}

class ModulesToolBox : public QWidget
{
    Q_OBJECT

public:
    explicit ModulesToolBox(QWidget *parent = 0);
    ~ModulesToolBox();

private:
    Ui::ModulesToolBox *ui;
};

#endif // MODULESTOOLBOX_H
