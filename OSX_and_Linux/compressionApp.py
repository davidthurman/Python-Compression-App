#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QAction, QFileDialog, QCheckBox,
    QInputDialog, QSlider, QVBoxLayout, QLCDNumber, QApplication, QLabel, QHBoxLayout, QMainWindow, QTextEdit)
from PyQt5.QtGui import QIcon

class CompressApp(QWidget):

    checkbox = True
    speed = "faster"

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):      

        # Set up labels above slider
        speedLabels = QHBoxLayout()
        slowLabel = QLabel("Slow", self)
        slowLabel.setStyleSheet('font-size: 10pt;')
        mediumLabel = QLabel("Medium", self)
        mediumLabel.setStyleSheet('font-size: 10pt;')
        fastLabel = QLabel("Fast", self)
        fastLabel.setStyleSheet('font-size: 10pt;')
        fasterLabel = QLabel("Faster", self)
        fasterLabel.setStyleSheet('font-size: 10pt;')
        veryfastLabel = QLabel("Veryfast", self)
        veryfastLabel.setStyleSheet('font-size: 10pt;')
        ultrafastLabel = QLabel("Ultrafast", self)
        ultrafastLabel.setStyleSheet('font-size: 10pt;')
        speedLabels.addWidget(slowLabel)
        speedLabels.addWidget(mediumLabel)
        speedLabels.addWidget(fastLabel)
        speedLabels.addWidget(fasterLabel)
        speedLabels.addWidget(veryfastLabel)
        speedLabels.addWidget(ultrafastLabel)
        speedLabels.setSpacing(75)

        # Add slider and labels to VBox
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setRange(0, 5)
        self.sld.setValue(4)
        self.sld.setTickPosition(QSlider.TicksBelow)
        self.sld.setTickInterval(1)
        self.sld.valueChanged[int].connect(self.changeValue)
        sliderAndQualitiesVBox = QVBoxLayout()
        sliderAndQualitiesVBox.addLayout(speedLabels)
        sliderAndQualitiesVBox.addWidget(self.sld)

        # Add Speed and Quality labels and slider to HBox
        qualityLabel = QLabel("Quality", self)
        speedLabel = QLabel("Speed", self)
        sliderHBox = QHBoxLayout()
        sliderHBox.addWidget(qualityLabel)      
        sliderHBox.addLayout(sliderAndQualitiesVBox)
        sliderHBox.addWidget(speedLabel)

        # Add entire HBox to the main vbox of the app
        vbox = QVBoxLayout()
        vbox.addLayout(sliderHBox)

        # Add checkbox to keep original files or not
        cb = QCheckBox('Overwrite Existing File(s)?', self)
        cb.stateChanged.connect(self.checkboxChange)
        centeringHBox = QHBoxLayout()
        centeringHBox.addStretch(1)
        centeringHBox.addWidget(cb)
        centeringHBox.addStretch(2)
        vbox.addLayout(centeringHBox)

        # Make Single File button and Directory Button and add them to Hbox
        compressFileBtn = QPushButton('Compress a File', self)        
        compressFileBtn.clicked.connect(self.compressFile)
        compressDirBtn = QPushButton('Compress a Directory', self)    
        compressDirBtn.clicked.connect(self.compressDir)
        mainButtonsHBox = QHBoxLayout()
        mainButtonsHBox.addWidget(compressFileBtn)
        mainButtonsHBox.addWidget(compressDirBtn)

        # Add buttons Hbox to main app VBox
        vbox.addLayout(mainButtonsHBox)

        # Set layout of app 
        self.setLayout(vbox)
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Compression')
        self.show()
        
    def compressDir(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        x = 0
        for i in os.listdir(directory):
            if x == 0:
                directory = self.makeReadable(directory)
            x = x + 1
            if i.endswith(".mp4"): 
                i = str(self.makeReadable(i))
                os.system("time ffmpeg -threads 8 -i " + directory + "/" + i + " -c:v libx265 -preset " + self.speed + " -quality 1 -c:a aac -b:a 128k -strict -2 " + directory + "/" + i + "Compressed.mp4 -y")
                if self.checkbox == True:
                    os.system("rm " + directory + "/" + i)
                    os.system("mv " + directory + "/" + i + "Compressed.mp4 " + directory + "/" + i)
                continue
            else:
                continue

    def compressFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        newName = str(self.makeReadable(fname[0]))
        os.system("time ffmpeg -threads 8 -i " + newName + " -c:v libx265 -preset " + self.speed + " -quality 1 -c:a aac -b:a 128k -strict -2 " + newName + "Compressed.mp4 -y")
        if self.checkbox == True:
            os.system("rm " + newName)
            os.system("mv " + newName + "Compressed.mp4 " + newName)
        
    def checkboxChange(self, state):
        if state == Qt.Checked:
            self.checkbox = True
        else:
            self.checkbox = False

    def changeValue(self, value):
        if value == 5:
            self.speed = "ultrafast"
        elif value == 4:
            self.speed = "veryfast"
        elif value == 3:
            self.speed = "faster"
        elif value == 2:
            self.speed = "fast"
        elif value == 1:
            self.speed = "medium"
        else:
            self.speed = "slow"

    def makeReadable(self, myString):
        myString = myString.replace(" ", "\ ")
        myString = myString.replace("(", "\(")
        myString = myString.replace(")", "\)")
        myString = myString.replace("*", "\*")
        myString = myString.replace("!", "\!")
        myString = myString.replace("@", "\@")
        myString = myString.replace("#", "\#")
        myString = myString.replace("$", "\$")
        myString = myString.replace("%", "\%")
        myString = myString.replace("^", "\^")
        myString = myString.replace("&", "\&")
        myString = myString.replace("<", "\<")
        myString = myString.replace(">", "\>")
        myString = myString.replace("[", "\[")
        myString = myString.replace("]", "\]")
        myString = myString.replace("|", "\|")
        myString = myString.replace("{", "\{")
        myString = myString.replace("}", "\}")
        return myString

if __name__ == '__main__':
    app = QApplication(sys.argv)
    compressApp = CompressApp()
    sys.exit(app.exec_())