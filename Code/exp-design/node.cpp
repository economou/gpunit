#include <QVBoxLayout>
#include <iostream>
using namespace std;
#include "node.hpp"

void Node::paintEvent(QPaintEvent* event) {
    return;
}

void Node::createChildren() {
    cerr << "Test" << endl;
    QVBoxLayout* vbox = new QVBoxLayout(this);
    QPushButton* button = new QPushButton(tr(name.c_str()), this);
    vbox->addWidget(button);
    button = new QPushButton(tr("Node 2"), this);
    vbox->addWidget(button);
    button = new QPushButton(tr("Node 3"), this);
    vbox->addWidget(button);
}
