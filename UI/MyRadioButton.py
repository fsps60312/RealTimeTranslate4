from typing import Union
import wx

class MyRadioButton(wx.RadioButton):
    def __init__(self, parent: wx.Window, *args, **kwargs):
        font: Union[None, wx.Font] = kwargs.pop('font', None)
        wx.RadioButton.__init__(self, parent, *args, **kwargs)
        if font is not None:
            self.SetFont(font)