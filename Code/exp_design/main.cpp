#include <QtGui/QApplication>
#include "experimentmanager.hpp"

int main(int argc, char* args[]) {
    QApplication a(argc, args);
    ExperimentManager w;
    w.show();

    return a.exec();
}
