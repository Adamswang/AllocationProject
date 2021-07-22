# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AllocaitonDialog_v2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import os
import PyQt5
plugin_path = '/opt/anaconda3/lib/python3.8/site-packages/PyQt5/Qt5/plugins/platforms/'
os.environ['QT_QPA_PLATFORM_PLUGINS_PATH'] = plugin_path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(398, 578)
        font = QtGui.QFont()
        font.setFamily("Myriad Set")
        Dialog.setFont(font)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 361, 541))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.textEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 2)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 1, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_5.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Supply and Demand File Checking"))
        self.pushButton_4.setText(_translate("Dialog", "Close"))
        self.pushButton_5.setText(_translate("Dialog", "Process"))

