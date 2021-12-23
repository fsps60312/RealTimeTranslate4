from typing import List, Tuple, Union
import wx

class MyGridBagSizer(wx.GridBagSizer):
    def __init__(self, parent: wx.Window, n_rows: int, n_cols: int, *args, addmany_list: List[Tuple[Union[wx.Window, Tuple[int, int]], Union[Tuple[int, int], Tuple[int, int, int, int]]]], **kwargs):
        wx.GridBagSizer.__init__(self, *args, **kwargs)
        for w, f in addmany_list:
            if isinstance(w, wx.Window):
                w.Reparent(parent)
            self.Add(w, wx.GBPosition(*f[:2]), wx.GBSpan(*(f[2:] or (1, 1))), wx.EXPAND)
        for i in range(n_rows):
            self.AddGrowableRow(i)
        for i in range(n_cols):
            self.AddGrowableCol(i)
        parent.SetSizer(self)