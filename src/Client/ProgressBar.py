from PyQt4 import QtGui
from PyQt4.QtCore import QTimer, SIGNAL, SLOT, pyqtSlot, Qt
from time import sleep

class ProgressBar(QtGui.QWidget):

    def __init__(self, socket): 
        super(ProgressBar, self).__init__(None, Qt.WindowStaysOnTopHint)
        
        self.hasFinished = False
        self.setGeometry(250, 100, 275, 100)
        self.setFixedSize(self.size())
        self.setWindowTitle("Analyzing frames...")
        self.setWindowIcon(QtGui.QIcon('../../images/heart.ico'))
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        
        # center progress bar w/ main window
        fg = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())
        
        self.socket = socket
        
        self.initProgressBar()
        
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.progress)
        
        self.setLayout(self.vbox)
        
        self.show()
        
    def completed(self):
        progressReport = self.socket._send({'command':'progressReport'})
        if progressReport['status'] == 'running':
            self.progress.setValue(progressReport['progress']*100)
        if progressReport['progress']*100 == 100:
            self.timer.stop()
            self.hasFinished = True
            self.close()
        
    def initProgressBar(self):
        self.progress = QtGui.QProgressBar(self)
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.completed)
        self.timer.start(500)
        
    def closeEvent(self, event):
        # Currently unable to stop image processing, so ignore close events unless finished.
        if not self.hasFinished:
            event.ignore()
        '''if not self.hasFinished:
            quit_message = 'Are you sure you would like to cancel the frame analysis?'
            reply = QtGui.QMessageBox.question(self, 'Message', quit_message,
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                self.timer.stop()
                event.accept()
            else:
                event.ignore()'''