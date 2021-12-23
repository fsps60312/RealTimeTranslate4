import wx
from UI.MainPanel import MainPanel

app = wx.App()

frame = wx.Frame(None, title='RealTimeTranslate4', size=(1000, 500))
frame.SetIcon(wx.Icon('main.ico'))
main_panel = MainPanel(frame)
frame.Show()

app.MainLoop()