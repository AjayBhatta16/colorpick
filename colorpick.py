# color pick version 1.2.1

# Qt5 imports
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPalette, QColor, QKeySequence
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QWidget, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QLabel, QSlider, QPushButton, QApplication, QAction

# custom package imports
from pyswitch import Switch

# stdlib imports
import math
import random as rd 
import json 

def getHex(num):
    # assumes an integer between 0 and 255
    hexString = ''

    # get first digit
    s = Switch(math.floor(num/16))
    if s.case(10):
        hexString = hexString + 'A'
    if s.case(11):
        hexString = hexString + 'B'
    if s.case(12):
        hexString = hexString + 'C'
    if s.case(13):
        hexString = hexString + 'D'
    if s.case(14):
        hexString = hexString + 'E'
    if s.case(15):
        hexString = hexString + 'F'
    if s.default():
        hexString = hexString + str(math.floor(num/16))

    # get second digit 
    s.restart(num%16)
    if s.case(10):
        hexString = hexString + 'A'
    if s.case(11):
        hexString = hexString + 'B'
    if s.case(12):
        hexString = hexString + 'C'
    if s.case(13):
        hexString = hexString + 'D'
    if s.case(14):
        hexString = hexString + 'E'
    if s.case(15):
        hexString = hexString + 'F'
    if s.default():
        hexString = hexString + str(num%16)
    return hexString

def getHSL(r,g,b):
    # sources:
    # https://stackoverflow.com/questions/39118528/rgb-to-hsl-conversion
    # https://www.niwa.nu/2013/05/math-behind-colorspace-conversions-rgb-hsl/

    # get base hue value
    r /= 255
    g /= 255
    b /= 255
    maximum = max([r,g,b])
    minimum = min([r,g,b])
    chroma = maximum - minimum
    if chroma == 0:
        hue = 0
    else:
        s = Switch(maximum)
        if s.case(r):
            segment = (g - b) / chroma
            shift = 0
            if segment < 0:
                shift = 6
        if s.case(g):
            segment = (b - r) / chroma
            shift = 2
        if s.case(b):
            segment = (r - g) / chroma
            shift = 4
        hue = (segment + shift) * 60

    # get base luminace value
    luminace = (minimum + maximum) / 2

    # get base saturation value
    if maximum == minimum:
        saturation = 0
    else:
        if luminace < 0.5:
            saturation = chroma / (2 * luminace)
        else:
            saturation = chroma / (2 * (1 - luminace))
        saturation *= 100

    # reformat values
    luminace *= 100
    if hue % 1 == 0:
        hue = int(hue)
    else: 
        hue = round(hue,2)
    if saturation % 1 == 0:
        saturation = int(saturation)
    else:
        saturation = round(saturation,3)
    if luminace % 1 == 0:
        luminace = int(luminace)
    else:
        luminace = round(luminace,3)
    return "HSL("+str(hue)+","+str(saturation)+"%,"+str(luminace)+"%)"

