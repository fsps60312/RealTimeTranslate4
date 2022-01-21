from typing import Union
import wx

class MyTextCtrl(wx.TextCtrl):
    def __init__(self, parent: wx.Window, *args, **kwargs):
        font: Union[None, wx.Font] = kwargs.pop('font', None)
        tooltip: str = kwargs.pop('tooltip', None)
        hint: str = kwargs.pop('hint', None)
        wx.TextCtrl.__init__(self, parent, *args, **kwargs)
        if font is not None:
            self.SetFont(font)
        if tooltip is not None:
            self.SetToolTip(tooltip)
        if hint is not None:
            self.SetHint(hint)
