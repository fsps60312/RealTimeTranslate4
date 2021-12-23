from typing import Union
import wx

class MyButton(wx.Button):
    def __init__(self, parent: wx.Window, *args, **kwargs):
        font: Union[None, wx.Font] = kwargs.pop('font', None)
        wx.Button.__init__(self, parent, *args, **kwargs)
        if font is not None:
            self.SetFont(font)