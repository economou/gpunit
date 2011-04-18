.PHONY: all clean

PY_FILES = experimentmanager.py \
		   modulestoolbox.py \
		   clusterview.py \
		   moduleeditor.py \
		   node.py

PY_UI_FILES = gui/ui_modulestoolbox.py \
		  gui/ui_clusterview.py \
		  gui/ui_experimentmanager.py \
		  gui/ui_moduleeditor.py \
		  gui/ui_nodeinfodialog.py \
		  gui/ui_particlesettings.py \
		  gui/ui_node.py

all : $(PY_UI_FILES) $(PY_FILES)

gui/%.py : %.ui
	pyuic4 $^ -o $@

clean:
	-rm *.pyc
