import wx
import serial
import time

class AppFrame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, parent=None, title=title, size=(600, 400))

        filemenu = wx.Menu()

        filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)

    def on_close(self, event):
        self.Destroy()


class SliderPanel(wx.Panel):
    lamp = serial.Serial()

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)

        self.slider_red = wx.Slider(self, -1, 5000, 0, 9999, (10, 10), (580, 20),
            wx.SL_HORIZONTAL)
        self.slider_amber = wx.Slider(self, -1, 5000, 0, 9999, (10, 60), (580, 20),
            wx.SL_HORIZONTAL)
        self.slider_green = wx.Slider(self, -1, 5000, 0, 9999, (10, 110), (580, 20),
            wx.SL_HORIZONTAL)
        self.slider_blue = wx.Slider(self, -1, 5000, 0, 9999, (10, 160), (580, 20),
            wx.SL_HORIZONTAL)
        self.buttonConnect = wx.Button(self, -1, label="open port", pos=(10, 210))
        self.buttonSend = wx.Button(self, -1, label="send value", pos=(10, 250))

        self.Bind(wx.EVT_SLIDER, self.sliderUpdate)
        self.Bind(wx.EVT_BUTTON, self.onButton)

    def sliderUpdate(self, event):
        self.pos_red = self.slider_red.GetValue()
        self.pos_amber = self.slider_amber.GetValue()
        self.pos_green = self.slider_green.GetValue()
        self.pos_blue = self.slider_blue.GetValue()

        str1 = "R = %d, A = %d, G = %d, B = %d" % (self.pos_red, 
                                                   self.pos_amber,
                                                   self.pos_green, 
                                                   self.pos_blue)

        send_string = ':0104 %i %i %i %i\r\n' % (self.pos_red, 
                                                 self.pos_amber,
                                                 self.pos_green, 
                                                 self.pos_blue)
        if self.lamp.isOpen():
            self.lamp.write(send_string)
            time.sleep(0.001)

        frame.SetTitle(str1)

    def onButton(self, event):
        self.lamp.port = '/dev/tty.LUME20R_130426-DevB'
        self.lamp.timeout = 1

app = wx.App(True)
frame = AppFrame("ColorControl")
SliderPanel(frame, -1)
frame.Show(True)
app.MainLoop()