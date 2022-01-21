from multiprocessing import Value
from typing import Tuple, Union
import wx
from UI.MyTextCtrl import MyTextCtrl
from UI.MyCheckBox import MyCheckBox
from UI.MyBoxSizer import MyBoxSizer

class MyTextCheckBox(wx.Panel):
    def __init__(self, parent: wx.Window, textctrl: wx.TextCtrl, checkbox: wx.CheckBox, boxsizer_flags: Tuple[wx.SizerFlags, wx.SizerFlags], *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.textctrl = textctrl
        self.checkbox = checkbox
        self.sizer = MyBoxSizer(self, wx.HORIZONTAL, [
            (self.textctrl, boxsizer_flags[0]),
            (self.checkbox, boxsizer_flags[1]),
        ])

    # @property
    # def Text(self) -> str:
    #     return self.textctrl.Value
    # @Text.setter
    # def Text(self, new_value: str):
    #     self.textctrl.SetValue(new_value)
    
    # @property
    # def Checked(self) -> bool:
    #     return self.checkbox.GetValue()
    # @Checked.setter
    # def Checked(self, new_value: bool):
    #     self.checkbox.SetValue(new_value)