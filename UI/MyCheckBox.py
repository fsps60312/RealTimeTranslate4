from typing import Union
import wx

class MyCheckBox(wx.CheckBox):
    def __init__(self, parent: wx.Window, *args, **kwargs):
        font: Union[None, wx.Font] = kwargs.pop('font', None)
        tooltip: str = kwargs.pop('tooltip', None)
        wx.CheckBox.__init__(self, parent, *args, **kwargs)
        if font is not None:
            self.SetFont(font)
        if tooltip is not None:
            self.SetToolTip(tooltip)
