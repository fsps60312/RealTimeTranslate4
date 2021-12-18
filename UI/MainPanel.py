import wx
from UI.BrowserPanel import BrowserPanel
from UI.MyBoxSizer import MyBoxSizer

class MainPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.__init_UI()
        self.__init_events()

    def __init_events(self):
        self.button.Bind(wx.EVT_BUTTON, lambda e: [
            w:=self.text_entry.GetValue(),
            self.TopLevelParent.SetTitle(w),
            self.browser_panel.LoadURL(w)])
    
    def __init_UI(self):
        self.control_panel = wx.Panel(self)

        self.text_entry = wx.TextCtrl(self)
        self.button = wx.Button(self, label='I\'m button')

        self.browser_panel = BrowserPanel(self)

        self.control_panel.sizer = MyBoxSizer(self.control_panel, orient=wx.HORIZONTAL, addmany_list=[
            (self.text_entry, wx.SizerFlags(1).Expand()),
            (self.button, wx.SizerFlags(0).Expand())
        ])
        
        self.sizer = MyBoxSizer(self, orient=wx.VERTICAL, addmany_list=[
            (self.control_panel, wx.SizerFlags(0).Expand()),
            (self.browser_panel, wx.SizerFlags(1).Expand())
        ])