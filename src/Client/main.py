from PyQt4.QtGui import *
from PyQt4.QtCore import QPoint, QRect, QSize, Qt
from PyQt4.phonon import Phonon
from PyQt4 import QtCore
from my_ui import Ui_MainWindow
from clientSocket import ClientSocket

import cv2
import imageio
imageio.plugins.ffmpeg.download()
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

class MyMainUi(QMainWindow, Ui_MainWindow, QLabel):

    def __init__(self, parent=None):
        super(MyMainUi, self).__init__(parent)
        QLabel.__init__(self, parent)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.clientSocket = ClientSocket()
        self.clientSocket.connect()

        # Setup UI.
        self.setupUi(self)
        self.play_pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))

        # Setup video widget.
        self.fileName = None
        self.mediaObject = Phonon.MediaObject()
        self.videoWidget = self.videoPlayer.videoWidget()
        Phonon.createPath(self.mediaObject, self.videoWidget)
        self.mediaObject.stateChanged.connect(self.stateChanged)

        # Connect seek slider.
        self.seekSlider.setMediaObject(self.mediaObject)

        # Connect menu options (load, analyze, and exit).
        self.actionLoad.triggered.connect(self.loadVideo)
        self.actionAnalyze_Area.triggered.connect(self.analyzeArea)
        self.actionExit.triggered.connect(self.exit)

        # Connect buttons.
        self.play_pauseButton.clicked.connect(self.playPause)
        self.stopButton.clicked.connect(self.stop)
        self.analyzeButton.clicked.connect(self.analyze)

    def stateChanged(self, newstate, oldstate):
        if self.mediaObject.state() == Phonon.ErrorState:
            self.play_pauseButton.setEnabled(False)
            self.stopButton.setEnabled(False)
            messageBox = QMessageBox()
            messageBox.critical(None, 'ERROR', self.mediaObject.errorString() + '.')
        elif self.mediaObject.state() == Phonon.PlayingState:
            self.play_pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.play_pauseButton.setToolTip('Pause')
        else:
            self.play_pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.play_pauseButton.setToolTip('Play')

    def loadVideo(self):
        file = QFileDialog.getOpenFileName(self, "Select Video to Load")

        if file != '':
            self.mediaObject.setCurrentSource(Phonon.MediaSource(file))
            self.play_pauseButton.setEnabled(True)
            self.stopButton.setEnabled(True)
            self.mediaObject.play()
            self.mediaObject.pause()
            self.fileName = file

    def analyzeArea(self):
        if self.rangeSlider.isVisible():
            self.mediaObject.seek(0)
            self.rangeSlider.hide()
            self.analyzeButton.hide()
            self.seekSlider.show()
            self.play_pauseButton.show()
            self.stopButton.show()
        else:
            self.rangeSliderSetup()
            self.analyzeButton.show()
        print('')

    def rangeSliderSetup(self):
        self.rangeSlider.setMinimum(0)
        self.rangeSlider.setLow(0)

        self.mediaObject.seek(0)

        if self.mediaObject.totalTime() != 0:
            self.rangeSlider.setMaximum(self.mediaObject.totalTime())
            self.rangeSlider.setHigh(self.mediaObject.totalTime())
        else:
            self.rangeSlider.setMaximum(10000)
            self.rangeSlider.setHigh(10000)

        QtCore.QObject.connect(self.rangeSlider, QtCore.SIGNAL('sliderMoved(int)'), self.seekRangeSlider)

        self.play_pauseButton.hide()
        self.stopButton.hide()
        self.seekSlider.hide()

        self.rangeSlider.show()

    def seekRangeSlider(self, value):
        self.mediaObject.seek(value)

    def analyze(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Folder for Vector Output")
        self.extractClip()
        self.clientSocket.sendPath(directory)

    def extractClip(self):
        beginning = float(self.rangeSlider.low()) / float(1000)
        end = float(self.rangeSlider.high()) / float(1000)
        target = self.fileName[:-4] + "[SUBCLIP].avi"
        ffmpeg_extract_subclip(self.fileName, beginning, end, targetname=target)
        self.extractFrames(target)

    def extractFrames(self, videoFile):
        cap = cv2.VideoCapture(videoFile)
        count = 0

        while count < cap.get(cv2.CAP_PROP_FRAME_COUNT):
            ret, frame = cap.read()
            frame = frame[0:0 + 725, 188:188 + 465]
            cv2.imwrite("../../tests/images/clientTest/frame%d.png" % count, frame)
            count = count + 1

        cap.release()
        cv2.destroyAllWindows()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = QPoint(event.pos())
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()
    
    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rubberBand.hide()

    def playPause(self):
        if self.mediaObject.state() == Phonon.PlayingState:
            self.mediaObject.pause()
        # Restart if at end of video.
        elif self.mediaObject.remainingTime() == 0:
            self.mediaObject.seek(0)
            self.mediaObject.play()
        else:
            self.mediaObject.play()

    def stop(self):
        self.mediaObject.stop()
        self.mediaObject.play()
        self.mediaObject.pause()

    @staticmethod
    def exit():
        self.clientSocket.close()
        app.exit()


if __name__ == "__main__":
    app = QApplication([])
    my_ui = MyMainUi()
    my_ui.show()
    app.exit(app.exec_())
