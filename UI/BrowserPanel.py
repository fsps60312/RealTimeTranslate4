import wx
import wx.html2
from UI.MyBoxSizer import MyBoxSizer

class BrowserPanel(wx.Panel):
    '''https://wxpython.org/Phoenix/docs/html/wx.html2.WebView.html#wx-html2-webview'''

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.__init_UI()

    def __init_UI(self):
        self.webview: wx.html2.WebView = wx.html2.WebView.New(self, url='http://codingsimplifylife.blogspot.tw/')
        self.sizer = MyBoxSizer(self, orient=wx.VERTICAL, addmany_list=[
            (self.webview, wx.SizerFlags(1).Expand())
        ])
    
    def LoadURL(self, url: str):
        self.webview.LoadURL(url)