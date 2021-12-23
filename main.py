import wx
from UI.MainPanel import MainPanel

app = wx.App()

frame = wx.Frame(None, title='RealTimeTranslate4', size=(800, 400))
main_panel = MainPanel(frame)
frame.Show()

app.MainLoop()