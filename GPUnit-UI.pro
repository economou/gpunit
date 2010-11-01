#-------------------------------------------------
#
# Project created by QtCreator 2010-11-01T12:26:03
#
#-------------------------------------------------

QT       += core gui

TARGET = GPUnit-UI
TEMPLATE = app


SOURCES += src/main.cpp\
        src/windows/mainwindow.cpp \
    src/windows/moduleeditor.cpp \
    src/widgets/modulestoolbox.cpp

HEADERS  += src/windows/mainwindow.h \
    src/windows/moduleeditor.h \
    src/widgets/modulestoolbox.h

FORMS    += ui/mainwindow.ui \
    ui/moduleeditor.ui \
    ui/modulestoolbox.ui
