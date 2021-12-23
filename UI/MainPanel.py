import wx
from wx.core import HORIZONTAL
from UI.BrowserPanel import BrowserPanel
from UI.MyBoxSizer import MyBoxSizer
from UI.MyGridBagSizer import MyGridBagSizer
from UI.MyRadioButton import MyRadioButton
from UI.MyButton import MyButton


class MainPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.__init_UI()
        self.__init_events()

    def __init_events(self):
        return
        self.button.Bind(wx.EVT_BUTTON, lambda e: [
            w:=self.text_entry.GetValue(),
            self.TopLevelParent.SetTitle(w),
            self.browser_panel.LoadURL(w)])
    
    def __init_UI(self):
        font = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        small_font = wx.Font(7, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        self.control_panel = wx.Panel(self)
        self.text_entry = wx.TextCtrl(self, size=(0, -1))
        self.translate_provider_panel = wx.Panel(self)
        self.translate_direction_panel = wx.Panel(self)
        self.expand_button = MyButton(self, label='︾Expand', font=font, size=(0, 0))
        self.browser_panel = BrowserPanel(self)

        self.google_translate_radiobutton = MyRadioButton(self, label='Google', font=font, size=(0, -1), style=wx.RB_GROUP)
        self.bing_translate_radiobutton = MyRadioButton(self, label='Bing', font=font, size=(0, -1))
        self.yahoo_dictionary_radiobutton = MyRadioButton(self, label='Yahoo', font=font, size=(0, -1))

        self.translate_direction_CE_radiobutton = MyRadioButton(self, label='CE', font=small_font, size=(0, 0), style=wx.RB_GROUP)
        self.translate_direction_EC_radiobutton = MyRadioButton(self, label='EC', font=small_font, size=(0, 0))
        self.translate_direction_Auto_radiobutton = MyRadioButton(self, label='Auto', font=small_font, size=(0, 0))

        # self.button = wx.Button(self, label='I\'m button')

        self.translate_provider_panel.sizer = MyGridBagSizer(self.translate_provider_panel, 1, 3, addmany_list=[
            (self.google_translate_radiobutton, (0, 0)),
            (self.bing_translate_radiobutton, (0, 1)),
            (self.yahoo_dictionary_radiobutton, (0, 2))
        ])

        self.translate_direction_panel.sizer = MyGridBagSizer(self.translate_direction_panel, 2, 2, addmany_list=[
            (self.translate_direction_CE_radiobutton, (0, 0)),
            (self.translate_direction_EC_radiobutton, (0, 1)),
            (self.translate_direction_Auto_radiobutton, (1, 0, 1, 2))
        ])

        self.control_panel.sizer = MyGridBagSizer(self.control_panel, 1, 8, addmany_list=[
            (self.text_entry, (0, 0, 1, 4)),
            (self.translate_provider_panel, (0, 4, 1, 2)),
            (self.translate_direction_panel, (0, 6)),
            (self.expand_button, (0, 7))
        ])
        
        self.sizer = MyBoxSizer(self, orient=wx.VERTICAL, addmany_list=[
            (self.control_panel, wx.SizerFlags(0).Expand()),
            (self.browser_panel, wx.SizerFlags(1).Expand())
        ])
