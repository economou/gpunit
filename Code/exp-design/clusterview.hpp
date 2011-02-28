#ifndef CLUSTERVIEW_HPP
#define CLUSTERVIEW_HPP

#include <QMainWindow>

namespace Ui {
    class ClusterView;
}

class ClusterView : public QMainWindow
{
    Q_OBJECT

public:
    explicit ClusterView(QWidget *parent = 0);
    ~ClusterView();

private:
    Ui::ClusterView *ui;
};

#endif // CLUSTERVIEW_HPP
