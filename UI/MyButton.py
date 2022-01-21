from typing import Tuple, Union
from datetime import datetime
import wx

class MyButton(wx.Button):
    def __init__(self, parent: wx.Window, *args, **kwargs):
        font: Union[None, wx.Font] = kwargs.pop('font', None)
        tooltip: str = kwargs.pop('tooltip', None)
        wx.Button.__init__(self, parent, *args, **kwargs)
        if font is not None:
            self.SetFont(font)
        if tooltip is not None:
            self.SetToolTip(tooltip)
    # def Flash(self, secs: float, color: Tuple[int, int, int]):
    #     self.ForegroundColour
    #     self.flash_info = (datetime.now(), secs, color)
    #     # self.original_backcolor = getattr(self, 'original_backcolor', (c:=self.BackgroundColour, c.Red(), c.Green(), c.Blue())[1:])
    #     self.original_forecolor = getattr(self, 'original_forecolor', (c:=self.ForegroundColour, c.Red(), c.Green(), c.Blue())[1:])
    #     # print('original_backcolor:', self.original_backcolor)
    #     print('original_forecolor:', self.original_forecolor)
    #     def handler(e: wx.IdleEvent):
    #         secs_elapsed = (datetime.now() - self.flash_info[0]).total_seconds()
    #         r = max(0.0, min(1.0, secs_elapsed / self.flash_info[1]))
    #         if r == 1.0:
    #             # self.BackgroundColour = wx.Colour(*self.original_backcolor)
    #             self.ForegroundColour = wx.Colour(*self.original_forecolor)
    #             # delattr(self, 'original_backcolor')
    #             delattr(self, 'original_forecolor')
    #             self.Unbind(wx.EVT_IDLE)
    #         else:
    #             # self.BackgroundColour = wx.Colour(*tuple(int(a + r * (b - a)) for a, b in zip(self.flash_info[2], self.original_backcolor)))
    #             self.ForegroundColour = wx.Colour(*tuple(int(a + r * (b - a)) for a, b in zip(self.flash_info[2], self.original_forecolor)))
    #     # self.BackgroundColour = wx.Colour(*self.flash_info[2])
    #     self.ForegroundColour = wx.Colour(*self.flash_info[2])
    #     self.Unbind(wx.EVT_IDLE)
    #     self.Bind(wx.EVT_IDLE, handler=handler)
