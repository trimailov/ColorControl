import wx
import serial

class MainFrame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, parent=None, title=title, size=(600, 400))

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

        self.sliderRed = wx.Slider(self, -1, 5000, 1000, 9999,
                                    (20, 20), (560, 20), wx.SL_HORIZONTAL)
        self.sliderAmber = wx.Slider(self, -1, 5000, 1000, 9999,
                                      (20, 70), (560, 20), wx.SL_HORIZONTAL)
        self.sliderGreen = wx.Slider(self, -1, 5000, 1000, 9999,
                                      (20, 120), (560, 20), wx.SL_HORIZONTAL)
        self.sliderBlue = wx.Slider(self, -1, 5000, 1000, 9999,
                                     (20, 170), (560, 20), wx.SL_HORIZONTAL)

        self.Bind(wx.EVT_SLIDER, self.sliderUpdate)

    def sliderUpdate(self, event):
        self.posRed = self.sliderRed.GetValue()
        self.posAmber = self.sliderAmber.GetValue()
        self.posGreen = self.sliderGreen.GetValue()
        self.posBlue = self.sliderBlue.GetValue()

        string = ':0104 %i %i %i %i\r\n' % (self.posRed, self.posGreen, self.posBlue, self.posAmber)

        self.ser.write(string)
        self.ser.flush()
        print string

    def lampOn(self, event):
        self.ser = serial.Serial(port='/dev/tty.LUME20R_130426-DevB', timeout=1)
        if self.ser.open == False:
            self.ser.open()

    def lampZero(self, event):
        if self.ser.isOpen():
            self.ser.write(':0104 0000 0000 0000 0000\r\n')

def main():
    app = wx.App(True)
    frame = MainFrame("ColorControl")
    frame.Show(True)
    app.MainLoop()

if __name__ == "__main__":
    main()