.PHONY: all clean

GUI_PATH = exp_design/gui

PY_RC_FILES = $(GUI_PATH)/imgres_rc.py

PY_UI_FILES = $(GUI_PATH)/modulestoolbox_ui.py \
		  $(GUI_PATH)/clusterview_ui.py \
		  $(GUI_PATH)/experimentmanager_ui.py \
		  $(GUI_PATH)/moduleeditor_ui.py \
		  $(GUI_PATH)/nodeinfodialog_ui.py \
		  $(GUI_PATH)/particlesettings_ui.py \
		  $(GUI_PATH)/node_ui.py

all : $(PY_UI_FILES) $(PY_RC_FILES)

$(GUI_PATH)/%_ui.py : $(GUI_PATH)/%.ui
	pyuic4 $^ -o $@

$(GUI_PATH)/%_rc.py : $(GUI_PATH)/%.qrc
	pyrcc4 $^ -o $@

clean:
	-rm $(PY_UI_FILES)
	-rm $(PY_RC_FILES)
	-rm $(GUI_PATH)/*.pyc
