from typing import Optional
import wx
import wx.html2
import enum
import time
import threading
from datetime import datetime
from UI.BrowserPanel import BrowserPanel
from UI.MyBoxSizer import MyBoxSizer
from UI.MyGridBagSizer import MyGridBagSizer
from UI.MyRadioButton import MyRadioButton
from UI.MyButton import MyButton
from Utility.ClipboardListener import ClipboardListener
from Utility.TimeLock import TimeLock
from Utility.TranslateDirection import TranslateDirection
from Utility.strlib import is_chinese
from Utility.Translator import GoogleTranslate, BingTranslate, YahooDictionary
from Decorators.add_attrs import add_attrs

class TranslateProvider(enum.Enum):
    GoogleTranslate = enum.auto()
    BingTranslate = enum.auto()
    YahooDictionary = enum.auto()

class MainPanel(wx.Panel):

    class Settings:
        translate_direction = TranslateDirection.Auto
        translate_provider = TranslateProvider.GoogleTranslate
        keyword: str = ''
        
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.__clipboard_listener = ClipboardListener()
        self.__settings: MainPanel.Settings = MainPanel.Settings()
        self.__lasttime_change_title: Optional[datetime] = None
        self.__init_UI()
        self.__init_events()
    
    @staticmethod
    def GetUrl(settings: Settings) -> str:
        if settings.translate_provider == TranslateProvider.GoogleTranslate:
            return GoogleTranslate.Translate(settings.keyword, settings.translate_direction)
        elif settings.translate_provider == TranslateProvider.BingTranslate:
            return BingTranslate.Translate(settings.keyword, settings.translate_direction)
        elif settings.translate_provider == TranslateProvider.YahooDictionary:
            return YahooDictionary.Translate(settings.keyword, settings.translate_direction)
        else:
            raise NotImplementedError(settings.translate_provider)
    
    def __SetTitle(self, title: str, footprint: bool = True):
        self.TopLevelParent.SetTitle(title)
        if footprint:
            self.__lasttime_change_title = datetime.now()
    
    def __GetTitle(self) -> str:
        return self.TopLevelParent.GetTitle()

    def Refresh(self, *, keyword: Optional[str] = None,
                         translate_provider: Optional[TranslateProvider] = None,
                         translate_direction: Optional[TranslateDirection] = None):
        if keyword is not None:
            self.__settings.keyword = keyword
        if translate_provider is not None:
            self.__settings.translate_provider = translate_provider
        if translate_direction is not None:
            self.__settings.translate_direction = translate_direction
        self.TopLevelParent.SetTitle('⟳' + (s[:50] + '...' if len(s:=repr(self.__settings.keyword)[1:-1]) > 50 else s))
        url = self.GetUrl(self.__settings)
        self.browser_panel.LoadURL(url)

    def __init_events(self):
        # @add_attrs(timelock=TimeLock(0.5))
        def idle_event_listener():
            # timelock: TimeLock = idle_event_listener.timelock
            # if timelock.acquire():
            if True:
                if self.__lasttime_change_title is not None and (datetime.now() - self.__lasttime_change_title).total_seconds() > 1.0:
                    self.__SetTitle('☑'+self.__GetTitle()[1:], footprint=False)
                    self.__lasttime_change_title = None
                new_text = self.__clipboard_listener.check_text()
                if new_text is not None:
                    self.GetTopLevelParent().Raise()
                    self.text_entry.SetValue(new_text)
                    self.Refresh(keyword=new_text)
        # self.Bind(wx.EVT_IDLE, handler=idle_event_listener)
        def idle_event_backgroundloop():
            while True:
                wx.CallAfter(idle_event_listener)
                time.sleep(0.5)
        self.idle_event_backgroundthread = threading.Thread(target=idle_event_backgroundloop, daemon=True)
        self.idle_event_backgroundthread.start()
        self.browser_panel.webview.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, handler=lambda e: [self.__SetTitle('⏳'+self.__GetTitle()[1:])])
        self.browser_panel.webview.Bind(wx.html2.EVT_WEBVIEW_NAVIGATED, handler=lambda e: [self.__SetTitle('⌛'+self.__GetTitle()[1:])])
        self.browser_panel.webview.Bind(wx.html2.EVT_WEBVIEW_LOADED, handler=lambda e: [self.__SetTitle('✓'+self.__GetTitle()[1:])])
        self.browser_panel.webview.Bind(wx.html2.EVT_WEBVIEW_ERROR, handler=lambda e: [self.__SetTitle('⚠'+self.__GetTitle()[1:])])
        self.browser_panel.webview.Bind(wx.html2.EVT_WEBVIEW_NEWWINDOW, handler=lambda e: [self.__SetTitle('🆕'+self.__GetTitle()[1:])])
        self.browser_panel.webview.Bind(wx.html2.EVT_WEBVIEW_TITLE_CHANGED, handler=lambda e: [self.__SetTitle('✏'+self.__GetTitle()[1:])])
        self.google_translate_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler=lambda e: self.Refresh(translate_provider=TranslateProvider.GoogleTranslate))
        self.bing_translate_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler=lambda e: self.Refresh(translate_provider=TranslateProvider.BingTranslate))
        self.yahoo_dictionary_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler=lambda e: self.Refresh(translate_provider=TranslateProvider.YahooDictionary))
        self.translate_direction_Auto_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler=lambda e: self.Refresh(translate_direction=TranslateDirection.Auto))
        self.translate_direction_CE_radiobutton.Bind(wx.EVT_RADIOBUTTON, lambda e: self.Refresh(translate_direction=TranslateDirection.CE))
        self.translate_direction_EC_radiobutton.Bind(wx.EVT_RADIOBUTTON, lambda e: self.Refresh(translate_direction=TranslateDirection.EC))
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

        print('wx.DefaultSize:', wx.DefaultSize) # wx.DefaultSize
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

        self.google_translate_radiobutton.SetValue(True)
        self.translate_direction_Auto_radiobutton.SetValue(True)
