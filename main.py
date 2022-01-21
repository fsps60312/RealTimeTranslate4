import Utility.SingleInstanceChecker
if Utility.SingleInstanceChecker.OtherProcessExists():
    print('exit because other instance running.')
    exit()

import wx
import pathlib
from UI.MainPanel import MainPanel

app = wx.App()

frame = wx.Frame(None, title='RealTimeTranslate4', size=(1000, 500))
frame.SetIcon(wx.Icon('main.ico'))

def close_handler(e: wx.CloseEvent):
    pathlib.Path(Utility.SingleInstanceChecker.filename).unlink(missing_ok=True)
    e.Skip()
frame.Bind(wx.EVT_CLOSE, handler=close_handler)

main_panel = MainPanel(frame)
frame.Show()

app.MainLoop()