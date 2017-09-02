from PyQt5.QtWidgets import *

import sys

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.grid = QGridLayout()
        self.grid.addWidget(self.createFistExclusiveGroup(), 0, 0)
        self.grid.addWidget(self.createSecondExclusiveGroup(), 1, 0)
        self.grid.addWidget(self.createNoneExclusiveGroup(), 0, 1)
        self.grid.addWidget(self.createPushButtonGroup(), 1, 1)
        self.setLayout(self.grid)

        self.setWindowTitle('Group Boxes')
        self.resize(480, 320)

    def createFistExclusiveGroup(self):
        groupBox = QGroupBox('Exclusive Radio Buttons')

        radiao1 = QRadioButton('&Radio Button 1')
        radiao2 = QRadioButton('R&adio Button 2')
        radiao3 = QRadioButton('Ra&dio Button 3')
        radiao1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radiao1)
        vbox.addWidget(radiao2)
        vbox.addWidget(radiao3)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createSecondExclusiveGroup(self):
        groupBox = QGroupBox('E&xclusive Radio Buttons')

        radiao1 = QRadioButton('&Radio Button 1')
        radiao2 = QRadioButton('R&adio Button 2')
        radiao3 = QRadioButton('Ra&dio Button 3')
        radiao1.setChecked(True)
        checkBox = QCheckBox('Ind&ependent checkbox')
        checkBox.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radiao1)
        vbox.addWidget(radiao2)
        vbox.addWidget(radiao3)
        vbox.addWidget(checkBox)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createNoneExclusiveGroup(self):
        groupBox = QGroupBox('None-E&xclusive Checkboxes')

        checkBox1 = QCheckBox('&Checkbox 1')
        checkBox2 = QCheckBox('C&heckbox 2')
        checkBox2.setChecked(True)
        tristateBox = QCheckBox('Tri-&state button')
        tristateBox.setTristate(True)

        vBox = QVBoxLayout()
        vBox.addWidget(checkBox1)
        vBox.addWidget(checkBox2)
        vBox.addWidget(tristateBox)
        vBox.addStretch(1)
        groupBox.setLayout(vBox)

        return groupBox

    def createPushButtonGroup(self):
        groupBox = QGroupBox('&Push Buttons')
        groupBox.setCheckable(True)
        groupBox.setChecked(True)

        pushButton = QPushButton('&Normal Button')
        toggleButton = QPushButton('&Toggle Button')
        toggleButton.setCheckable(True)
        toggleButton.setChecked(True)
        flatButton = QPushButton('&Flat Button')
        flatButton.setFlat(True)
        popupButton = QPushButton('Pop&up Button')

        menu = QMenu(self)
        menu.addAction('&First Item')
        menu.addAction('&Second Item')
        menu.addAction('&Third Item')
        menu.addAction('F&ourth Item')
        popupButton.setMenu(menu)

        vBox = QVBoxLayout()
        vBox.addWidget(pushButton)
        vBox.addWidget(toggleButton)
        vBox.addWidget(flatButton)
        vBox.addWidget(popupButton)
        vBox.addStretch(1)
        groupBox.setLayout(vBox)

        return groupBox


app = QApplication(sys.argv)
win = Window()
win.show()
app.exec_()
