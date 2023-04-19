
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Signal
from threading import Thread
import socket
import requests
import math
import vlccontroller
from PySide2.QtCore import Slot
import os

class JoinMenu_Ui(object):
    def setupUi(self, Form):
        self.client = Client()
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 75, -1, 75)
        self.verticalLayout.setObjectName("verticalLayout")
        self.NameLabel = QtWidgets.QLabel(Form)
        self.NameLabel.setObjectName("NameLabel")
        self.verticalLayout.addWidget(self.NameLabel)
        self.nameInput = QtWidgets.QLineEdit(Form)
        self.nameInput.setObjectName("nameInput")
        self.verticalLayout.addWidget(self.nameInput)
        self.IpLabel = QtWidgets.QLabel(Form)
        self.IpLabel.setObjectName("IpLabel")
        self.verticalLayout.addWidget(self.IpLabel)
        self.ipInput = QtWidgets.QLineEdit(Form)
        self.ipInput.setObjectName("ipInput")
        self.verticalLayout.addWidget(self.ipInput)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.JoinButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.JoinButton.sizePolicy().hasHeightForWidth())
        self.JoinButton.setSizePolicy(sizePolicy)
        self.JoinButton.setObjectName("JoinButton")
        self.JoinButton.clicked.connect(self.joinButtonAction)
        self.verticalLayout_2.addWidget(self.JoinButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def joinButtonAction(self):
        print("clicked")
        self.client.name = self.nameInput.text()
        self.client.connect(self.ipInput.text())

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.NameLabel.setText(_translate("Form", "Name:"))
        self.IpLabel.setText(_translate("Form", "Ip:"))
        self.JoinButton.setText(_translate("Form", "Join"))


class ClientMenu_Ui(QtWidgets.QWidget):
    start_signal = Signal(str)
    play_signal = Signal()
    pause_signal = Signal()

    def setupUi(self, Dialog):
        self.client: Client
        Dialog.setObjectName("Dialog")
        Dialog.resize(661, 387)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(0, 120, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 9, 0, 1, 1)
        self.downloadProgress = QtWidgets.QProgressBar(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadProgress.sizePolicy().hasHeightForWidth())
        self.downloadProgress.setSizePolicy(sizePolicy)
        self.downloadProgress.setObjectName("downloadProgress")
        self.downloadProgress.setMaximumSize(340, 21)
        self.setProgress(0)
        self.gridLayout.addWidget(self.downloadProgress, 4, 0, 1, 1)
        self.statusLabel = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusLabel.sizePolicy().hasHeightForWidth())
        self.statusLabel.setSizePolicy(sizePolicy)
        self.statusLabel.setStyleSheet("color: rgb(0, 0, 0);")
        self.statusLabel.setObjectName("statusLabel")
        self.statusLabel.setMaximumWidth(48)
        self.gridLayout.addWidget(self.statusLabel, 4, 1, 1, 1)
        self.movieName = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.movieName.setFont(font)
        self.movieName.setStyleSheet("color: rgb(255, 0, 0);")
        self.movieName.setMaximumWidth(340)
        self.movieName.setText("")
        self.movieName.setObjectName("movieName")
        self.gridLayout.addWidget(self.movieName, 2, 0, 1, 1)
        self.listView = QtWidgets.QListView(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setMinimumSize(QtCore.QSize(120, 138))
        self.listView.setMaximumSize(QtCore.QSize(120, 138))
        self.listView.setAcceptDrops(False)
        self.listView.setGridSize(QtCore.QSize(0, 0))
        self.listView.setItemAlignment(QtCore.Qt.AlignLeading)
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 1, 10, 1, 1)
        self.participantsLabel = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.participantsLabel.setFont(font)
        self.participantsLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.participantsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.participantsLabel.setObjectName("participantsLabel")
        self.gridLayout.addWidget(self.participantsLabel, 0, 10, 1, 1)
        self.leaveButton = QtWidgets.QPushButton(Dialog)
        self.leaveButton.setObjectName("leaveButton")
        self.gridLayout.addWidget(self.leaveButton, 11, 10, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(175, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 9, 1, 1)
        self.downloadButton = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadButton.sizePolicy().hasHeightForWidth())
        self.downloadButton.setSizePolicy(sizePolicy)
        self.downloadButton.setMaximumSize(QtCore.QSize(100, 23))
        self.downloadButton.setShortcut("")
        self.downloadButton.setCheckable(False)
        self.downloadButton.setChecked(False)
        self.downloadButton.setAutoExclusive(False)
        self.downloadButton.setAutoDefault(True)
        self.downloadButton.setDefault(False)
        self.downloadButton.setFlat(False)
        self.downloadButton.setObjectName("downloadButton")
        self.gridLayout.addWidget(self.downloadButton, 6, 0, 1, 1)
        self.movieIcon = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.movieIcon.sizePolicy().hasHeightForWidth())
        self.movieIcon.setSizePolicy(sizePolicy)
        self.movieIcon.setMaximumSize(QtCore.QSize(340, 218))
        self.movieIcon.setStyleSheet("")
        self.movieIcon.setText("")
        self.movieIcon.setTextFormat(QtCore.Qt.PlainText)
        self.movieIcon.setPixmap(QtGui.QPixmap(".src/moveimage.webp"))
        self.movieIcon.setScaledContents(True)
        self.movieIcon.setWordWrap(False)
        self.movieIcon.setObjectName("movieIcon")
        self.gridLayout.addWidget(self.movieIcon, 0, 0, 2, 1)
        self.downloadButton.clicked.connect(self.client.Download)
        self.retranslateUi(Dialog)
        self.start_signal.connect(self.startMovie)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def setMovieName(self, name:str):
        self.movieName.setText(name)
        self.movieName.setStyleSheet("color: rgb(0, 0, 0);")

    def setProgress(self, progress: int):
        self.downloadProgress.setValue(progress)
    
    def setReadyToDownload(self):
        self.statusLabel.setText("Gotta \nDownload")
        self.statusLabel.setStyleSheet("color: rgb(255, 140, 0);")

    def downloadComplete(self):
        _translate = QtCore.QCoreApplication.translate
        self.statusLabel.setStyleSheet("color: rgb(0, 255, 0);")
        self.statusLabel.setText(_translate("Dialog", "Ready"))

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.statusLabel.setText(_translate("Dialog", "No Movie \nSelected"))
        self.participantsLabel.setText(_translate("Dialog", "Participants"))
        self.leaveButton.setText(_translate("Dialog", "Leave"))
        self.downloadButton.setText(_translate("Dialog", "Download"))
    


    @Slot(str)
    def startMovie(self, moviedir):
        self.vlcinstance = vlccontroller.VlcInstance()
        self.vlcinstance.CreateInstance(moviedir, self.client.sendData)

