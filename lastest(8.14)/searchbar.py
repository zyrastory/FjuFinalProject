import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *

app = QApplication(sys.argv)

model = QStringListModel()
model.setStringList(['some', 'words', 'in', 'my', 'dictionary'])

completer = QCompleter()
completer.setModel(model)

lineedit = QLineEdit()
lineedit.setCompleter(completer)
lineedit.show()

sys.exit(app.exec_())