from PyQt4.QtGui import QDialog, QApplication, QFormLayout, QLabel, QPushButton
from PyQt4.QtGui import QVBoxLayout, QHBoxLayout
from PyQt4.QtGui import QDoubleSpinBox, QSpinBox, QLineEdit, QComboBox, QCheckBox

from PyQt4.QtCore import SIGNAL

class SettingsDialog(QDialog):
    def __init__(self, inputs, defaults, parent = None):
        QDialog.__init__(self, parent)

        self.inputs = inputs
        self.defaults = defaults
        self.outputs = {}

        self.form = QFormLayout()
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        for label, valueType in self.inputs.items():
            label = label
            widget = self.widgetByType(valueType)

            self.outputs[label] = widget
            self.form.addRow(label, widget)

        self.okButton = QPushButton("Ok")
        self.cancelButton = QPushButton("Cancel")

        self.connect(self.okButton, SIGNAL("clicked()"), self.accept)
        self.connect(self.cancelButton, SIGNAL("clicked()"), self.reject)

        self.hbox.addWidget(self.okButton)
        self.hbox.addWidget(self.cancelButton)

        self.vbox.addLayout(self.form)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)

    def getValues(self):
        # Populate initial inputs with default values.
        for label, default in self.defaults.items():
            widget = self.outputs[label]

            if isinstance(widget, QSpinBox):
                widget.setValue(int(default))
            elif isinstance(widget, QDoubleSpinBox):
                widget.setValue(float(default))
            elif isinstance(widget, QComboBox):
                index = widget.findText(default)
                widget.setCurrentIndex(index)
            elif isinstance(widget, QLineEdit):
                widget.setText(str(default))
            elif isinstance(widget, QCheckBox):
                widget.setChecked(default)

        ret = self.exec_()

        results = {}

        # If the user accepted their input, pull out the values from the UI and
        # return them as a dictionary.
        if ret == QDialog.Accepted:
            for label, widget in self.outputs.items():
                if isinstance(widget, QSpinBox):
                    value = int(widget.value())

                    results[label] = value
                    self.defaults[label] = value
                elif isinstance(widget, QDoubleSpinBox):
                    value = float(widget.value())

                    results[label] = value
                    self.defaults[label] = value
                elif isinstance(widget, QComboBox):
                    value = str(widget.currentText())

                    results[label] = value
                    self.defaults[label] = value
                elif isinstance(widget, QLineEdit):
                    value = str(widget.text())

                    results[label] = value
                    self.defaults[label] = value
                elif isinstance(widget, QCheckBox):
                    value = widget.isChecked()

                    results[label] = value
                    self.defaults[label] = value

        return results

    def widgetByType(self, valueType):
        if isinstance(valueType, str):
            valPieces = valueType.lower().split(":")
            typeStr = valPieces[0]

            rngMin = "min"
            rngMax = "max"

            if len(valPieces) == 3:
                rngMin = valPieces[1] if valPieces[1] != "" else "min"
                rngMax = valPieces[2] if valPieces[2] != "" else "max"

            if typeStr == "float":
                box = QDoubleSpinBox(self)
                if rngMin == "min":
                    rngMin = -2000000000.
                else:
                    rngMin = float(rngMin)

                if rngMax == "max":
                    rngMax = 2000000000.
                else:
                    rngMax = float(rngMax)

                box.setRange(rngMin, rngMax)
                box.setDecimals(10)
                return box
            elif typeStr == "int":
                box = QSpinBox(self)
                if rngMin == "min":
                    rngMin = -2**31 + 1
                else:
                    rngMin = int(rngMin)

                if rngMax == "max":
                    rngMax = 2**31 - 1
                else:
                    rngMax = int(rngMax)

                box.setRange(rngMin, rngMax)
                return box
            elif typeStr == "str":
                return QLineEdit(self)
            elif typeStr == "bool":
                return QCheckBox(self)
        elif isinstance(valueType, list):
            box = QComboBox(self)
            for item in valueType:
                box.addItem(item)

            return box
