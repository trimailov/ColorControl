import wx

class SliderPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)

        self.slider_red = wx.Slider(self, -1, 50, 0, 100, (50, 50), (300, 20),
            wx.SL_HORIZONTAL)
        self.slider_amber = wx.Slider(self, -1, 50, 0, 100, (50, 100), (300, 20),
            wx.SL_HORIZONTAL)
        self.slider_green = wx.Slider(self, -1, 50, 0, 100, (50, 150), (300, 20),
            wx.SL_HORIZONTAL)
        self.slider_blue = wx.Slider(self, -1, 50, 0, 100, (50, 200), (300, 20),
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
frame = wx.Frame(None, -1, "Sliders", size=(400, 300))
SliderPanel(frame, -1)
frame.Show(True)
app.MainLoop()