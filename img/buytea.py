__author__ = 'Ann'
# !/usr/bin/python
# -*- coding: utf-8 -*-
# maintea.py

import sys
import os
import math
import re
import Queue
from multiprocessing import Queue, Process
from time import sleep
from datetime import datetime
from PySide import QtGui
from PySide import QtCore
from subprocess import Popen, PIPE, check_output
from threading import Thread


import ConfigParser
config = ConfigParser.ConfigParser()
config.read('config.ini')
windowsTitle = unicode(config.get('main', 'windowsTitle').decode('utf8'))
teaBuy = unicode(config.get('main', 'teaBuy').decode('utf8'))
teaName = unicode(config.get('main', 'teaName').decode('utf8'))

temperature = unicode(config.get('main', 'temperature').decode('utf8'))
teaFirst = unicode(config.get('main', 'teaFirst').decode('utf8'))
teaSecond = unicode(config.get('main', 'teaSecond').decode('utf8'))
teaThird = unicode(config.get('main', 'teaThird').decode('utf8'))
teaFourth = unicode(config.get('main', 'teaFourth').decode('utf8'))

need = unicode(config.get('main', 'need').decode('utf8'))
your = unicode(config.get('main', 'your').decode('utf8'))

text = unicode(config.get('main', 'text').decode('utf8'))
PRICE = unicode(config.get('main', 'price').decode('utf8'))

balanceint = unicode(config.get('main', 'balanceint').decode('utf8'))


class BalanceUpdate(QtCore.QObject):
        sig = QtCore.Signal(int)

class AcceptorThread(QtCore.QThread):

    def __init__(self, parent=None):
        super(AcceptorThread, self).__init__(parent)
        self.exiting = False
        self.signal = BalanceUpdate()

    def run(self):
        self.billPath = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'bill_acceptor.py')

        self.billProc = Popen(
            ['sudo', self.billPath],
            stdout=PIPE,
            close_fds=True,
            universal_newlines=True
        )
        self.billQueue = Queue.Queue()

        self.bill = Thread(target=self.enqueue_output,
                           args=(self.billProc.stdout, self.billQueue))
        self.bill.daemon = False
        self.bill.start()

        while not self.exiting:
            try:
                line = self.billQueue.get_nowait()
                amount = int(line)
                if amount:
                    self.signal.sig.emit(amount)
            except Queue.Empty:
                pass
            sleep(0.2)

        self.billProc.terminate()
        self.billProc.wait()

    def enqueue_output(self, out, queue):
        while True:
            line = out.readline()
            if line:
                queue.put(line.strip())
            else:
                break
        out.close()


class MoneyScreen(QtGui.QWidget):
    def __init__(self):
        super(MoneyScreen, self).__init__()
        self.initUI()
        self.initStyle()

    def initUI(self):
        self._layout = QtGui.QGridLayout()
        self.fon2 = fon2()
        self._layout.addWidget(self.fon2, 1, 1)
        desktop = QtGui.QApplication.desktop()
        rect = desktop.availableGeometry()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.setGeometry(0, 250, 1280, 350)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setLayout(self._layout)
        self.show()

    def initStyle(self):
        img_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'img/1.png')
        tile = QtGui.QPixmap(img_path)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, tile)
        self.setPalette(palette)
    
    
class fon2(QtGui.QWidget): 
    def __init__(self, *args, **kwargs):
        super(fon2, self).__init__(*args, **kwargs)
        self.initUI()
        self.initStyle()

    def initUI(self):
        self._layout = QtGui.QGridLayout()
        self.yourMoney = QtGui.QPushButton()
        self.yourMoney2 = QtGui.QPushButton()
	
        self._layout.addWidget(self.yourMoney, 1, 0)
        self._layout.addWidget(self.yourMoney2, 1, 2)

        self.yourMoney.setText( u' %s ' % PRICE)
        self.yourMoney2.setText(your)

        self.setLayout(self._layout)

    def initStyle(self):

        self.yourMoney.setStyleSheet(
            "QPushButton {"
            "font-size: 32px;"
            "background: transparent;"
            "border: 3px solid #ffffff;"
            "color: #ffffff;"
            "width: 363px;"
            "height: 70px}"
        )
        self.yourMoney2.setStyleSheet(
            "QPushButton {"
            "font-size: 32px;"
            "background: transparent;"
            "border: 3px solid #ffffff;"
            "color: #ffffff;"
            "width: 363px;"
            "height: 70px}"
        )

