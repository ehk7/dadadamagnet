import wx
import lib.maes
from mqtt import MQTTManager
from mqtt import Status

class MainFrame(wx.Frame):
    """Main window"""
    def __init__(self, parent, title):
        self.devicestatus = Status.UNCALIBRATED
        super(MainFrame, self).__init__(parent, title=title, size=(600,500))
        self.panel = wx.Panel(self)

        #used to show calibration instructions
        self.txt1=None

        #status text
        self.txt2=None

        #create menus
        self.InitMenu()

        #add the widgets: calibration button, text
        self.InitWidgets()
        self.Centre()

        #display panel
        self.Show()

        #create instance of MQTT manager as a member of MainFrame
        self.mqtt = MQTTManager(self)

    def InitWidgets(self):
        self. txt1 = wx.StaticText(self.panel, pos=(10, 10), label="Attach the Smart Lock to your door, close and lock "
                                                                   "it, then click the button to start calibrating the sensor.")

        self.calibrationButton = wx.Button(self.panel, wx.ID_ANY, label='Calibrate: locked', size=(200, 30), pos=(200, 30))
        self.calibrationButton.Bind(wx.EVT_BUTTON, self.OnCalibrate)

    def DisplayStatus(self, status):
        if self.txt2==None:
            return 0
        elif int(status)==3:
            self.txt2.Label = "LOCKED"
        elif int(status)==4:
            self.txt2.Label = "CLOSED"
        elif int(status)==5:
            self.txt2.Label = "OPEN"

        self.Refresh()


    def OnCalibrate(self, event):
        #start calibration sequence
        if self.calibrationButton.Label=='Calibrate: locked':
            #send calibration instruction to device for locked status
            self.mqtt.publish("esys/dadada/userstatus","3")
            self.calibrationButton.Label="Calibrate: closed and Unlocked"

        elif self.calibrationButton.Label=="Calibrate: closed and Unlocked":
            # send calibration instruction to device for closed & unlocked status
            self.mqtt.publish("esys/dadada/userstatus", "4")
            print("calibrating closed")
            self.calibrationButton.Label = "Calibrate: unlocked and open"

        elif self.calibrationButton.Label=='Calibrate: unlocked and open':
            # send calibration instruction to device for door open status
            self.mqtt.publish("esys/dadada/userstatus", "5")

            #since last status of the door was open, default to open state
            self.devicestatus = Status.OPEN

            #remove calibration text and button
            self.calibrationButton.Show(False)
            self.txt1.Show(False)

            #create and display status text
            self.CreateStatusText()

            #subscribe to lock status messages
            #this will allow the information form the sensor to be shown in the app
            self.mqtt.client.subscribe("esys/dadada/status")

    def CreateStatusText(self):
        """Creates the status text used to display the locks state"""
        self.txt2 = wx.StaticText(self.panel, label="LOCKED", style=wx.ALIGN_CENTER)
        font = self.txt2.GetFont()
        font.SetPointSize(48)
        self.txt2.SetFont(font.Bold())
        self.txt2.SetForegroundColour("RED")

        #sizers are used to centre align the text
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox5.Add(self.txt2, wx.CENTER)
        vbox.Add(hbox5, flag=wx.CENTER | wx.TOP, border=45)

        self.panel.SetSizer(vbox)

        #refresh layout to ensure changes are displayed
        self.panel.Layout()
        self.Layout()

    def InitMenu(self):
        """Creates the 'file' menu"""
        filesMenu = wx.Menu()
        helpMenu = wx.Menu()

        #create the "quit" and "about" menu items
        aboutItem = helpMenu.Append(wx.ID_ABOUT)
        exitItem = filesMenu.Append(wx.ID_EXIT)

        #creat emenubar and add 'file' and 'help' menus
        menuBar = wx.MenuBar()
        menuBar.Append(filesMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        #set menubar as the menu for this frame
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        self.Close(True)

    def OnAbout(self, event):
        """Simple about prompt"""
        wx.MessageBox("This is an app demonstrating the Doora systems functionality.",
                      "About Doora", wx.OK|wx.ICON_INFORMATION)


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None, title = "Doora Demo")
    app.MainLoop()

