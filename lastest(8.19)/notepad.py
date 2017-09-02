import os
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Notepad(QWidget):

    def __init__(self):
        super().__init__()
        self.text = QTextEdit(self)
        f = self.text.font()
        f.setPointSize(14) 
        self.text.setFont(f)
        self.text.setFixedSize(475,280)

        self.compile_place = QTextEdit(self)
        F = self.compile_place.font()
        F.setPointSize(12) 
        self.compile_place.setFont(F)


        
        self.strw = QListWidget(self)
        self.strategybutton = QPushButton('確認',self)
        self.clr_btn = QPushButton('清除',self)
        self.compile_btn = QPushButton('編譯',self)
       
        listB = []
        for dirPath, dirNames, fileNames in os.walk \
        ("C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\internal"):
            fileNames = [ fi for fi in fileNames if  fi.endswith(".md") ] 
            for f in fileNames:
                listB.append(f.replace(".md",""))
                
        self.strw.addItems(listB)
        self.strw.setFixedSize(300,580)

        self.init_ui()

    def init_ui(self):
        
        
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        h_layout2 =QHBoxLayout()
        
        
        v_layout.addWidget(self.text)
        h_layout.addWidget(self.clr_btn)
        h_layout.addWidget(self.strategybutton)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.compile_btn)
        v_layout.addWidget(self.compile_place)        #編譯
        

        h_layout2.addLayout(v_layout)
        h_layout2.addWidget(self.strw)
        
        
        self.strategybutton.clicked.connect(self.txt)
        self.clr_btn.clicked.connect(self.clear_text)
        self.compile_btn.clicked.connect(self.compiler)

        self.setLayout(h_layout2)
        self.setWindowTitle('PyQt5 TextEdit')



    def save_text(self):
        path = "C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\User"
        filename = QFileDialog.getSaveFileName(self, 'Save File',path,"*.md")

        try:
            with open(filename[0], 'w', encoding = 'utf8') as f:
                my_text = self.text.toPlainText()
                f.write(my_text)
        except FileNotFoundError:
            print("why dont save me")

    def open_text(self):
        path = "C:\\Users\\user\\Desktop\\lastest(8.19)\\strategy\\User"
        filename = QFileDialog.getOpenFileName(self, 'Open File',path,"*.md;;*.txt")

        try:
            with open(filename[0], 'r', encoding = 'utf8') as f:
                file_text = f.read()
                self.text.setText(file_text)
            self.strw.clearSelection()
        except FileNotFoundError:
            print("why no open")

    def txt(self):

        try:
            for i in self.strw.selectedItems():
                choose = i.text()
            path = "C:\\Users\\user\\Desktop\\lastest(8.19)"
            with open("./strategy/internal/"+choose+".md", 'r', encoding = 'utf8') as f:
                
                r = None
                r = f.read()
                self.text.setText(r)
        except:
            print("no choose no text")
        #except Exception as e: print (str(e))
        

    def clear_text(self):
        self.text.clear()
        self.compile_place.clear()

    def compiler(self):
        os.system("del cache\\compiler.md")
        os.system("del cache\\compiler.py")

        

        with open("./cache/compiler.md", 'w', encoding = 'utf8') as f:
            my_text = self.text.toPlainText()
            f.write(my_text)

        my_text2 = my_text.replace(" ","")
        my_text3 = my_text2.replace("\n","")
        my_text4 = my_text3.replace("\t","")


        if my_text == "" or my_text4 == "":
            self.compile_place.setText("ERROR_001:連個毛都沒寫，印雞雞啦") 

        elif my_text.find("import") == -1 or my_text.find("pyalgotrade") == -1\
            or my_text.find("strategy") == -1:
            self.compile_place.setText("ERROR_002:沒有import 所需模組(pyalgotrade)")

        elif my_text.find("enterLong") == -1:
            self.compile_place.setText("ERROR_003:沒有買進無法成立策略")
        elif my_text.find("exitMarket") == -1:
            self.compile_place.setText("ERROR_004:沒有寫入退場方式")
        else:
            try:
                import part1
                self.compile_place.setText("編譯成功success")
                QTimer.singleShot(2000, self.save_text)
                

            except Exception as e: 
                #print (str(e))
                if str(e)=="module 'compiler' has no attribute 'MyStrategy'":
                    self.compile_place.setText("ERROR_05:沒寫MyStrategy進主程式")
                
                elif str(e).find("invalid syntax") != -1:
                    self.compile_place.setText("ERROR_06:invalid syntax error")                    
                
                elif str(e).find("types") != -1:
                    self.compile_place.setText("ERROR_07:TypesError，None Type cannot \
compare with integer or float")
                else:
                    self.compile_place.setText(str(e))
                    print (str(e))




class Writer(QMainWindow):
    
    def __init__(self, parent = None):
        super(Writer, self).__init__(parent)
        self.setFixedSize(800,650)
        self.setWindowTitle('Note')
        self.form_widget = Notepad()
        self.form_widget.setFixedSize(800, 600)
        self.setCentralWidget(self.form_widget)
        self.init_ui()
    def init_ui(self):
        bar = self.menuBar()
        file = bar.addMenu('File')

        new_action = QAction('New', self)
        new_action.setShortcut('Ctrl+N')

        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')

        open_action = QAction('&Open', self)

        quit_action = QAction('&Quit', self)

        file.addAction(new_action)
        file.addAction(save_action)
        file.addAction(open_action)
        file.addAction(quit_action)

        quit_action.triggered.connect(self.quit_trigger)
        file.triggered.connect(self.respond)         
            

    def quit_trigger(self):
        self.close()
        #qApp.quit()

    def respond(self, q):
        signal = q.text()

        if signal == 'New':
            self.form_widget.clear_text()
        elif signal == '&Open':
            self.form_widget.open_text()
        elif signal == '&Save':
            self.form_widget.save_text()

    def closeEvent(self, event):

        os.system("del cache\\compiler.md")
        os.system("del cache\\compiler.py")