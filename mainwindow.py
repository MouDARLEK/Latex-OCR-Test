import sys
import time
import pyperclip

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QImage, QPixmap, QIcon, QFont, QPalette, QColor
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QGraphicsPixmapItem, QGraphicsScene
from PyQt5 import uic

from PIL import Image
from PIL import ImageGrab

import matplotlib.font_manager as MatFont
from matplotlib.mathtext import math_to_image

from pix2tex.cli import LatexOCR
import screen_shot

import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


class button1Thread(QThread):
    bt1Signal = pyqtSignal(str)
    def __init__(self):
        super(button1Thread, self).__init__()
        self.bt1Run = True

    def begin(self):
        self.bt1Run = True
        print('thread1 begin')

    def stop(self):
        self.bt1Run = False
        print('thread1 stop')
        # self.wait()

    def run(self):
        while True:
            if self.bt1Run == True:
                img = Image.open("screenshots/func_shot.png")
                model = LatexOCR()
                model_str = model(img)
                print(model_str)
                prop = MatFont.FontProperties(math_fontfamily='stix', size=64, weight='bold')
                math_to_image('$'+model_str+'$', 'images/func0.png', prop=prop, dpi=72)
                self.bt1Signal.emit(str(model_str))

            self.sleep(1)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('app.ui', self)
        self.pushButton0.clicked.connect(self.showScreenShot)
        self.pushButton1.clicked.connect(self.button1Clicked)
        self.pushButton2.clicked.connect(self.button2Clicked)
        self.pushButton3.clicked.connect(self.button3Clicked)

        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setFont(QFont("微软雅黑", 16, QFont.Bold))

        # 按键1线程
        self.thread = QThread()
        self.bt1Thread = button1Thread()
        self.bt1Thread.moveToThread(self.thread)
        self.thread.started.connect(self.bt1Thread.run)
        self.bt1Thread.bt1Signal.connect(self.button1CallBack)

        # 设置快捷键
        self.pushButton3.setShortcut('f1')
        self.pushButton1.setShortcut('f3')

    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if a0.key() == QtCore.Qt.Key.Key_F1:
            self.button3Clicked()
        if a0.key() == QtCore.Qt.Key.Key_F3:
            self.button1Clicked()


    def button1Clicked(self):
        self.text1.setText("正在解析公式...")
        self.bt1Thread.begin()
        self.thread.start()


    def button1CallBack(self, msg):
        self.text1.setText(str(msg))
        pyperclip.copy(str(msg))
        self.bt1Thread.stop()
        self.showLatexPic()



    def button2Clicked(self):
        print("clear")
        graphicScene = QGraphicsScene()
        self.graphicsView1.setScene(graphicScene)
        self.text1.clear()



    def button3Clicked(self):
        print("screen shot")
        self.captureScreen()
        time.sleep(0.2)

    def showScreenShot(self):
        print('show pic')
        funcImg = QImage('screenshots/func_shot.png')
        funcPix = QPixmap.fromImage(funcImg)
        funcItem = QGraphicsPixmapItem(funcPix)
        graphicScene = QGraphicsScene()
        graphicScene.addItem(funcItem)
        self.graphicsView1.setScene(graphicScene)

    def showLatexPic(self):
        print('latex')
        funcImg = QImage('images/func0.png')
        funcPix = QPixmap.fromImage(funcImg)
        funcItem = QGraphicsPixmapItem(funcPix)
        graphicScene = QGraphicsScene()
        graphicScene.addItem(funcItem)
        self.graphicsView2.setScene(graphicScene)
        # self.graphicsView2.fitInView(funcItem)




    def captureScreen(self):
        try:
            self.showMinimized()
            time.sleep(0.3)
            img = ImageGrab.grab()
            img.save('screenshots/fullshot.png')
            self.child_window = screen_shot.Ui_MainWindow()
            self.child_window.show()
            self.showNormal()


        except:
            pass


def showMainWindow():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.setWindowIcon(QIcon('images/icon0.ico'))
    win.setWindowTitle('LatexOCR APP V1.0')

    mainTheme = QPalette()
    color = QColor()
    color.setRgb(180, 200, 220, 250)
    mainTheme.setColor(QPalette.Window, color)
    color.setRgb(48, 175, 152, 250)
    mainTheme.setColor(QPalette.ButtonText, color)

    win.setPalette(mainTheme)
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    showMainWindow()


