import vlc
from PySide2 import QtWidgets, QtCore
import shutil


from PySide2 import QtCore, QtWidgets
import shutil

class vlcInterface_Ui(object):
    def setupUi(self, MainWindow, playPauseAction, openFile):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(821, 599)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.PlayPause = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PlayPause.sizePolicy().hasHeightForWidth())
        self.PlayPause.setSizePolicy(sizePolicy)
        self.PlayPause.setCheckable(False)
        self.PlayPause.setChecked(False)
        self.PlayPause.setAutoDefault(False)
        self.PlayPause.setDefault(False)
        self.PlayPause.setFlat(False)
        self.PlayPause.setProperty("isPlaying", False)
        self.PlayPause.setObjectName("PlayPause")
        self.gridLayout.addWidget(self.PlayPause, 4, 0, 1, 1)
        self.ProgressBar = QtWidgets.QSlider(self.centralwidget)
        self.ProgressBar.setOrientation(QtCore.Qt.Horizontal)
        self.ProgressBar.setObjectName("ProgressBar")
        self.gridLayout.addWidget(self.ProgressBar, 4, 1, 1, 1)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(782, 512))
        self.widget.setObjectName("widget")
        self.gridLayout.addWidget(self.widget, 0, 0, 3, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 821, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuActions = QtWidgets.QMenu(self.menubar)
        self.menuActions.setObjectName("menuActions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)

        self.actionOpen.triggered.connect(openFile)

        self.actionOpen.setObjectName("actionOpen")
        self.actionDisconnect = QtWidgets.QAction(MainWindow)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.actionParticipants = QtWidgets.QAction(MainWindow)
        self.actionParticipants.setObjectName("actionParticipants")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionLeave = QtWidgets.QAction(MainWindow)
        self.actionLeave.setObjectName("actionLeave")
        self.actionFullscreen = QtWidgets.QAction(MainWindow)
        self.actionFullscreen.setObjectName("actionFullscreen")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionLeave)
        self.menuFile.addAction(self.actionClose)
        self.menuActions.addAction(self.actionFullscreen)
        self.menuActions.addAction(self.actionParticipants)
        self.menuActions.addAction(self.actionDisconnect)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuActions.menuAction())

        self.PlayPause.clicked.connect(playPauseAction)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.PlayPause.setText(_translate("MainWindow", "Play"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuActions.setTitle(_translate("MainWindow", "Actions"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionDisconnect.setText(_translate("MainWindow", "Disconnect"))
        self.actionParticipants.setText(_translate("MainWindow", "Participants"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionLeave.setText(_translate("MainWindow", "Leave"))
        self.actionFullscreen.setText(_translate("MainWindow", "Fullscreen"))

class VlcInstance():

    def CreateInstance(self, moviedir, senddatafunc):
        self.senddatafunc = senddatafunc
        self.interface = vlcInterface_Ui()
        instance: vlc.Instance
        instance = vlc.Instance(['--video-on-top'])
        self.player = instance.media_player_new()
        self.interface.player = self.player
        media = instance.media_new(moviedir)
        self.player.set_media(media)
        self.mainwindow = QtWidgets.QMainWindow()
        self.interface.setupUi(self.mainwindow, self.PlayPause, self.openFile)
        self.mainwindow.show()
        self.player.set_hwnd(self.interface.widget.winId())
        self.player.play()
    
    def openFile(self):
        self.name = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', "", "Video Files (*.mp4 *.mkv)")
        try:
            shutil.copy(self.name[0], "./Movies")
            print(self.name)
        except Exception as e: print(e)

    def PlayPause(self):
        if(self.player.is_playing()):
            self.Pause()
            self.senddatafunc("Pause")
        else:
            self.Play()
            self.senddatafunc("Play")

    def Play(self):
        self.player.play()

    def Pause(self):
        self.player.pause()