class teaFirstWidget(QtGui.QWidget): 
    def __init__(self, money, *args, **kwargs):
        super(teaFirstWidget, self).__init__(*args, **kwargs)
        self.initUI()
        self.initStyle()
        self.initAction()
        self.moneyScreen = money

    def initUI(self):
        self._layout = QtGui.QGridLayout()
        self.teaName = QtGui.QPushButton()
	self.teaBuy = QtGui.QPushButton()
        self.info = QtGui.QTextEdit()
        self.temperature = QtGui.QLabel()
	
	self.teaPrice = QtGui.QLabel(u'%s ' % PRICE)
	self.balanceLabel = QtGui.QLabel()	
	self.balanceLabel._format = u'balans %s rub.'
	self.balanceLabel.setWordWrap(True)
	
        
	self._layout.addWidget(self.teaName, 1, 0, 1, 1)
        self._layout.addWidget(self.info, 2, 0, 2, 3)
        self._layout.addWidget(self.teaPrice, 4, 0, 1, 1)
        self._layout.addWidget(self.teaBuy, 5, 0, 1, 1,
                               alignment =  QtCore.Qt.AlignTop)
	self._layout.addWidget(self.balanceLabel, 6, 0, 1, 1)
        self._layout.addWidget(self.temperature, 7, 0, 1, 1,
                               alignment = QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        self.info.setText(text)
        self.info.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setLayout(self._layout)
        self._layout = QtGui.QGridLayout()

    def initStyle(self):
        self.setGeometry(-9, 0, 0, 0)
        self.setContentsMargins(-9,0,0,0)
        self.teaBuy.setText(teaBuy) 
        self.teaName.setText(teaName) 
        self.temperature.setText(temperature)
	self.balanceLabel.setStyleSheet(
            "QLabel{font-size: 18px;}"
        )
        self.teaName.setStyleSheet(
            "QPushButton {"
            "font-size: 32px;"
            "background: transparent;"
            "border: 3px solid #ffffff;"
            "color: #ffffff;"
            "width: 363px;"
            "height: 70px}"
        )
        self.teaPrice.setStyleSheet(
            "QLabel {"
            "font-size: 32px;"
            "background: transparent;"
            "border: 3px solid #ffffff;"
            "color: #ffffff;"
            "width: 363px;"
            "height: 70px}"
        )
        self.teaBuy.setStyleSheet(
            "QPushButton {"
            "font-size: 32px;"
            "background: transparent;"
            "border: 3px solid #ffffff;"
            "color: #ffffff;"
            "width: 363px;"
            "height: 70px}"
        )
        self.info.setStyleSheet(
            "QTextEdit {"
            "background: transparent;"
            "border: none;"
            "color: #ffffff;"
            "font-size: 18px;"
            "padding: 2px}"
        )
        self.temperature.setStyleSheet(
            "QLabel {"
            "background: transparent;"
            "color: #ffffff;"
            "font-size: 18px;"
            "padding: 2px}"
        )

    def initAction(self):
        self.teaBuy.clicked.connect(lambda: self.onTeaBuy())

    def onTeaBuy(self):
        self.moneyScreen.show()

class teaSecondWidget(QtGui.QWidget): 
    def __init__(self, *args, **kwargs):
        super(teaSecondWidget, self).__init__(*args, **kwargs)
        self.initUI()
        self.initStyle()
    def initUI(self):
        self._layout = QtGui.QGridLayout()
        self.teaImage = QtGui.QPushButton()
        self._layout.addWidget(self.teaImage, 0, 0,
                               alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)
        self.setLayout(self._layout)
    def initStyle(self):
        self.setContentsMargins(0,0,0,0)
        img_path1 = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'img/plasticbottle2.png')
        #img_path1 = os.path.join('C:/Users/Ann/PycharmProjects/teabox/img/#plasticbottle2.png')
        self.teaImage.setFocusPolicy(QtCore.Qt.NoFocus)
        self.teaImage.setStyleSheet(
            "QPushButton {"
            "background: url(" + img_path1 + ");"
            "border: none;"
            "color: #ffffff;"
            "min-height: 630px;"
            "min-width: 365px}"
        )

