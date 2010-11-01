#include <QtGui/QApplication>
#include "mainwindow.h"

int main(int argc, char* args[]) {
    QApplication a(argc, args);
    MainWindow w;
    w.show();

    return a.exec();
}
