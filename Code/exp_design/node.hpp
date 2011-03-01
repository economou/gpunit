#include <QWidget>
#include <QPushButton>
#include <string>
using std::string;

class Node : public QWidget {
    public:
        Node(QWidget* parent = NULL) : QWidget(parent), name("Node") {
            createChildren();
        }

        Node(const string& n, QWidget* parent = NULL) : QWidget(parent), name(n) {
            createChildren();
        }

        float getUsage() const; 
        int getNumCPUs() const; 
        float getFreeMemory() const; 
        int getTotalMemory() const; 

        void setUsage(const float& usage);
        void setNumCPUs(const int& cpus);
        void setFreeMemory(const float& freemem);
        void setTotalMemory(const int& totalmem);

    protected:
        virtual void paintEvent(QPaintEvent* event);

    private:
        void createChildren();

        string name;
        string ipAddress;
        float cpuUsage;
        int numCPUs;

        float freeMemory;
        int totalMemory;
};
