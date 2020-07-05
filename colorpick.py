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
        layout = QVBoxLayout()
        self.red = QSlider(Qt.Horizontal)
        self.red.setMinimum(0)
        self.red.setMaximum(255)
        self.red.setValue(200)
        self.red.valueChanged.connect(self.changeRed)
        self.green = QSlider(Qt.Horizontal)
        self.green.setMinimum(0)
        self.green.setMaximum(255)
        self.green.setValue(200)
        self.green.valueChanged.connect(self.changeGreen)
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
        layout.addWidget(self.red)
        layout.addWidget(self.green)
        layout.addWidget(self.blue)
        layout.addWidget(self.label)
        layout.addWidget(self.label2)
        self._centralWidget.setLayout(layout)
    def StyleUI(self):
        self.style.setColor(QPalette.Window,QColor(self.r,self.g,self.b))
        self.textBrightness = int(255-(self.r+self.g+self.b)/3)
        self.style.setColor(QPalette.Text,QColor(self.textBrightness,self.textBrightness,self.textBrightness))
        app.setPalette(self.style)

    @pyqtSlot()
    def changeRed(self):
        self.r = self.red.value()
        self.label.setText("rgb("+str(self.r)+","+str(self.g)+","+str(self.b)+")")
        self.label2.setText("#"+getHex(self.r)+getHex(self.g)+getHex(self.b))
        self.StyleUI()
    def changeGreen(self):
        self.g = self.green.value()
        self.label.setText("rgb("+str(self.r)+","+str(self.g)+","+str(self.b)+")")
        self.label2.setText("#"+getHex(self.r)+getHex(self.g)+getHex(self.b))
        self.StyleUI()
    def changeBlue(self):
        self.b = self.blue.value()
        self.label.setText("rgb("+str(self.r)+","+str(self.g)+","+str(self.b)+")")
        self.label2.setText("#"+getHex(self.r)+getHex(self.g)+getHex(self.b))
        self.StyleUI()


app = QApplication([])
view = ColorPick()
view.show()
app.exec_()
