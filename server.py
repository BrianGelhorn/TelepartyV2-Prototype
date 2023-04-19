import socket
from threading import Thread
from PySide2 import QtCore, QtGui, QtWidgets
from urllib.request import urlopen
import shutil
import os
import vlccontroller
import http.server
import socketserver
import hashlib


class createMenu_IU(object):
    def setupUi(self, Dialog):
        self.sv = Server(self)
        self.allparticipants = []
        Dialog.setObjectName("Dialog")
        Dialog.resize(661, 387)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(125, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.listView = QtWidgets.QListWidget(Dialog)
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
        self.gridLayout.addWidget(self.listView, 1, 3, 1, 1)
        self.participantsLabel = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.participantsLabel.setFont(font)
        self.participantsLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.participantsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.participantsLabel.setObjectName("participantsLabel")
        self.gridLayout.addWidget(self.participantsLabel, 0, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(0, 120, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 6, 0, 1, 1)
        self.movieIcon = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.movieIcon.sizePolicy().hasHeightForWidth())
        self.movieIcon.setSizePolicy(sizePolicy)
        self.movieIcon.setMaximumSize(QtCore.QSize(340, 218))
        self.movieIcon.setText("")
        self.movieIcon.setTextFormat(QtCore.Qt.PlainText)
        self.movieIcon.setPixmap(QtGui.QPixmap("./src/defaultImage.webp"))
        self.movieIcon.setScaledContents(True)
        self.movieIcon.setWordWrap(False)
        self.movieIcon.setObjectName("movieIcon")
        self.gridLayout.addWidget(self.movieIcon, 0, 0, 5, 1)
        self.loadButton = QtWidgets.QPushButton(Dialog)
        self.loadButton.setObjectName("loadButton")
        self.loadButton.clicked.connect(self.openMovie)
        self.gridLayout.addWidget(self.loadButton, 0, 1, 1, 1)
        self.createButton = QtWidgets.QPushButton(Dialog)
        self.createButton.setObjectName("createButton")
        
        self.gridLayout.addWidget(self.createButton, 8, 0, 1, 1)
        self.movieName = QtWidgets.QLabel(Dialog)
        self.ipLabel = QtWidgets.QLabel(Dialog)
        self.ipLabel.setText(str(urlopen('https://api.ipify.org?format=json').read()).replace('b\'{"ip":"', "").replace('"}\'', ""))
        self.gridLayout.addWidget(self.ipLabel)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.movieName.setFont(font)
        self.movieName.setStyleSheet("color: rgb(255, 0, 0);")
        self.movieName.setObjectName("movieName")
        self.movieName.setMaximumWidth(340)
        self.gridLayout.addWidget(self.movieName, 5, 0, 1, 1)
        self.createButton.clicked.connect(self.createRoom)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def openMovie(self):
        self.movie = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', "", "Video Files (*.mp4 *.mkv); All Files (*)")
        try:
            f = open(self.movie[0])
            name = os.path.basename(f.name)
            dir = shutil.copy2(self.movie[0], self.sv.movieDir)
            self.sv.movieMd5 = util.checkIntegrity(dir)
            self.movieName.setText(name)
            self.movieName.setStyleSheet("color: rgb(0, 0, 0);")
            Thread(target=self.sv.startFileHost, daemon=True).start()
            self.sv.downloadrequest = constant.SIZE + str(os.stat(f.name).st_size) + "N" + name
            self.sv.sendData(constant.MD5 + self.sv.movieMd5)
        except Exception as e: print(e)

    def createRoom(self):
        self.vlcinstance = vlccontroller.VlcInstance()
        self.vlcinstance.CreateInstance(self.movie[0], self.sv.sendData)
        self.sv.sendData(constant.ROOMCREATED)

    def addParticipant(self, participant:str):
        self.allparticipants.append(participant)
        self.updateParticipants()

    def updateParticipants(self):
        strallparticipants = ""
        for i in self.allparticipants:
            strallparticipants += i + "\n"
        self.listView.addItem(strallparticipants)

    def deleteParticipant(self, participant:str):
        self.allparticipants.remove(participant)
        self.updateParticipants()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.participantsLabel.setText(_translate("Dialog", "Participants"))
        self.loadButton.setText(_translate("Dialog", "Load Movie"))
        self.createButton.setText(_translate("Dialog", "Create Room"))
        self.movieName.setText(_translate("Dialog", "Select a movie"))
import time
import utilities as util
import constant


class Server():
    def __init__(self, menu: createMenu_IU):
        self.movieMd5: str
        self.clientList: list[list[socket.socket, str]] = []
        self.movieDir: str
        self.read: Thread
        self.downloadrequest: str

        hostThread = Thread(target=self.startHost, daemon=True)
        hostThread.start()
        self.menu = menu
        self.videosDir = "~\Videos\Vidarty"
        if(not os.path.exists(os.path.expanduser(self.videosDir))):
            os.mkdir(os.path.expanduser(self.videosDir))
        self.movieDir = os.path.expanduser(self.videosDir)

    def startHost(self):
        ip, port = socket.gethostbyname(socket.gethostname()), 80
        self.host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host.bind((ip, port))
        self.host.listen(5)
        Thread(target=self.listenForJoiners, daemon=True).start()
        Thread(target=self.readData, daemon=True).start()
        Thread(target=self.checkIfAlive, daemon=True).start()

    def sendData(self, data: str):
        for client in self.clientList:
            try: 
                client[0].send(data.encode("utf-8"))
            except Exception as e:
                self.menu.deleteParticipant(self.clientList[self.clientList.index(client)][1])
                self.clientList.remove(client)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.movieDir: str
            super().__init__(*args, **kwargs, directory=self.movieDir)

    def startFileHost(self):
        # os.system("python -m http.server 8000 --directory ./temp")
        PORT = 8000
        Handler = self.Handler
        Handler.movieDir = self.movieDir
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            httpd.serve_forever()

    def listenForJoiners(self):
        while True:
            try:
                (clientsocket, address) = self.host.accept()
                data = clientsocket.recv(1024).decode("utf-8")
                if(util.checkDataType(data, constant.NAME)):
                    data = util.filterData(data, constant.NAME)
                    self.menu.addParticipant(data)
                    if(not clientsocket in self.clientList):
                        self.clientList.append([clientsocket, data, True])
                        clientsocket.send(constant.CONNECTED.encode("utf-8"))
                    if(self.downloadrequest):
                        util.sendDataToSocket(clientsocket, constant.MD5 + self.movieMd5)
            except Exception as e: print(e)

    def readData(self):
        while True:
            try:
                for client in self.clientList:
                    data = client[0].recv(1024).decode("utf-8")
                    print(data)
                    if(util.checkDataType(data, constant.PLAY)):
                        self.menu.vlcinstance.Play()
                    elif(util.checkDataType(data, constant.PAUSE)):
                        self.menu.vlcinstance.Pause()
                    elif(util.checkDataType(data, constant.DOWNLOAD)):
                        util.sendDataToSocket(client[0], self.downloadrequest)
            except Exception as e: print(e)

    def checkIfAlive(self):
        while True:
            self.sendData("a")
            time.sleep(5)

    def stopHost(self):
    #TODO Interrupt startHost method
        pass
