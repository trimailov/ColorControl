import wx
import serial

class AppFrame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, parent=None, title=title, size=(400, 300))

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
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)

        self.slider_red = wx.Slider(self, -1, 50, 0, 100, (50, 10), (300, 20),
            wx.SL_HORIZONTAL)
        self.slider_amber = wx.Slider(self, -1, 50, 0, 100, (50, 60), (300, 20),
            wx.SL_HORIZONTAL)
        self.slider_green = wx.Slider(self, -1, 50, 0, 100, (50, 110), (300, 20),
            wx.SL_HORIZONTAL)
        self.slider_blue = wx.Slider(self, -1, 50, 0, 100, (50, 160), (300, 20),
            wx.SL_HORIZONTAL)



        self.Bind(wx.EVT_SLIDER, self.slider_update)

    def slider_update(self, event):
        self.pos_red = self.slider_red.GetValue()
        self.pos_amber = self.slider_amber.GetValue()
        self.pos_green = self.slider_green.GetValue()
        self.pos_blue = self.slider_blue.GetValue()

        str1 = "R = %d, A = %d, G = %d, B = %d" % (self.pos_red, 
                                                   self.pos_amber,
                                                   self.pos_green, 
                                                   self.pos_blue)

        frame.SetTitle(str1)

app = wx.App(True)
frame = AppFrame("ColorControl")
SliderPanel(frame, -1)
frame.Show(True)
app.MainLoop()