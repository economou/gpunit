.PHONY: all clean

PY_FILES = experimentmanager.py \
		   modulestoolbox.py \
		   clusterview.py \
		   moduleeditor.py \
		   node.py

PY_UI_FILES = ui_modulestoolbox.py \
		  ui_clusterview.py \
		  ui_experimentmanager.py \
		  ui_moduleeditor.py \
		  ui_nodeinfodialog.py

all : $(PY_UI_FILES) $(PY_FILES)

%.py : %.ui
	pyuic4 $^ -o $@

clean:
	-rm $(PY_UI_FILES)
	-rm *.pyc