import utilities
import constant

class Client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(2000)
        self.movieName: str = ""
        self.movieSize: int = 0
        self.name: str
        self.videosDir = os.path.expanduser("~\Videos\Vidarty")
        if(not os.path.exists(self.videosDir)):
            os.mkdir(self.videosDir)
        self.movieDir = self.videosDir
        self.downloadedmovies = utilities.checkForDownloadedMovies(self.movieDir)

    def connect(self, ip):
        print(self.name)
        if(len(self.name) < 3):
            return
        self.client.connect((ip, 80))
        self.Hostip = ip
        self.sendData(constant.NAME + self.name)
        while(True):
            try:
                data = self.getData()
                if(data == constant.CONNECTED): 
                    self.Widget = QtWidgets.QWidget()
                    self.ui = ClientMenu_Ui()
                    self.ui.client = self
                    self.ui.setupUi(self.Widget)
                    self.Widget.show()
                    utilities.startThread(self.readData)
                    break
            except Exception as e: print(e)

    def sendData(self, data: str):
        try:
            self.client.send(data.encode("utf-8"))
            print(data)
        except Exception as e: print(e)

    def getData(self):
        return self.client.recv(1024).decode("utf-8")

    def readData(self):
        while True:
            try:
                data = self.getData()
                if(len(data)>0):
                    print(data)
                
                if(utilities.checkDataType(data, constant.ROOMCREATED)):
                    self.ui.start_signal.emit(self.movieDir)
                elif(utilities.checkDataType(data, constant.PLAY)):
                    self.ui.vlcinstance.Play()
                elif(utilities.checkDataType(data, constant.PAUSE)):
                    self.ui.vlcinstance.Pause()
                elif(utilities.checkDataType(data, constant.DIR)):
                    data = utilities.filterData(data, constant.DIR)
                elif(utilities.checkDataType(data, constant.MD5)):
                    data = utilities.filterData(data, constant.MD5)
                    found = False
                    for file in self.downloadedmovies:
                        if(utilities.compareIntegritys(file[0], data)):
                            self.movieDir = file[1]
                            self.movieName = os.path.basename(file[1])
                            self.ui.setProgress(100)
                            self.ui.setMovieName(self.movieName)
                            self.ui.downloadComplete()
                            found = True
                            break
                    if(not found):
                        self.sendData(constant.DOWNLOAD)
                        self.ui.setProgress(0)
                elif(utilities.checkDataType(data, constant.SIZE)): #Check for Size and Name
                    data = utilities.filterData(data, constant.SIZE)
                    self.movieName = ""
                    self.movieSize = ""
                    isName = False
                    for i in data: #Check For Name
                        if(i == "N"):
                            data = data.removeprefix("N")
                            self.movieName = data
                            break
                        else:
                            self.movieSize = int(str(self.movieSize) + i)
                            data = data.removeprefix(i)
                    self.movieDir = self.videosDir + self.movieName
                    self.ui.setReadyToDownload()
            except Exception as e:print(e)   


    def Download(self):
        self.ui.setMovieName(self.movieName)
        chunk_size = 40960
        print(self.movieSize)
        totalfragments = self.movieSize / chunk_size
        curfragment = 0
        beforeprogress = 0
        print(self.movieDir + "    "+ self.movieName)
        self.serverdir = "http://" + self.Hostip + ":8000/" + self.movieName
        with requests.get(self.serverdir, stream=True) as r:
            with open(self.movieDir + self.movieName, 'wb') as f:
                for chunk in r.iter_content(chunk_size):
                    if chunk:
                        f.write(chunk)
                        curfragment += 1
                        curprogress = math.ceil(curfragment*100/totalfragments)
                        if(beforeprogress < curprogress):
                            self.ui.setProgress(curprogress)
                            beforeprogress = curprogress
        self.ui.downloadComplete()