class ColorPick(QMainWindow):
    def __init__(self):
        super().__init__()

        # initialize window
        self.setFixedSize(400,400)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)

        # main color variables
        self.r = 200
        self.g = 200
        self.b = 200

        # initialize palette
        self.style = QPalette()

        # create and style UI
        self.InitUI()
        self.InitMenu()
        self.StyleUI()

    def InitUI(self):
        # main layout of page
        generalLayout = QVBoxLayout()

        # sub layout for sliders
        layout = QGridLayout()

        # sub layout for random button
        layout2 = QGridLayout()

        # red label & slider
        rLabel = QLabel("Red:")
        rLabel.setAlignment(Qt.AlignLeft)
        rLabel.setFixedSize(40,20)
        self.red = QSlider(Qt.Horizontal)
        self.red.setMinimum(0)
        self.red.setMaximum(255)
        self.red.setValue(200)
        self.red.valueChanged.connect(self.changeRed)

        # green label & slider
        gLabel = QLabel("Green:")
        gLabel.setAlignment(Qt.AlignLeft)
        gLabel.setFixedSize(40,20)
        self.green = QSlider(Qt.Horizontal)
        self.green.setMinimum(0)
        self.green.setMaximum(255)
        self.green.setValue(200)
        self.green.valueChanged.connect(self.changeGreen)

        # blue label & slider
        bLabel = QLabel("Blue:")
        bLabel.setAlignment(Qt.AlignLeft)
        bLabel.setFixedSize(40,20)
        self.blue = QSlider(Qt.Horizontal)
        self.blue.setMinimum(0)
        self.blue.setMaximum(255)
        self.blue.setValue(200)
        self.blue.valueChanged.connect(self.changeBlue)

        # RGB Label
        self.label = QLabel("rgb(200,200,200)")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # Hex label
        self.label2 = QLabel("#C8C8C8")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # HSL label
        self.label3 = QLabel("HSL(0,0%,78.4%)")
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # random button
        self.randomButton = QPushButton("Random")
        self.randomButton.setFixedWidth(100)
        self.randomButton.clicked.connect(self.randomColor)

        # add widgets to slider sub layout
        layout.addWidget(rLabel,0,0)
        layout.addWidget(self.red,0,1)
        layout.addWidget(gLabel,1,0)
        layout.addWidget(self.green,1,1)
        layout.addWidget(bLabel,2,0)
        layout.addWidget(self.blue,2,1)

        # add random button to bottom sub layout
        layout2.addWidget(self.randomButton,0,0)

        # add widgets to main layout
        generalLayout.addLayout(layout)
        generalLayout.addWidget(self.label)
        generalLayout.addWidget(self.label2)
        generalLayout.addWidget(self.label3)
        generalLayout.addLayout(layout2)

        # add main layout to central widget
        self._centralWidget.setLayout(generalLayout)

    def InitMenu(self):
        # initialize menu bar
        self.menu = self.menuBar().addMenu("&File")

        # create save action
        self.saveColor = QAction("&Save")
        self.saveColor.triggered.connect(self.save)
        self.saveColor.setShortcut(QKeySequence.Save)

        # create open action
        self.openColor = QAction("&Open")
        self.openColor.triggered.connect(self.open)
        self.openColor.setShortcut(QKeySequence.Open)

        # add actions to menu bar
        self.menu.addAction(self.saveColor)
        self.menu.addAction(self.openColor)

    def StyleUI(self):
        # set the color according to the sliders
        self.style.setColor(QPalette.Window,QColor(self.r,self.g,self.b))

        # adjust text color accordingly
        self.textBrightness = int(255-(self.r+self.g+self.b)/3)
        self.style.setColor(QPalette.WindowText,QColor(self.textBrightness,self.textBrightness,self.textBrightness))

        # update palette
        app.setPalette(self.style)

    @pyqtSlot()
    def changeRed(self):
        # get new color 
        self.r = self.red.value()

        # modify labels
        self.label.setText("rgb("+str(self.r)+","+str(self.g)+","+str(self.b)+")")
        self.label2.setText("#"+getHex(self.r)+getHex(self.g)+getHex(self.b))
        self.label3.setText(getHSL(self.r,self.g,self.b))

        # adjust stylesheet
        self.StyleUI()

    def changeGreen(self):
        # get new color
        self.g = self.green.value()

        # modify labels
        self.label.setText("rgb("+str(self.r)+","+str(self.g)+","+str(self.b)+")")
        self.label2.setText("#"+getHex(self.r)+getHex(self.g)+getHex(self.b))
        self.label3.setText(getHSL(self.r,self.g,self.b))

        # adjist stylesheet
        self.StyleUI()

    def changeBlue(self):
        # get new color
        self.b = self.blue.value()

        # modify labels
        self.label.setText("rgb("+str(self.r)+","+str(self.g)+","+str(self.b)+")")
        self.label2.setText("#"+getHex(self.r)+getHex(self.g)+getHex(self.b))
        self.label3.setText(getHSL(self.r,self.g,self.b))

        # adjust stylesheet
        self.StyleUI()

    def randomColor(self):
        # get random colors
        self.r = rd.randint(0,255)
        self.g = rd.randint(0,255)
        self.b = rd.randint(0,255)

        # adjust sliders
        self.red.setValue(self.r)
        self.green.setValue(self.g)
        self.blue.setValue(self.b)

        # modify labels
        self.label.setText("rgb("+str(self.r)+","+str(self.g)+","+str(self.b)+")")
        self.label2.setText("#"+getHex(self.r)+getHex(self.g)+getHex(self.b))
        self.label3.setText(getHSL(self.r,self.g,self.b)) 

        # update stylesheet       
        self.StyleUI()

    def save(self):
        # create data to be saved
        data = {
            "r": str(self.r),
            "g": str(self.g),
            "b": str(self.b),
            "rgb": self.label.text(),
            "hex": self.label2.text(),
            "hsl": self.label3.text()
        }
        # get directory to save to
        path = QFileDialog.getSaveFileName(self,"Save")[0]

        # write data to given directory
        with open(path,"w") as f:
            f.write(json.dumps(data))

    def open(self):
        # get directory of file
        path = QFileDialog.getOpenFileName(self,"Open")[0]
        # read data from file
        if path:
            with open(path,"r") as f:
                data = json.loads(f.read())
        # read RGB values
        self.r = int(data["r"])
        self.g = int(data["g"])
        self.b = int(data["b"])
        
        # update stylesheet
        self.StyleUI()

        # update labels
        self.label.setText(data["rgb"])
        self.label2.setText(data["hex"])
        self.label3.setText(data["hsl"])

# generate application
app = QApplication([])
view = ColorPick()
view.show()
app.exec_()
 
"""
Changelog:

1.0.1 - added hexadecimal conversion feature
      - hex conversion algorithm created math and pyswitch dependencies
      - made rgb and hex text selectable by mouse

1.0.2 - added labels for color sliders
      - put labels and color sliders in grid sub-layout

1.0.3 - added HSL conversion feature
      - fixed text staying black on dark colors

1.1.0 - added button for random color
      - created dependency on random library

1.2.0 - added option to save color in json object
      - save feature created dependency on json library
      - added inline documentation
      - made additional improvements to code readability

1.2.1 - added option to open saved colors
      - replaced * imports with specific class imports
      - added keyboard shortcuts for save and open
"""
