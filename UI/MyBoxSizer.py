from typing import List, Literal, Tuple, Union
import wx

class MyBoxSizer(wx.BoxSizer):
    def __init__(self, parent: wx.Window, orient, addmany_list: List[Tuple[Union[wx.Window, Tuple[int, int]], wx.SizerFlags]]):
        wx.BoxSizer.__init__(self, orient=orient)
        for w, f in addmany_list:
            if isinstance(w, wx.Window):
                w.Reparent(parent)
        self.AddMany(addmany_list)
        parent.SetSizer(self)