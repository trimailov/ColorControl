"""
LUME20R GUI control software

Tristimulus values of RAGB chanels
RED: X=44176 Y=19107 Z=00344
AMBER: X=44823 Y=33499 Z=00481
GREEN: X=08102 Y=33309 Z=07899
BLUE: X=17664 Y=04212 Z=92900

Planckian lockus formula:
X (1667K < T < 4000K) = -0.2661239e9 / T ** 3 - 0.234358e6 / T ** 2 + 0.8776956e3 / T + 0.17991
X (4000K < T < 25000K) = -3.0258469e9 / T ** 3 + 2.1070379e6 / T ** 2 + 0.2226347e3 / T + 0.24039

Y (1667K < T < 2222K) = -1.1063814 * X ** 3 - 1.3481102 * X ** 2 + 2.18555832 * X - 0.20219683
Y (2222K < T < 4000K) = -0.9549476 * X ** 3 - 1.37418593 * X ** 2 + 2.09137015 * X - 0.16748867
Y (4000K < T < 25000K) = 3.081758 * X ** 3 - 5.8733867 * X ** 2 + 3.75112997 * X - 0.37001483

"""

import wx
import serial

class MainFrame(wx.Frame):

    ser = serial.Serial()

    def __init__(self, title):
        frame = wx.Frame.__init__(self, parent=None, title=title, size=(600, 400))

        filemenu = wx.Menu()

        filemenu.Append(wx.ID_ABOUT, "&About", "Information about this program.")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program.")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)

        self.buttonLampOn = wx.Button(self, label="Connect to lamp", pos=(10, 340))
        self.buttonLampZero = wx.Button(self, label="Intensity 0", pos=(10, 300))

        self.Bind(wx.EVT_BUTTON, self.lampOn, self.buttonLampOn)
        self.Bind(wx.EVT_BUTTON, self.lampZero, self.buttonLampZero)

        self.sliderRed = wx.Slider(self, -1, 5000, 0, 9999,
                                    (20, 50), (560, 20), 
                                    wx.SL_HORIZONTAL, name="RED")
        self.sliderAmber = wx.Slider(self, -1, 5000, 0, 9999,
                                    (20, 100), (560, 20), 
                                    wx.SL_HORIZONTAL, name="AMBER")
        self.sliderGreen = wx.Slider(self, -1, 5000, 0, 9999,
                                    (20, 150), (560, 20), 
                                    wx.SL_HORIZONTAL, name="GREEN")
        self.sliderBlue = wx.Slider(self, -1, 5000, 0, 9999,
                                    (20, 200), (560, 20), 
                                    wx.SL_HORIZONTAL, name="BLUE")
        self.sliderTemp = wx.Slider(self, -1, 2000, 2000, 10000,
                                    (20, 250), (560, 20),
                                    wx.SL_HORIZONTAL, name="TEMP")

        self.txtRed = wx.StaticText(self, label="RED", pos=(20, 30))
        self.txtAmber = wx.StaticText(self, label="AMBER", pos=(20, 80))
        self.txtGreen = wx.StaticText(self, label="GREEN", pos=(20, 130))
        self.txtBlue = wx.StaticText(self, label="BLUE", pos=(20, 180))
        self.txtTemp = wx.StaticText(self, label="TEMPERATURE", pos=(20, 230))

        self.Bind(wx.EVT_SLIDER, self.sliderUpdate)
        self.Bind(wx.EVT_SLIDER, self.sliderTempUpdate, self.sliderTemp)

    def sliderUpdate(self, event):
        self.posRed = lamp_string(self.sliderRed.GetValue())
        self.posAmber = lamp_string(self.sliderAmber.GetValue())
        self.posGreen = lamp_string(self.sliderGreen.GetValue())
        self.posBlue = lamp_string(self.sliderBlue.GetValue())

        print self.posRed, self.posAmber, self.posGreen, self.posBlue

        string = ':0104 %s %s %s %s\r\n' % (self.posRed, self.posGreen, self.posBlue, self.posAmber)

        if self.ser.isOpen():
            self.ser.write(string)
            self.ser.flush()
        print string

    def sliderTempUpdate(self, event):
        temp = self.sliderTemp.GetValue()
        if temp >= 1667 and temp < 2222:
            x = (-0.2661239e9 / (temp ** 3)) - (0.234358e6 / (temp ** 2)) + (0.8776956e3 / temp) + 0.17991
            y = (-1.1063814 * (x ** 3)) - (1.3481102 * (x ** 2)) + (2.18555832 * x) - 0.20219683
        elif temp >= 2222 and temp < 4000:
            x = (-0.2661239e9 / (temp ** 3)) - (0.234358e6 / (temp ** 2)) + (0.8776956e3 / temp) + 0.17991
            y = (-0.9549476 * (x ** 3)) - (1.37418593 * (x ** 2)) + (2.09137015 * x) - 0.16748867
        elif temp >= 4000 and temp < 25000:
            x = (-3.0258469e9 / (temp ** 3)) + (2.1070379e6 / (temp ** 2)) + (0.2226347e3 / temp) + 0.24039
            y = (3.081758 * (x ** 3)) - (5.8733867 * (x ** 2)) + (3.75112997 * x) - 0.37001483
        print temp, 'K', (x, y)

    def lampOn(self, event):
        self.ser = serial.Serial(port='/dev/tty.LUME20R_130426-DevB', timeout=1)
        if self.ser.open == False:
            self.ser.open()

    def lampZero(self, event):
        if self.ser.isOpen():
            self.ser.write(':0104 0000 0000 0000 0000\r\n')
            self.sliderRed.SetValue(0)
            self.sliderAmber.SetValue(0)
            self.sliderGreen.SetValue(0)
            self.sliderBlue.SetValue(0)

# sets a string form a number according to lamps communication protocol
# eg. int(48) -> str(0048)
def lamp_string(number):
    string = str(number)
    while(len(string) < 4):
        string = '0' + string
    return string

def main():
    app = wx.App(redirect=True, filename="log.txt")
    frame = MainFrame("ColorControl")
    frame.Show(True)
    app.MainLoop()

if __name__ == "__main__":
    main()