class teaThirdWidget(QtGui.QWidget): 
    def __init__(self):
        super(teaThirdWidget, self).__init__()
        self.initUI()
        self.initStyle()
    def initUI(self):
        self._layout = QtGui.QGridLayout()
        self.teaFirst = QtGui.QPushButton()
        self.teaSecond = QtGui.QPushButton()
        self.teaThird = QtGui.QPushButton()
        self.teaFourth = QtGui.QPushButton()
        self.info = QtGui.QLabel()


        self._layout.addWidget(self.teaFirst, 1, 0, 1, 1)
        self._layout.addWidget(self.teaSecond, 2, 0, 1, 1)
        self._layout.addWidget(self.teaThird, 3, 0, 1, 1)
        self._layout.addWidget(self.teaFourth, 4, 0, 1, 1)
        self._layout.addWidget(self.info, 5, 0, 1, 1,
                               alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
	

        self.setLayout(self._layout)

    def initStyle(self):
        self.setGeometry(0, 0, -9, 0)
        self.setContentsMargins(0,200,-9,0)
        self.teaFirst.setText(teaFirst)
        self.teaSecond.setText(teaSecond)
        self.teaThird.setText(teaThird)
        self.teaFourth.setText(teaFourth)
	
	
        self.teaFirst.setStyleSheet(
            "QPushButton {"
            "font-size: 32px;"
            "background: transparent;"
            "border: 3px solid #ffffff;"
            "color: #ffffff;"
            "width: 363px;"
            "height: 70px}"
        )
        self.teaSecond.setStyleSheet(
            "QPushButton {"
            "font-size: 32px;"
            "background: transparent;"
            "border: 3px solid #ffffff;"
            "color: #ffffff;"
            "width: 363px;"
            "height: 70px}"
        )
        self.teaThird.setStyleSheet(
            "QPushButton {"
            "font-size: 32px;"
            "background: transparent;"
            "border: 3px solid #ffffff;"
            "color: #ffffff;"
            "width: 363px;"
            "height: 70px}"
        )
        self.teaFourth.setStyleSheet(
            "QPushButton {"
            "font-size: 32px;"
            "background: transparent;"
            "border: 3px solid #ffffff;"
            "color: #ffffff;"
            "width: 363px;"
            "height: 70px}"
        )

class Main(QtGui.QWidget):
    def __init__(self, money):
        super(Main, self).__init__()

        self.moneyScreen = money
        self.initUI()
        self.initStyle()
	self.initThread()
	self.balance = balanceint
	

    def initUI(self):
        self._layout = QtGui.QGridLayout(self)
        self.teaFirstWidget = teaFirstWidget(self.moneyScreen)
        self.teaSecondWidget = teaSecondWidget()
        self.teaThirdWidget = teaThirdWidget()
        self._layout.addWidget(self.teaFirstWidget, 0, 0)
        self._layout.addWidget(self.teaSecondWidget, 0, 1)

        self._layout.addWidget(self.teaThirdWidget, 0, 2)

        self.setLayout(self._layout)
        self.setWindowTitle(windowsTitle) #config
        desktop = QtGui.QApplication.desktop()
        rect = desktop.availableGeometry()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.show()

    def initStyle(self):
        img_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'img/1.png')
        tile = QtGui.QPixmap(img_path)
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, tile)
        self.setPalette(palette)
    
    def initThread(self):
	self.acceptorThread = AcceptorThread()
	self.acceptorThread.signal.sig.connect(self.on_balance_update)

	self.acceptorThread.start()

    @property
    def balance(self, value):
	self._balance = value
	self.teaThirdWidget.balanceLabel.setText(
	    self.teaThirdWidget.balanceLabel._format % value)

    def on_balance_update(self, data):
	self.balance +=int(data)

    
def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName(windowsTitle)
    money_screen = MoneyScreen()
    money_screen.hide()
    main_inst = Main(money_screen)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

