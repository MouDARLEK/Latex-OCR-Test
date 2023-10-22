from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PIL import ImageGrab
import os

# 此ui作为子窗口被调用
class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.resize(1920, 1080)

        self.firstPoint = QtCore.QPoint()
        self.endPoint = QtCore.QPoint()
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint) #让窗口显示在屏幕的最上层
        self.setWindowState(QtCore.Qt.WindowFullScreen)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        paint = QtGui.QPainter(self)
        paint.drawPixmap(0, 0, QtGui.QPixmap('screenshots/fullshot.png'))
        pen = QtGui.QPen(QtCore.Qt.green, 1, QtCore.Qt.DashLine)
        paint.setPen(pen)
        paint.drawRect(self.firstPoint.x(), self.firstPoint.y(), self.endPoint.x() - self.firstPoint.x(),
                       self.endPoint.y() - self.firstPoint.y())

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.firstPoint = a0.pos()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.endPoint = a0.pos()
        self.update()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.endPoint = a0.pos()
        self.update()
        # os.remove('screenshots/func_shot.png')
        im = ImageGrab.grab((self.firstPoint.x()+1 , self.firstPoint.y()+1 , self.endPoint.x(), self.endPoint.y()))
        im.save(f"screenshots/func_shot.png")
        os.remove('screenshots/fullshot.png')
        self.close()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(723, 491)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
