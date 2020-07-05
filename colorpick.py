# color pick version 1.0.3

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pyswitch import Switch
import math

def getHex(num):
    # assumes an integer between 0 and 255
    hexString = ''
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
    luminace = (minimum + maximum) / 2
    if maximum == minimum:
        saturation = 0
    else:
        if luminace < 0.5:
            saturation = chroma / (2 * luminace)
        else:
            saturation = chroma / (2 * (1 - luminace))
        saturation *= 100
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
        self.setFixedSize(400,400)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self.r = 200
        self.g = 200
        self.b = 200
        self.style = QPalette()
        self.InitUI()
        self.StyleUI()
    def InitUI(self):
        generalLayout = QVBoxLayout()
        layout = QGridLayout()
        rLabel = QLabel("Red:")
        rLabel.setAlignment(Qt.AlignLeft)
        rLabel.setFixedSize(40,20)
        self.red = QSlider(Qt.Horizontal)
        self.red.setMinimum(0)
        self.red.setMaximum(255)
        self.red.setValue(200)
        self.red.valueChanged.connect(self.changeRed)
        gLabel = QLabel("Green:")
        gLabel.setAlignment(Qt.AlignLeft)
        gLabel.setFixedSize(40,20)
        self.green = QSlider(Qt.Horizontal)
        self.green.setMinimum(0)
        self.green.setMaximum(255)
        self.green.setValue(200)
        self.green.valueChanged.connect(self.changeGreen)
        bLabel = QLabel("Blue:")
        bLabel.setAlignment(Qt.AlignLeft)
        bLabel.setFixedSize(40,20)
        self.blue = QSlider(Qt.Horizontal)
        self.blue.setMinimum(0)
        self.blue.setMaximum(255)
        self.blue.setValue(200)
        self.blue.valueChanged.connect(self.changeBlue)
        self.label = QLabel("rgb(200,200,200)")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label2 = QLabel("#C8C8C8")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label3 = QLabel("HSL(0,0%,78.4%)")
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(rLabel,0,0)
        layout.addWidget(self.red,0,1)
        layout.addWidget(gLabel,1,0)
        layout.addWidget(self.green,1,1)
        layout.addWidget(bLabel,2,0)
        layout.addWidget(self.blue,2,1)
        generalLayout.addLayout(layout)
        generalLayout.addWidget(self.label)
        generalLayout.addWidget(self.label2)
        generalLayout.addWidget(self.label3)
        self._centralWidget.setLayout(generalLayout)
    def StyleUI(self):
        self.style.setColor(QPalette.Window,QColor(self.r,self.g,self.b))
        self.textBrightness = int(255-(self.r+self.g+self.b)/3)
        self.style.setColor(QPalette.WindowText,QColor(self.textBrightness,self.textBrightness,self.textBrightness))
        app.setPalette(self.style)

    @pyqtSlot()
    def changeRed(self):
        self.r = self.red.value()
        self.label.setText("rgb("+str(self.r)+","+str(self.g)+","+str(self.b)+")")
        self.label2.setText("#"+getHex(self.r)+getHex(self.g)+getHex(self.b))
        self.label3.setText(getHSL(self.r,self.g,self.b))
        self.StyleUI()
    def changeGreen(self):
        self.g = self.green.value()
        self.label.setText("rgb("+str(self.r)+","+str(self.g)+","+str(self.b)+")")
        self.label2.setText("#"+getHex(self.r)+getHex(self.g)+getHex(self.b))
        self.label3.setText(getHSL(self.r,self.g,self.b))
        self.StyleUI()
    def changeBlue(self):
        self.b = self.blue.value()
        self.label.setText("rgb("+str(self.r)+","+str(self.g)+","+str(self.b)+")")
        self.label2.setText("#"+getHex(self.r)+getHex(self.g)+getHex(self.b))
        self.label3.setText(getHSL(self.r,self.g,self.b))
        self.StyleUI()


app = QApplication([])
view = ColorPick()
view.show()
app.exec_()

"""
Changelog:
1.0.1 - added hexadecimal conversion feature
      - hex conversion algorithm added math and pyswitch dependencies
      - made rgb and hex text selectable by mouse
1.0.2 - added labels for color sliders
      - put labels and color sliders in grid sub-layout
1.0.3 - added HSL conversion feature
      - fixed text staying black on dark colors
"""
