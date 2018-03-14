# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'my_ui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, Qt
from PyQt4 import phonon
from RangeSlider import RangeSlider

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(765, 582)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.videoPlayer = phonon.Phonon.VideoPlayer(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoPlayer.sizePolicy().hasHeightForWidth())
        self.videoPlayer.setSizePolicy(sizePolicy)
        self.videoPlayer.setObjectName(_fromUtf8("videoPlayer"))
        self.verticalLayout.addWidget(self.videoPlayer)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.play_pauseButton = QtGui.QToolButton(self.centralwidget)
        self.play_pauseButton.setEnabled(False)
        self.play_pauseButton.setStyleSheet(_fromUtf8(""))
        self.play_pauseButton.setText(_fromUtf8(""))
        self.play_pauseButton.setIconSize(QtCore.QSize(25, 25))
        self.play_pauseButton.setObjectName(_fromUtf8("play_pauseButton"))
        self.horizontalLayout_2.addWidget(self.play_pauseButton)
        self.stopButton = QtGui.QToolButton(self.centralwidget)
        self.stopButton.setEnabled(False)
        self.stopButton.setAutoFillBackground(False)
        self.stopButton.setStyleSheet(_fromUtf8(""))
        self.stopButton.setText(_fromUtf8(""))
        self.stopButton.setIconSize(QtCore.QSize(25, 25))
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.horizontalLayout_2.addWidget(self.stopButton)
        self.seekSlider = phonon.Phonon.SeekSlider(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.seekSlider.sizePolicy().hasHeightForWidth())
        self.seekSlider.setSizePolicy(sizePolicy)
        self.seekSlider.setIconVisible(False)
        self.seekSlider.setTracking(True)
        self.seekSlider.setIconSize(QtCore.QSize(16, 16))
        self.seekSlider.setObjectName(_fromUtf8("seekSlider"))
        self.horizontalLayout_2.addWidget(self.seekSlider)
        self.seekSlider.show()

        # range slider
        self.rangeSlider = RangeSlider(Qt.Qt.Horizontal)
        self.rangeSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.rangeSlider.setTickInterval(1)
        self.horizontalLayout_2.addWidget(self.rangeSlider)
        self.rangeSlider.hide()

        # analyze button
        self.analyzeButton = QtGui.QPushButton("Analyze", self)
        self.horizontalLayout_2.addWidget(self.analyzeButton)
        self.analyzeButton.hide()

        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 765, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuField = QtGui.QMenu(self.menubar)
        self.menuField.setObjectName(_fromUtf8("menuField"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad = QtGui.QAction(MainWindow)
        self.actionLoad.setObjectName(_fromUtf8("actionLoad"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionMy_playlist = QtGui.QAction(MainWindow)
        self.actionMy_playlist.setObjectName(_fromUtf8("actionMy_playlist"))
        self.actionAnalyze_Area = QtGui.QAction(MainWindow)
        self.actionAnalyze_Area.setObjectName(_fromUtf8("actionAnalyze_Area"))
        self.menuField.addAction(self.actionLoad)
        self.menuField.addSeparator()
        self.menuField.addAction(self.actionAnalyze_Area)
        self.menuField.addSeparator()
        self.menuField.addAction(self.actionExit)
        self.menubar.addAction(self.menuField.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "VFI Analysis", None))
        self.play_pauseButton.setToolTip(_translate("MainWindow", "Play", None))
        self.stopButton.setToolTip(_translate("MainWindow", "Stop", None))
        self.seekSlider.setToolTip(_translate("MainWindow", "Seek", None))
        self.rangeSlider.setToolTip(_translate("MainWindow", "Range", None))
        self.menuField.setTitle(_translate("MainWindow", "Action", None))
        self.menuView.setTitle(_translate("MainWindow", "Help", None))
        self.actionLoad.setText(_translate("MainWindow", "Load Video", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionMy_playlist.setText(_translate("MainWindow", "My_playlist", None))
        self.actionAnalyze_Area.setText(_translate("MainWindow", "Analyze Area", None))
