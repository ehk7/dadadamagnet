import wx
from enum import Enum
from mqtt import MQTTManager

class AppStatus(Enum):
    START=1
    OPEN=3
    UNLOCKED=4
    LOCKED=5

class MainFrame(wx.Frame):
    """Main window"""
    def __init__(self, parent, title):
        self.status = AppStatus.START
        super(MainFrame, self).__init__(parent, title=title, size=(600,500))
        self.panel = wx.Panel(self)
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)
        self.InitMenu()
        self.InitWidgets()

        self.Centre()
        self.Show()
        #self.mqtt = MQTTManager()

    def InitWidgets(self):
        self. txt1 = wx.StaticText(self.panel, pos=(10, 10), label="Attach the Smart Lock to your door, close and lock "
                                                                   "it, then click the button to start calibrating the sensor.")

        self.calibrationButton = wx.Button(self.panel, wx.ID_ANY, label='Calibrate: locked', size=(200, 30), pos=(200, 30))
        self.calibrationButton.Bind(wx.EVT_BUTTON, self.OnCalibrate)

    def DisplayStatus(self, status):
        pass

    def OnCalibrate(self, event):
        if self.calibrationButton.Label=='Calibrate: locked':
            print("Do calibration now for closed and locked")
            self.calibrationButton.Label="Calibrate: closed and Unlocked"

        elif self.calibrationButton.Label=="Calibrate: closed and Unlocked":
            print("Do calibration now for closed and unlocked")
            self.calibrationButton.Label = "Calibrate: unlocked and open"

        elif self.calibrationButton.Label=='Calibrate: unlocked and open':
            print("Do calibration now for open and unlocked")
            self.calibrationButton.Show(False)
            self.txt1.Label="Status:"
            font = self.txt1.GetFont()
            font.SetPointSize(24)
            self.txt1.SetFont(font.Bold())
            self.txt2 = wx.StaticText(self.panel, pos=(250, 220),
                                     label="LOCKED")
            font = self.txt2.GetFont()
            font.SetPointSize(24)
            self.txt2.SetFont(font.Bold())
            self.txt2.SetForegroundColour("RED")
            self.status=AppStatus.OPEN
        self.Refresh()


    def InitMenu(self):
        filesMenu = wx.Menu()
        helpMenu = wx.Menu()

        aboutItem = filesMenu.Append(wx.ID_ABOUT)
        exitItem = filesMenu.Append(wx.ID_EXIT)

        menuBar = wx.MenuBar()
        menuBar.Append(filesMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        self.Close(True)

    def OnAbout(self, event):
        wx.MessageBox("This is a demo app showing how the sensor can communicate with the user through MQTT",
                      "About DaDaDa", wx.OK|wx.ICON_INFORMATION)

    def DrawRing(self, dc, x, y, innerRadius, outerRadius, colour):
        dc.Clear()
        dc.SetPen(wx.Pen(colour))
        dc.SetBrush(wx.Brush(colour))
        dc.DrawCircle(x, y, outerRadius)

        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
        dc.DrawCircle(x, y, innerRadius)

        # paint open

    def OnPaint(self, event):
        dc = wx.PaintDC(event.GetEventObject())

        if self.status == AppStatus.OPEN:
            self.DrawRing(dc, 300, 250, 120, 150, "RED")

        elif self.status == AppStatus.UNLOCKED:
            self.DrawRing(dc, 300, 250, 120, 150, "YELLOW")

        elif self.status == AppStatus.LOCKED:
            self.DrawRing(dc, 300, 250, 120, 150, "GREEN")





if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None, title = "DaDaDa Demo")
    app.MainLoop()
    pass
