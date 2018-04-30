from PyQt4.QtGui import *
from PyQt4.QtCore import QPoint, QRect, QSize, Qt
from PyQt4.phonon import Phonon
from PyQt4 import QtCore
from my_ui import Ui_MainWindow
from clientSocket import ClientSocket
from ProgressBar import ProgressBar

import os
import cv2
import imageio
imageio.plugins.ffmpeg.download()
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

class MyMainUi(QMainWindow, Ui_MainWindow, QLabel):
    def __init__(self, parent=None):
        super(MyMainUi, self).__init__(parent)
        QLabel.__init__(self, parent)		
        # Connect to server.
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.clientSocket = ClientSocket()
        self.clientSocket.connect()
        self.progress = None

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
	
        # Setup rubberband.
        self.rubberBand = QRubberBand(QRubberBand.Rectangle)
        self.rubberBand.installEventFilter(self)
        self.rubberBand.hide()
        self.origin = QPoint()
        self.hasResized = False
        self.installEventFilter(self)
        
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
        
    # Detect change in video state.
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

    # Load user-specified video.
    def loadVideo(self):
        file = QFileDialog.getOpenFileName(self, "Select Video to Load")

        if file != '':
            # Load video and adjust GUI appropriately
            self.mediaObject.setCurrentSource(Phonon.MediaSource(file))
            self.play_pauseButton.setEnabled(True)
            self.stopButton.setEnabled(True)
            self.mediaObject.play()
            self.mediaObject.pause()
            self.fileName = file
            self.actionAnalyze_Area.setEnabled(True)
            
            # Retrieve video dimensions.
            cap = cv2.VideoCapture(self.fileName)
            videoWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            videoHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.aspectRatio = videoWidth / videoHeight
            cap.release()
            cv2.destroyAllWindows()
            
            # Maintain video aspect ratio.
            width, height = self.getAspectRatioDimensions()
            self.resize(width, height)
    
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

    # Construct range slider.
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
        
    # Alter GUI when analyze area button is pressed.
    def analyzeArea(self):
        if self.rangeSlider.isVisible():
            self.mediaObject.seek(0)
            self.rangeSlider.hide()
            self.analyzeButton.hide()
            self.rubberBand.hide()
            self.seekSlider.show()
            self.play_pauseButton.show()
            self.stopButton.show()
        else:
            self.rangeSliderSetup()
            self.analyzeButton.show()
            self.rubberBand.resize(0, 0)
            self.rubberBand.show()

    # Contact server for video analysis.
    def analyze(self):
        self.rubberBand.hide()
        directory = QFileDialog.getExistingDirectory(self, "Select Folder for Vector Output")
        
        if directory != '':
            self.extractClip(directory)
            self.clientSocket.sendPath(directory)
            self.progress = ProgressBar(self.clientSocket)
            
        self.rubberBand.resize(0, 0)
        self.rubberBand.show()

    # Obtain user-specified clip of video.
    def extractClip(self, directory):
        beginning = float(self.rangeSlider.low()) / float(1000)
        end = float(self.rangeSlider.high()) / float(1000)
        target = self.fileName[:-4] + "[SUBCLIP].avi"
        ffmpeg_extract_subclip(self.fileName, beginning, end, targetname=target)
        self.extractFrames(target, directory)

    def extractFrames(self, videoFile, directory):
        newDirectory = directory + "\Frames"
        os.makedirs(newDirectory, exist_ok=True)
        cap = cv2.VideoCapture(videoFile)
        count = 0
        
        while count < cap.get(cv2.CAP_PROP_FRAME_COUNT):
            ret, frame = cap.read()
            if (self.rubberBand.size().width() != 0):
                x, y, width, height = self.getCropPositions(frame)
                frame = frame[int(y):int(y) + int(height), int(x):int(x) + int(width)]
            cv2.imwrite(newDirectory + "/frame%d.png" % count, frame)
            count = count + 1
            
        cap.release()
        cv2.destroyAllWindows()
     
    # Obtain area of frame to crop.
    def getCropPositions(self, frame):
        imgHeight, imgWidth = frame.shape[:2]
        screenArea = self.videoWidget.geometry()
        selectedArea = self.rubberBand.geometry()
        startingPoint = self.videoWidget.mapFromGlobal(selectedArea.topLeft())
        
        widthFactor = imgWidth / screenArea.width()
        heightFactor = imgHeight / screenArea.height()
            
        x = startingPoint.x() * widthFactor
        y = startingPoint.y() * heightFactor
        cropWidth = selectedArea.width() * widthFactor
        cropHeight = selectedArea.height() * heightFactor
        
        return x, y, cropWidth, cropHeight
        
    # Obtain adjusted dimensions to maintain aspect ratio. Only change the width.
    def getAspectRatioDimensions(self):
        videoScaledXDim = self.aspectRatio * self.videoWidget.size().height()
        windowScaledXDim = videoScaledXDim + self.size().width() - self.videoWidget.size().width()
        windowY = self.size().height()
        return windowScaledXDim, windowY

    def mousePressEvent(self, event):
        widgetRect = self.videoWidget.geometry()
        mousePos = self.videoWidget.mapFromGlobal(event.globalPos())
        if widgetRect.contains(mousePos):
            self.origin = event.globalPos()
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
   
    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            widgetRect = self.videoWidget.geometry()
            mousePos = self.videoWidget.mapFromGlobal(event.globalPos())
            if widgetRect.contains(mousePos):
                self.rubberBand.setGeometry(QRect(self.origin, event.globalPos()).normalized())
          
    def eventFilter(self, object, event):
        # If window is moved or no longer in focus, remove rubber band.
        if event.type() == QtCore.QEvent.Move or event.type() == QtCore.QEvent.WindowDeactivate:
            if isinstance(object, QMainWindow):
                self.rubberBand.resize(0, 0)
                return True
                
        # If window was resized and contains a video, maintain the aspect ratio.
        if event.type() == QtCore.QEvent.NonClientAreaMouseMove or event.type() == QtCore.QEvent.HoverMove:
            if self.hasResized and self.mediaObject.hasVideo():
                width, height = self.getAspectRatioDimensions()
                self.resize(width, height)
                self.hasResized = False
                return True

         # If window is resized, remove rubber band.
        if event.type() == QtCore.QEvent.Resize:
            if isinstance(object, QMainWindow):
                self.hasResized = True
                self.rubberBand.resize(0, 0)
                return True
        
        return False

    # Menu exit button.
    def exit(self):
        self.clientSocket.close()
        app.exit()
    
    # Top-right window exit button.
    def closeEvent(self, event):
        self.clientSocket.close()
        app.exit()

if __name__ == "__main__":
    app = QApplication([])
    my_ui = MyMainUi()
    my_ui.show()
    app.exit(app.exec_())
