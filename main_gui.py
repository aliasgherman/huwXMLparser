# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_app.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1016, 917)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 1001, 71))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.frame_2)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 1001, 61))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.chkLatestDate = QtWidgets.QCheckBox(self.formLayoutWidget_2)
        self.chkLatestDate.setChecked(True)
        self.chkLatestDate.setObjectName("chkLatestDate")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.chkLatestDate)
        self.labProcessFileTodayDate = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.labProcessFileTodayDate.setObjectName("labProcessFileTodayDate")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labProcessFileTodayDate)
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setObjectName("formLayout_4")
        self.labCustomDate = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.labCustomDate.setObjectName("labCustomDate")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labCustomDate)
        self.txtCustomDate = QtWidgets.QPlainTextEdit(self.formLayoutWidget_2)
        self.txtCustomDate.setEnabled(False)
        self.txtCustomDate.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txtCustomDate.setObjectName("txtCustomDate")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtCustomDate)
        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.formLayout_4)
        self.formLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(0, 80, 1001, 243))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.labLocalDirectory = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.labLocalDirectory.setObjectName("labLocalDirectory")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labLocalDirectory)
        self.cmdSelLocalDir = QtWidgets.QCommandLinkButton(self.formLayoutWidget_3)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.cmdSelLocalDir.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.cmdSelLocalDir.setFont(font)
        self.cmdSelLocalDir.setAutoFillBackground(True)
        self.cmdSelLocalDir.setObjectName("cmdSelLocalDir")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cmdSelLocalDir)
        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setObjectName("formLayout_6")
        self.labExportParsed = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.labExportParsed.setObjectName("labExportParsed")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labExportParsed)
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setObjectName("formLayout_5")
        self.labExportDir = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.labExportDir.setObjectName("labExportDir")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labExportDir)
        self.labCompressFiles = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.labCompressFiles.setObjectName("labCompressFiles")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labCompressFiles)
        self.cmdSelExportDir = QtWidgets.QCommandLinkButton(self.formLayoutWidget_3)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.cmdSelExportDir.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.cmdSelExportDir.setFont(font)
        self.cmdSelExportDir.setAutoFillBackground(True)
        self.cmdSelExportDir.setObjectName("cmdSelExportDir")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cmdSelExportDir)
        self.chkCompressFiles = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.chkCompressFiles.setChecked(True)
        self.chkCompressFiles.setObjectName("chkCompressFiles")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.chkCompressFiles)
        self.formLayout_9 = QtWidgets.QFormLayout()
        self.formLayout_9.setObjectName("formLayout_9")
        self.txt7zLoc = QtWidgets.QPlainTextEdit(self.formLayoutWidget_3)
        self.txt7zLoc.setMaximumSize(QtCore.QSize(65535, 30))
        self.txt7zLoc.setInputMethodHints(QtCore.Qt.ImhNone)
        self.txt7zLoc.setObjectName("txt7zLoc")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txt7zLoc)
        self.formLayout_5.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.formLayout_9)
        self.labLocation7z = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.labLocation7z.setEnabled(True)
        self.labLocation7z.setMaximumSize(QtCore.QSize(200, 30))
        self.labLocation7z.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        self.labLocation7z.setTextFormat(QtCore.Qt.PlainText)
        self.labLocation7z.setWordWrap(True)
        self.labLocation7z.setObjectName("labLocation7z")
        self.formLayout_5.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.labLocation7z)
        self.labExportDIrVal = QtWidgets.QLabel(self.formLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.labExportDIrVal.setFont(font)
        self.labExportDIrVal.setObjectName("labExportDIrVal")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.labExportDIrVal)
        self.formLayout_6.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.formLayout_5)
        self.chkExportCSV = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.chkExportCSV.setChecked(True)
        self.chkExportCSV.setObjectName("chkExportCSV")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.chkExportCSV)
        self.formLayout_3.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.formLayout_6)
        self.labImportToMongo = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.labImportToMongo.setObjectName("labImportToMongo")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.labImportToMongo)
        self.chkImportToMongo = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.chkImportToMongo.setChecked(True)
        self.chkImportToMongo.setObjectName("chkImportToMongo")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.chkImportToMongo)
        self.labLocalDirValue = QtWidgets.QLabel(self.formLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.labLocalDirValue.setFont(font)
        self.labLocalDirValue.setObjectName("labLocalDirValue")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.labLocalDirValue)
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 460, 1001, 341))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.labDownloadFTP = QtWidgets.QLabel(self.formLayoutWidget)
        self.labDownloadFTP.setObjectName("labDownloadFTP")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labDownloadFTP)
        self.chkDownloadFromFTP = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.chkDownloadFromFTP.setObjectName("chkDownloadFromFTP")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.chkDownloadFromFTP)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.labFTP1IP = QtWidgets.QLabel(self.formLayoutWidget)
        self.labFTP1IP.setEnabled(False)
        self.labFTP1IP.setObjectName("labFTP1IP")
        self.horizontalLayout_5.addWidget(self.labFTP1IP)
        self.txtFTP1IP = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.txtFTP1IP.setEnabled(False)
        self.txtFTP1IP.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txtFTP1IP.setInputMethodHints(QtCore.Qt.ImhNone)
        self.txtFTP1IP.setObjectName("txtFTP1IP")
        self.horizontalLayout_5.addWidget(self.txtFTP1IP)
        self.labFTP1U = QtWidgets.QLabel(self.formLayoutWidget)
        self.labFTP1U.setEnabled(False)
        self.labFTP1U.setObjectName("labFTP1U")
        self.horizontalLayout_5.addWidget(self.labFTP1U)
        self.txtFTP1User = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.txtFTP1User.setEnabled(False)
        self.txtFTP1User.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txtFTP1User.setInputMethodHints(QtCore.Qt.ImhNone)
        self.txtFTP1User.setObjectName("txtFTP1User")
        self.horizontalLayout_5.addWidget(self.txtFTP1User)
        self.labFTP1P = QtWidgets.QLabel(self.formLayoutWidget)
        self.labFTP1P.setEnabled(False)
        self.labFTP1P.setObjectName("labFTP1P")
        self.horizontalLayout_5.addWidget(self.labFTP1P)
        self.txtFTP1Pwd = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.txtFTP1Pwd.setEnabled(False)
        self.txtFTP1Pwd.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txtFTP1Pwd.setInputMethodHints(QtCore.Qt.ImhSensitiveData)
        self.txtFTP1Pwd.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.txtFTP1Pwd.setMaximumBlockCount(0)
        self.txtFTP1Pwd.setObjectName("txtFTP1Pwd")
        self.horizontalLayout_5.addWidget(self.txtFTP1Pwd)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.labFTP2IP = QtWidgets.QLabel(self.formLayoutWidget)
        self.labFTP2IP.setEnabled(False)
        self.labFTP2IP.setObjectName("labFTP2IP")
        self.horizontalLayout_6.addWidget(self.labFTP2IP)
        self.txtFTP2IP = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.txtFTP2IP.setEnabled(False)
        self.txtFTP2IP.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txtFTP2IP.setInputMethodHints(QtCore.Qt.ImhNone)
        self.txtFTP2IP.setObjectName("txtFTP2IP")
        self.horizontalLayout_6.addWidget(self.txtFTP2IP)
        self.labFTP2U = QtWidgets.QLabel(self.formLayoutWidget)
        self.labFTP2U.setEnabled(False)
        self.labFTP2U.setObjectName("labFTP2U")
        self.horizontalLayout_6.addWidget(self.labFTP2U)
        self.txtFTP2User = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.txtFTP2User.setEnabled(False)
        self.txtFTP2User.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txtFTP2User.setInputMethodHints(QtCore.Qt.ImhNone)
        self.txtFTP2User.setObjectName("txtFTP2User")
        self.horizontalLayout_6.addWidget(self.txtFTP2User)
        self.labFTP2P = QtWidgets.QLabel(self.formLayoutWidget)
        self.labFTP2P.setEnabled(False)
        self.labFTP2P.setObjectName("labFTP2P")
        self.horizontalLayout_6.addWidget(self.labFTP2P)
        self.txtFTP2Pwd = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.txtFTP2Pwd.setEnabled(False)
        self.txtFTP2Pwd.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txtFTP2Pwd.setInputMethodHints(QtCore.Qt.ImhSensitiveData)
        self.txtFTP2Pwd.setObjectName("txtFTP2Pwd")
        self.horizontalLayout_6.addWidget(self.txtFTP2Pwd)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.labFTP3IP = QtWidgets.QLabel(self.formLayoutWidget)
        self.labFTP3IP.setEnabled(False)
        self.labFTP3IP.setObjectName("labFTP3IP")
        self.horizontalLayout_4.addWidget(self.labFTP3IP)
        self.txtFTP3IP = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.txtFTP3IP.setEnabled(False)
        self.txtFTP3IP.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txtFTP3IP.setInputMethodHints(QtCore.Qt.ImhNone)
        self.txtFTP3IP.setObjectName("txtFTP3IP")
        self.horizontalLayout_4.addWidget(self.txtFTP3IP)
        self.labFTP3U = QtWidgets.QLabel(self.formLayoutWidget)
        self.labFTP3U.setEnabled(False)
        self.labFTP3U.setObjectName("labFTP3U")
        self.horizontalLayout_4.addWidget(self.labFTP3U)
        self.txtFTP3User = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.txtFTP3User.setEnabled(False)
        self.txtFTP3User.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txtFTP3User.setInputMethodHints(QtCore.Qt.ImhNone)
        self.txtFTP3User.setObjectName("txtFTP3User")
        self.horizontalLayout_4.addWidget(self.txtFTP3User)
        self.labFTP3P = QtWidgets.QLabel(self.formLayoutWidget)
        self.labFTP3P.setEnabled(False)
        self.labFTP3P.setObjectName("labFTP3P")
        self.horizontalLayout_4.addWidget(self.labFTP3P)
        self.txtFTP3Pwd = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.txtFTP3Pwd.setEnabled(False)
        self.txtFTP3Pwd.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txtFTP3Pwd.setInputMethodHints(QtCore.Qt.ImhSensitiveData)
        self.txtFTP3Pwd.setObjectName("txtFTP3Pwd")
        self.horizontalLayout_4.addWidget(self.txtFTP3Pwd)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.verticalLayout)
        self.labParseFiles = QtWidgets.QLabel(self.formLayoutWidget)
        self.labParseFiles.setObjectName("labParseFiles")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labParseFiles)
        self.chkParseFromLocal = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.chkParseFromLocal.setChecked(True)
        self.chkParseFromLocal.setObjectName("chkParseFromLocal")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.chkParseFromLocal)
        self.labExportFromMongo = QtWidgets.QLabel(self.formLayoutWidget)
        self.labExportFromMongo.setObjectName("labExportFromMongo")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.labExportFromMongo)
        self.chkExportFromMongo = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.chkExportFromMongo.setObjectName("chkExportFromMongo")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.chkExportFromMongo)
        self.formLayout_8 = QtWidgets.QFormLayout()
        self.formLayout_8.setObjectName("formLayout_8")
        self.labExportLatestMongoOnly = QtWidgets.QLabel(self.formLayoutWidget)
        self.labExportLatestMongoOnly.setEnabled(False)
        self.labExportLatestMongoOnly.setObjectName("labExportLatestMongoOnly")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labExportLatestMongoOnly)
        self.chkExportLatestOnly = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.chkExportLatestOnly.setEnabled(False)
        self.chkExportLatestOnly.setChecked(True)
        self.chkExportLatestOnly.setObjectName("chkExportLatestOnly")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.chkExportLatestOnly)
        self.labMongoDBName = QtWidgets.QLabel(self.formLayoutWidget)
        self.labMongoDBName.setEnabled(False)
        self.labMongoDBName.setObjectName("labMongoDBName")
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labMongoDBName)
        self.txtMongoDB = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.txtMongoDB.setEnabled(False)
        self.txtMongoDB.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txtMongoDB.setObjectName("txtMongoDB")
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtMongoDB)
        self.txtMongoMO = QtWidgets.QPlainTextEdit(self.formLayoutWidget)
        self.txtMongoMO.setEnabled(False)
        self.txtMongoMO.setObjectName("txtMongoMO")
        self.formLayout_8.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txtMongoMO)
        self.labMongoMOName = QtWidgets.QLabel(self.formLayoutWidget)
        self.labMongoMOName.setEnabled(False)
        self.labMongoMOName.setTextFormat(QtCore.Qt.PlainText)
        self.labMongoMOName.setObjectName("labMongoMOName")
        self.formLayout_8.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labMongoMOName)
        self.formLayout.setLayout(4, QtWidgets.QFormLayout.FieldRole, self.formLayout_8)
        self.cmdRun = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.cmdRun.setGeometry(QtCore.QRect(810, 810, 191, 41))
        self.cmdRun.setObjectName("cmdRun")
        self.formLayoutWidget_7 = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget_7.setGeometry(QtCore.QRect(0, 340, 1001, 104))
        self.formLayoutWidget_7.setObjectName("formLayoutWidget_7")
        self.formLayout_7 = QtWidgets.QFormLayout(self.formLayoutWidget_7)
        self.formLayout_7.setContentsMargins(0, 0, 0, 0)
        self.formLayout_7.setObjectName("formLayout_7")
        self.labMongoPort = QtWidgets.QLabel(self.formLayoutWidget_7)
        self.labMongoPort.setObjectName("labMongoPort")
        self.formLayout_7.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labMongoPort)
        self.txtMongoPort = QtWidgets.QPlainTextEdit(self.formLayoutWidget_7)
        self.txtMongoPort.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txtMongoPort.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.txtMongoPort.setObjectName("txtMongoPort")
        self.formLayout_7.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txtMongoPort)
        self.txtMongoPwd = QtWidgets.QTextEdit(self.formLayoutWidget_7)
        self.txtMongoPwd.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txtMongoPwd.setInputMethodHints(QtCore.Qt.ImhNone)
        self.txtMongoPwd.setAcceptRichText(False)
        self.txtMongoPwd.setObjectName("txtMongoPwd")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtMongoPwd)
        self.txtMongoUser = QtWidgets.QTextEdit(self.formLayoutWidget_7)
        self.txtMongoUser.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txtMongoUser.setInputMethodHints(QtCore.Qt.ImhNone)
        self.txtMongoUser.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.txtMongoUser.setAcceptRichText(False)
        self.txtMongoUser.setObjectName("txtMongoUser")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtMongoUser)
        self.labMongoUser = QtWidgets.QLabel(self.formLayoutWidget_7)
        self.labMongoUser.setObjectName("labMongoUser")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labMongoUser)
        self.labMongoPwd = QtWidgets.QLabel(self.formLayoutWidget_7)
        self.labMongoPwd.setObjectName("labMongoPwd")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labMongoPwd)
        self.frame_2.raise_()
        self.labExportParsed.raise_()
        self.chkExportCSV.raise_()
        self.labProcessFileTodayDate.raise_()
        self.labCustomDate.raise_()
        self.chkExportCSV.raise_()
        self.formLayoutWidget_3.raise_()
        self.formLayoutWidget.raise_()
        self.cmdRun.raise_()
        self.formLayoutWidget_7.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1016, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.chkLatestDate, self.txtCustomDate)
        MainWindow.setTabOrder(self.txtCustomDate, self.cmdSelLocalDir)
        MainWindow.setTabOrder(self.cmdSelLocalDir, self.chkExportCSV)
        MainWindow.setTabOrder(self.chkExportCSV, self.cmdSelExportDir)
        MainWindow.setTabOrder(self.cmdSelExportDir, self.chkCompressFiles)
        MainWindow.setTabOrder(self.chkCompressFiles, self.txt7zLoc)
        MainWindow.setTabOrder(self.txt7zLoc, self.chkImportToMongo)
        MainWindow.setTabOrder(self.chkImportToMongo, self.chkDownloadFromFTP)
        MainWindow.setTabOrder(self.chkDownloadFromFTP, self.txtFTP1IP)
        MainWindow.setTabOrder(self.txtFTP1IP, self.txtFTP1User)
        MainWindow.setTabOrder(self.txtFTP1User, self.txtFTP1Pwd)
        MainWindow.setTabOrder(self.txtFTP1Pwd, self.txtFTP2IP)
        MainWindow.setTabOrder(self.txtFTP2IP, self.txtFTP2User)
        MainWindow.setTabOrder(self.txtFTP2User, self.txtFTP2Pwd)
        MainWindow.setTabOrder(self.txtFTP2Pwd, self.txtFTP3IP)
        MainWindow.setTabOrder(self.txtFTP3IP, self.txtFTP3User)
        MainWindow.setTabOrder(self.txtFTP3User, self.txtFTP3Pwd)
        MainWindow.setTabOrder(self.txtFTP3Pwd, self.chkParseFromLocal)
        MainWindow.setTabOrder(self.chkParseFromLocal, self.chkExportFromMongo)
        MainWindow.setTabOrder(self.chkExportFromMongo, self.chkExportLatestOnly)
        MainWindow.setTabOrder(self.chkExportLatestOnly, self.txtMongoDB)
        MainWindow.setTabOrder(self.txtMongoDB, self.txtMongoMO)
        MainWindow.setTabOrder(self.txtMongoMO, self.cmdRun)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.chkLatestDate.setText(_translate("MainWindow", "Process Files for Today\'s Date"))
        self.labProcessFileTodayDate.setText(_translate("MainWindow", "Only process today\'s dated files"))
        self.labCustomDate.setText(_translate("MainWindow", "Custom Date if Today\'s date not needed"))
        self.txtCustomDate.setPlainText(_translate("MainWindow", "20190522"))
        self.labLocalDirectory.setText(_translate("MainWindow", "Local Directory for XML Files"))
        self.cmdSelLocalDir.setText(_translate("MainWindow", "Select Local Directory"))
        self.labExportParsed.setText(_translate("MainWindow", "Export Parsed Dump to CSV"))
        self.labExportDir.setText(_translate("MainWindow", "Local Directory for Dump Export"))
        self.labCompressFiles.setText(_translate("MainWindow", "Compress Exported Files"))
        self.cmdSelExportDir.setText(_translate("MainWindow", "Select File Export Directory"))
        self.chkCompressFiles.setText(_translate("MainWindow", "Compress Exported Files (Requires 7zip)"))
        self.txt7zLoc.setPlainText(_translate("MainWindow", "7z"))
        self.labLocation7z.setText(
            _translate("MainWindow", "Location of 7z (Like \"C:\\Program Files\\7z\\7z.exe\" or /usr/share/7z"))
        self.labExportDIrVal.setText(_translate("MainWindow", "Export Dir : Not Set"))
        self.chkExportCSV.setText(_translate("MainWindow", "Export to CSV (Not Recommended if XML count is high)"))
        self.labImportToMongo.setText(_translate("MainWindow", "Import Dumps to Mongo DB"))
        self.chkImportToMongo.setText(_translate("MainWindow", "Import to Mongo (Requires Mongo daemon running)"))
        self.labLocalDirValue.setText(_translate("MainWindow", "Local Dir : Not Set"))
        self.labDownloadFTP.setText(_translate("MainWindow", "Download AUTOBAK Files ?"))
        self.chkDownloadFromFTP.setText(_translate("MainWindow", "Download Dumps from FTP"))
        self.labFTP1IP.setText(_translate("MainWindow", "FTP1 IP:PORT"))
        self.txtFTP1IP.setPlainText(_translate("MainWindow", "10.200.163.7"))
        self.labFTP1U.setText(_translate("MainWindow", "FTP1:User"))
        self.txtFTP1User.setPlainText(_translate("MainWindow", "ftpuser"))
        self.labFTP1P.setText(_translate("MainWindow", "FTP1Pass"))
        self.txtFTP1Pwd.setPlainText(_translate("MainWindow", "PWD_1"))
        self.labFTP2IP.setText(_translate("MainWindow", "FTP2 IP:PORT"))
        self.txtFTP2IP.setPlainText(_translate("MainWindow", "10.200.163.15"))
        self.labFTP2U.setText(_translate("MainWindow", "FTP2:User"))
        self.txtFTP2User.setPlainText(_translate("MainWindow", "ftpuser"))
        self.labFTP2P.setText(_translate("MainWindow", "FTP2Pass"))
        self.txtFTP2Pwd.setPlainText(_translate("MainWindow", "PWD_2"))
        self.labFTP3IP.setText(_translate("MainWindow", "FTP3 IP:PORT"))
        self.labFTP3U.setText(_translate("MainWindow", "FTP3:User"))
        self.labFTP3P.setText(_translate("MainWindow", "FTP3Pass"))
        self.labParseFiles.setText(_translate("MainWindow", "Parse Files in Local Directory ?"))
        self.chkParseFromLocal.setText(_translate("MainWindow", "Parse Dumps from Local Directory"))
        self.labExportFromMongo.setText(_translate("MainWindow", "Export Existing / Parsed Dumps from Mongo ?"))
        self.chkExportFromMongo.setText(_translate("MainWindow", "Export Dumps from Mongo"))
        self.labExportLatestMongoOnly.setText(
            _translate("MainWindow", "Export Latest Date from Mongo Only (Else will export all dates in Mongo)"))
        self.chkExportLatestOnly.setText(_translate("MainWindow", "Export Latest Dump"))
        self.labMongoDBName.setText(
            _translate("MainWindow", "DB Name to Export From (Like BTS3900 or 1-BTS59005G) etc"))
        self.txtMongoDB.setPlainText(_translate("MainWindow", "1-BSC6910"))
        self.txtMongoMO.setPlainText(_translate("MainWindow", "\"NE\", \"TZ\", \"UFRC\", \"UCELL\""))
        self.labMongoMOName.setText(
            _translate("MainWindow", "MOs to Export (Like \"NE\", \"TZ\", \"UCELL\", \"UFRC\")"))
        self.cmdRun.setText(_translate("MainWindow", "Run Program"))
        self.labMongoPort.setText(_translate("MainWindow", "Mongo Port"))
        self.txtMongoPort.setPlainText(_translate("MainWindow", "localhost:27017"))
        self.labMongoUser.setText(_translate("MainWindow", "Mongo User (Usually Blank)"))
        self.labMongoPwd.setText(_translate("MainWindow", "Mongo Password (Usually Blank)"))

    def openFoldoerChooser(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName = QFileDialog.getExistingDirectory(parent=None, caption="Save File Name", options=options)
        if os.path.exists(fileName):
            return fileName
        else:
            return False

    def cmdSelLocalDir_click(self, btn):
        print(btn.text())
        localDir = self.openFoldoerChooser()
        if localDir != False:
            self.cmdSelLocalDir.setAutoFillBackground(False)  # change the background to show that local dir is set now
            self.labLocalDirValue.setText(localDir)
        else:
            self.cmdSelLocalDir.setAutoFillBackground(True)  # change the background to show that local dir is set now
            self.labLocalDirValue.setText("Local Dir : Not Set")

    def cmdSelExportDir_click(self, btn):
        print(btn.text())
        exportDir = self.openFoldoerChooser()
        if exportDir != False:
            self.cmdSelExportDir.setAutoFillBackground(False)  # change the background to show that local dir is set now
            self.labExportDIrVal.setText(exportDir)
        else:
            self.cmdSelExportDir.setAutoFillBackground(True)  # change the background to show that local dir is set now
            self.labExportDIrVal.setText("Export Dir : Not Set")

    def assignFunctions(self):
        # Assign a common function for all checkboxes

        self.chkImportToMongo.stateChanged.connect(lambda: self.chkImportToMongo_changed(self.chkImportToMongo))
        self.chkExportLatestOnly.stateChanged.connect(
            lambda: self.chkExportLatestOnly_changed(self.chkExportLatestOnly))
        self.chkExportCSV.stateChanged.connect(lambda: self.chkExportCSV_changed(self.chkExportCSV))
        self.chkCompressFiles.stateChanged.connect(lambda: self.chkCompressFiles_changed(self.chkCompressFiles))
        self.chkLatestDate.stateChanged.connect(lambda: self.chkLatestDate_changed(self.chkLatestDate))
        self.chkDownloadFromFTP.stateChanged.connect(lambda: self.chkDownloadFromFTP_changed(self.chkDownloadFromFTP))
        self.chkExportFromMongo.stateChanged.connect(lambda: self.chkExportFromMongo_changed(self.chkExportFromMongo))
        self.chkParseFromLocal.stateChanged.connect(lambda: self.chkParseFromLocal_changed(self.chkParseFromLocal))
        self.cmdSelLocalDir.clicked.connect(lambda: self.cmdSelLocalDir_click(self.cmdSelLocalDir))
        self.cmdSelExportDir.clicked.connect(lambda: self.cmdSelExportDir_click(self.cmdSelExportDir))
        self.cmdRun.clicked.connect(lambda: self.cmdRun_click(self.cmdRun))

    def cmdRun_click(self, btn):
        todayDate = ""
        HOST_LIST = []
        alert = QMessageBox()
        LOCALFOLDER = ""
        EXPORT_PATH = ""
        ZIP_EXPORT_PATH = ""
        TABLES_TO_EXPORT = []
        finalCommand = ""
        FOL_LIST = ["BTS3900", "BTS3900 LTE", "BTS5900 5G", "BTS5900 LTE", "PICO BTS3900", "DBS3900 IBS",
                    "MICRO BTS3900"]  # These are the folder names on the FTP servers where you have the XML files.

        if self.chkLatestDate.isChecked():
            todayDate = datetime.now()
            todayDate = "{:04d}{:02d}{:02d}".format(todayDate.year, todayDate.month, todayDate.day)
        else:
            todayDate = self.txtCustomDate.toPlainText()
            date_format = "%Y%m%d"
            try:
                datetime.strptime(todayDate, date_format)
            except ValueError:
                myErr = "The enterede date seems invalid. Format should be YYYYMMDD (like 20190530)"
                print(myErr)
                alert.setText(myErr)
                alert.exec_()
                return
        print("Selected date for processing is ", todayDate)

        if self.chkDownloadFromFTP.isChecked():
            if self.txtFTP1User.toPlainText() != "" and self.txtFTP1Pwd.toPlainText() != "" and self.txtFTP1IP.toPlainText() != "":
                # we may have a valid FTP1 server
                HOST_LIST.append(
                    [self.txtFTP1IP.toPlainText(), self.txtFTP1User.toPlainText(), self.txtFTP1Pwd.toPlainText()])
            if self.txtFTP2User.toPlainText() != "" and self.txtFTP2Pwd.toPlainText() != "" and self.txtFTP2IP.toPlainText() != "":
                # we may have a valid FTP1 server
                HOST_LIST.append(
                    [self.txtFTP2IP.toPlainText(), self.txtFTP2User.toPlainText(), self.txtFTP2Pwd.toPlainText()])
            if self.txtFTP3User.toPlainText() != "" and self.txtFTP3Pwd.toPlainText() != "" and self.txtFTP3IP.toPlainText() != "":
                # we may have a valid FTP1 server
                HOST_LIST.append(
                    [self.txtFTP3IP.toPlainText(), self.txtFTP3User.toPlainText(), self.txtFTP3Pwd.toPlainText()])
            print("HOST_LIST is ", HOST_LIST)

        if self.chkDownloadFromFTP.isChecked() or self.chkParseFromLocal.isChecked():
            if os.path.exists(self.labLocalDirValue.text()) == False:
                alert.setText(
                    "Please press the button to select the local directory where the XML files should be downloaded / present for parsing.")
                alert.exec_()
                return
            else:
                LOCALFOLDER = self.labLocalDirValue.text()
                print("Local folder is ", LOCALFOLDER)

        if self.chkParseFromLocal.isChecked() or self.chkExportFromMongo.isChecked():
            if os.path.exists(self.labExportDIrVal.text()) == False:
                alert.setText("Please select a valid directory to export files using the button provided.")
                alert.exec_()
                return
            else:
                EXPORT_PATH = os.path.join(self.labExportDIrVal.text(), todayDate)
                ZIP_EXPORT_PATH = os.path.join(self.labExportDIrVal.text(), todayDate + ".7z")
                print("Export path is ", EXPORT_PATH)
        if self.chkParseFromLocal.isChecked() == False and self.chkExportFromMongo.isChecked() == False and self.chkDownloadFromFTP.isChecked() == False:
            alert.setText("Please select atleast 1 step. (Download from FTP, or Parse Files or Export from Mongo.).")
            alert.exec_()
            return
        if self.chkExportFromMongo.isChecked():
            if self.txtMongoDB.toPlainText().strip() == "":
                alert.setText("Please enter a valid DB Name for export from Mongo DB")
                alert.exec_()
                return
            if self.txtMongoMO.toPlainText().strip() == "":
                alert.setText(
                    "We will export all MOs as no MO Names are specified. This could be slow depending on the amount of data.")
                alert.exec_()
                TABLES_TO_EXPORT = []
            else:
                cleanedMO = self.txtMongoMO.toPlainText().strip().replace("'", "").replace('"', '')
                cleanedMO = cleanedMO.split(",")
                for indivMO in cleanedMO:
                    TABLES_TO_EXPORT.append(indivMO.strip())
            print("Tables to export are :", TABLES_TO_EXPORT)

        if self.chkCompressFiles.isChecked():
            if self.txt7zLoc.toPlainText().strip() != "":
                finalCommand = r'"{}" a "{}" -r "{}" -mx=9'.format(self.txt7zLoc.toPlainText().strip(), ZIP_EXPORT_PATH,
                                                                   EXPORT_PATH)
                self.myLogger.info("The final command is selected to be " + finalCommand)
            else:
                alert.setText("Please enter the location of 7z utility to compress files. ")
                alert.exec_()
                return

        if self.chkDownloadFromFTP.isChecked() == True:
            downloader = XMLDownloader(self.myLogger, PATHFILTER=todayDate,
                                       HOST_LIST=HOST_LIST, FOL_LIST=FOL_LIST,
                                       LOCALFOLDER=LOCALFOLDER, type=XMLDownloader.AUTOBAK)
            downloader.run()

        if self.chkParseFromLocal.isChecked() == True:
            parserXML = ParserXML(logger=self.myLogger, CUSTOM_DATE_FILTER=todayDate,
                                  EXPORT_CSV=self.chkExportCSV.isChecked(),
                                  INSERT_MONGO=self.chkImportToMongo.isChecked(),
                                  DUMPDIR=LOCALFOLDER,
                                  EXPORT_DIR=EXPORT_PATH)
            parserXML.run()
            if self.chkExportCSV.isChecked() == True:
                if self.chkCompressFiles.isChecked() == True:
                    self.myLogger.info(
                        finalCommand)  # This is the command to combine the processed CSV files into a single 7z file
                    subprocess.call(finalCommand, shell=True)

        if self.chkExportFromMongo.isChecked() == True:
            exporter = MongoToExcel(logger=myLogger, DBNAME=self.txtMongoDB, EXPORT_PATH=EXPORT_PATH,
                                    TABLES_NEEDED=TABLES_TO_EXPORT, DATE_COLUMN="AAMDATE",
                                    EXPORT_ALL_DATES=(self.chkExportLatestOnly.isChecked() == False),
                                    COLUMNS_TO_DROP=['_id'], TABLE_FOR_MAXDATE="TZ",
                                    MONGO_USER=self.txtMongoUser.toPlainText(),
                                    MONGO_PWD=self.txtMongoPwd.toPlainText(),
                                    MONGO_PORT=self.txtMongoPort.toPlainText())
            exporter.run()

    def chkImportToMongo_changed(self, chk):
        print("Change event detected for ", chk.text(), chk.isChecked(), chk)

    def chkExportLatestOnly_changed(self, chk):
        print("Change event detected for ", chk.text(), chk.isChecked(), chk)

    def chkExportCSV_changed(self, chk):
        if chk.isChecked():
            self.cmdSelExportDir.setEnabled(True)
            self.chkCompressFiles.setEnabled(True)
            self.labExportDir.setEnabled(True)
            self.labCompressFiles.setEnabled(True)
            if self.chkCompressFiles.isChecked():
                self.txt7zLoc.setEnabled(True)
                self.labLocation7z.setEnabled(True)
            else:
                self.txt7zLoc.setEnabled(False)
                self.labLocation7z.setEnabled(False)
        else:
            self.cmdSelExportDir.setEnabled(False)
            self.chkCompressFiles.setEnabled(False)
            self.txt7zLoc.setEnabled(False)
            self.labExportDir.setEnabled(False)
            self.labCompressFiles.setEnabled(False)
            self.labLocation7z.setEnabled(False)
        print("Change event detected for ", chk.text(), chk.isChecked(), chk)

    def chkCompressFiles_changed(self, chk):
        if self.chkCompressFiles.isChecked():
            self.txt7zLoc.setEnabled(True)
            self.labLocation7z.setEnabled(True)
        else:
            self.txt7zLoc.setEnabled(False)
            self.labLocation7z.setEnabled(False)
        print("Change event detected for ", chk.text(), chk.isChecked(), chk)

    def chkLatestDate_changed(self, chk):
        if chk.isChecked():
            self.txtCustomDate.setEnabled(False)
        else:
            self.txtCustomDate.setEnabled(True)
        print("Change event detected for ", chk.text(), chk.isChecked(), chk)

    def chkDownloadFromFTP_changed(self, chk):
        if chk.isChecked():
            self.labFTP1IP.setEnabled(True)
            self.labFTP2IP.setEnabled(True)
            self.labFTP3IP.setEnabled(True)
            self.labFTP1U.setEnabled(True)
            self.labFTP2U.setEnabled(True)
            self.labFTP3U.setEnabled(True)
            self.labFTP1P.setEnabled(True)
            self.labFTP2P.setEnabled(True)
            self.labFTP3P.setEnabled(True)
            self.txtFTP1IP.setEnabled(True)
            self.txtFTP2IP.setEnabled(True)
            self.txtFTP3IP.setEnabled(True)
            self.txtFTP1User.setEnabled(True)
            self.txtFTP2User.setEnabled(True)
            self.txtFTP3User.setEnabled(True)
            self.txtFTP1Pwd.setEnabled(True)
            self.txtFTP2Pwd.setEnabled(True)
            self.txtFTP3Pwd.setEnabled(True)
        else:
            self.labFTP1IP.setEnabled(False)
            self.labFTP2IP.setEnabled(False)
            self.labFTP3IP.setEnabled(False)
            self.labFTP1U.setEnabled(False)
            self.labFTP2U.setEnabled(False)
            self.labFTP3U.setEnabled(False)
            self.labFTP1P.setEnabled(False)
            self.labFTP2P.setEnabled(False)
            self.labFTP3P.setEnabled(False)
            self.txtFTP1IP.setEnabled(False)
            self.txtFTP2IP.setEnabled(False)
            self.txtFTP3IP.setEnabled(False)
            self.txtFTP1User.setEnabled(False)
            self.txtFTP2User.setEnabled(False)
            self.txtFTP3User.setEnabled(False)
            self.txtFTP1Pwd.setEnabled(False)
            self.txtFTP2Pwd.setEnabled(False)
            self.txtFTP3Pwd.setEnabled(False)
        print("Change event detected for ", chk.text(), chk.isChecked(), chk)

    def chkExportFromMongo_changed(self, chk):
        if chk.isChecked():
            self.labExportLatestMongoOnly.setEnabled(True)
            self.labMongoDBName.setEnabled(True)
            self.labMongoMOName.setEnabled(True)
            self.txtMongoDB.setEnabled(True)
            self.txtMongoMO.setEnabled(True)
            self.chkExportLatestOnly.setEnabled(True)
        else:
            self.labExportLatestMongoOnly.setEnabled(False)
            self.labMongoDBName.setEnabled(False)
            self.labMongoMOName.setEnabled(False)
            self.txtMongoDB.setEnabled(False)
            self.txtMongoMO.setEnabled(False)
            self.chkExportLatestOnly.setEnabled(False)
        print("Change event detected for ", chk.text(), chk.isChecked(), chk)

    def chkParseFromLocal_changed(self, chk):
        print("Change event detected for ", chk.text(), chk.isChecked(), chk)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QFileDialog, QMessageBox
    from datetime import datetime
    from downloadAutobak import *
    from exportToExcel import *
    from loggersetup import *
    from parserxml import *
    import subprocess

    loggingClass = LoggerSetup(TAG="XML_PARSER", MAX_FILE_SIZE=1024 * 1024 * 20, BACKUP_COUNT=20,
                               FILE_LOG_LEVEL=logging.DEBUG, CONSOLE_LOG_LEVEL=logging.DEBUG)
    myLogger = loggingClass.run()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.myLogger = myLogger
    ui.assignFunctions()
    MainWindow.show()
    sys.exit(app.exec_())
