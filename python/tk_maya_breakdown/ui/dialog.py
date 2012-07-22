# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Sun Jul 22 13:39:30 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(834, 618)
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Scene Breakdown", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "<b><big>Scene Breakdown</big></b>\n"
"<br><br>\n"
"See what is out of date in your scene.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.left_browser = SceneBrowserWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_browser.sizePolicy().hasHeightForWidth())
        self.left_browser.setSizePolicy(sizePolicy)
        self.left_browser.setObjectName(_fromUtf8("left_browser"))
        self.gridLayout.addWidget(self.left_browser, 0, 0, 1, 1)
        self.right_browser = PublishBrowserWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.right_browser.sizePolicy().hasHeightForWidth())
        self.right_browser.setSizePolicy(sizePolicy)
        self.right_browser.setObjectName(_fromUtf8("right_browser"))
        self.gridLayout.addWidget(self.right_browser, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setMargin(2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setText(QtGui.QApplication.translate("Dialog", "Filters:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.chk_green = QtGui.QCheckBox(self.groupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/green_bullet.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.chk_green.setIcon(icon)
        self.chk_green.setObjectName(_fromUtf8("chk_green"))
        self.horizontalLayout_2.addWidget(self.chk_green)
        self.chk_red = QtGui.QCheckBox(self.groupBox)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/res/red_bullet.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.chk_red.setIcon(icon1)
        self.chk_red.setObjectName(_fromUtf8("chk_red"))
        self.horizontalLayout_2.addWidget(self.chk_red)
        self.horizontalLayout.addWidget(self.groupBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass

from ..publish_browser import PublishBrowserWidget
from ..scene_browser import SceneBrowserWidget
from . import resources_rc
