from cgitb import handler
from typing import Callable, List, Optional
import typing
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
from UI.MyCheckBox import MyCheckBox
from UI.MyTextCtrl import MyTextCtrl
from UI.MyButton import MyButton
from UI.MyTextCheckBox import MyTextCheckBox
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
        self.__expanded = False
        self.__init_UI()
        self.__init_events()
    
        def __start_backgroundloop(self: MainPanel):
            # idle loop to monitor clipboard change
            def idle_event_listener():
                if self.__lasttime_change_title is not None and (datetime.now() - self.__lasttime_change_title).total_seconds() > 1.0:
                    self.__SetTitle('☑' + self.__settings.keyword, footprint=False)
                    self.__lasttime_change_title = None
                new_text = self.__clipboard_listener.check_text()
                if new_text is not None:
                    self.__SetTitle('📋' + new_text, footprint=False)
                    if self.keyword_textcheckbox.checkbox.IsChecked():
                        self.GetTopLevelParent().Raise()
                        self.keyword_textcheckbox.textctrl.ChangeValue(new_text) # SetValue send EVT_TEXT event, while ChangeValue not
                        self.Navigate(keyword=new_text)
            def idle_event_backgroundloop():
                while True:
                    wx.CallAfter(idle_event_listener)
                    time.sleep(0.5)
            self.idle_event_backgroundthread = threading.Thread(target=idle_event_backgroundloop, daemon=True)
            self.idle_event_backgroundthread.start()
        __start_backgroundloop(self)

    def __init_UI(self):
        font = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        small_font = wx.Font(7, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        self.control_panel = wx.Panel(self)
        self.keyword_textcheckbox = MyTextCheckBox(self,
            MyTextCtrl(self, font=font, tooltip='keyword', hint='keyword', size=(0, -1), style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE), # |wx.HSCROLL
            MyCheckBox(self, font=font, tooltip='=📋 sync with clipboard', label='=📋', size=(-1, -1)),
            (wx.SizerFlags(1).Expand(), wx.SizerFlags(0).Expand()))
        self.keyword_textcheckbox.checkbox.SetValue(True)
        self.translate_provider_panel = wx.Panel(self)
        self.translate_direction_panel = wx.Panel(self)
        self.expand_button = MyButton(self, font=font, tooltip='︾ unfold', label='︾', size=(0, -1))

        self.extra_panel = wx.Panel(self)
        self.refresh_button = MyButton(self, font=font, tooltip='⟳ refresh', label='⟳', size=(0, -1))
        self.go_bwd_button = MyButton(self, font=font, tooltip='← go backward', label='←', size=(0, -1))
        self.go_fwd_button = MyButton(self, font=font, tooltip='→ go forward', label='→', size=(0, -1))
        self.url_textctrl = MyTextCtrl(self, font=font, tooltip='current URL', size=(0, -1), style=wx.TE_PROCESS_ENTER)

        self.browser_panel = BrowserPanel(self)

        print('wx.DefaultSize:', wx.DefaultSize) # wx.DefaultSize
        self.google_translate_radiobutton = MyRadioButton(self, font=font, tooltip='Google Translate', label='Google', size=(0, -1), style=wx.RB_GROUP)
        self.bing_translate_radiobutton = MyRadioButton(self, font=font, tooltip='Bing Translate', label='Bing', size=(0, -1))
        self.yahoo_dictionary_radiobutton = MyRadioButton(self, font=font, tooltip='Yahoo Dictionary', label='Yahoo', size=(0, -1))

        self.translate_direction_CE_radiobutton = MyRadioButton(self, font=small_font, tooltip='CE (Chinese to English)', label='CE', size=(0, 0), style=wx.RB_GROUP)
        self.translate_direction_EC_radiobutton = MyRadioButton(self, font=small_font, tooltip='EC (English to Chinese)', label='EC', size=(0, 0))
        self.translate_direction_Auto_radiobutton = MyRadioButton(self, font=small_font, tooltip='CE if there are any Chinese characters: [\\u4e00-\\u9fff]\nEC otherwise', label='Auto', size=(0, 0))

        # self.button = wx.Button(self, label='I\'m button')

        def __init_UI_layout(self: MainPanel):
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
                (self.keyword_textcheckbox, (0, 0, 1, 4)),
                (self.translate_provider_panel, (0, 4, 1, 2)),
                (self.translate_direction_panel, (0, 6)),
                (self.expand_button, (0, 7))
            ])
            
            self.extra_panel.sizer = MyGridBagSizer(self.extra_panel, 1, 12, addmany_list=[
                (self.refresh_button, (0, 0)),
                (self.go_bwd_button, (0, 1)),
                (self.go_fwd_button, (0, 2)),
                (self.url_textctrl, (0, 3, 1, 9)),
            ])

            self.google_translate_radiobutton.SetValue(True)
            self.translate_direction_Auto_radiobutton.SetValue(True)

            self.__set_expanded(False)
        __init_UI_layout(self)
    
    def __set_expanded(self, expanded: Optional[bool] = None):
        if expanded is None:
            expanded = not self.__expanded
        self.__expanded = expanded
        if self.__expanded:
            self.extra_panel.Show()
            self.sizer = MyBoxSizer(self, orient=wx.VERTICAL, addmany_list=[
                (self.control_panel, wx.SizerFlags(0).Expand()),
                (self.extra_panel, wx.SizerFlags(0).Expand()),
                (self.browser_panel, wx.SizerFlags(1).Expand())
            ])
            self.expand_button.SetLabel('︽')
            self.expand_button.SetToolTip('︽ fold')
        else:
            self.extra_panel.Hide()
            self.sizer = MyBoxSizer(self, orient=wx.VERTICAL, addmany_list=[
                (self.control_panel, wx.SizerFlags(0).Expand()),
                (self.browser_panel, wx.SizerFlags(1).Expand())
            ])
            self.expand_button.SetLabel('︾')
            self.expand_button.SetToolTip('︾ unfold')
        self.Layout()

    def __init_events(self):
        def __init_events_from_control_panel(self: MainPanel):
            self.keyword_textcheckbox.textctrl.Bind(wx.EVT_TEXT_ENTER, handler=lambda e: self.Navigate(keyword=e.GetString()))
            self.keyword_textcheckbox.textctrl.Bind(wx.EVT_TEXT, handler=lambda e: self.keyword_textcheckbox.checkbox.SetValue(False))
            self.expand_button.Bind(wx.EVT_BUTTON, handler=lambda e: self.__set_expanded())

            def keyword_checkbox_handler(e: wx.CommandEvent):
                self.keyword_textcheckbox.checkbox.SetToolTip('=📋 sync with clipboard' if e.GetInt() == 1 else '=📋 don\'t sync with clipboard')
                if e.GetInt() == 1:
                    keyword: str = self.__clipboard_listener.CachedText or ''
                    self.keyword_textcheckbox.textctrl.ChangeValue(keyword) # SetValue send EVT_TEXT event, while ChangeValue not
                    self.Navigate(keyword=keyword)
            self.keyword_textcheckbox.checkbox.Bind(wx.EVT_CHECKBOX, handler=keyword_checkbox_handler)
        __init_events_from_control_panel(self)

        def __init_events_from_extra_panel(self: MainPanel):
            self.go_bwd_button.Bind(wx.EVT_BUTTON, handler=lambda e: [
                print('CanGoBack:', v:=self.browser_panel.webview.CanGoBack(),
                self.browser_panel.webview.BackwardHistory), # CanGoBack: True [<wx._html2.WebViewHistoryItem object at 0x000002D2B762D820>]
                v and self.browser_panel.webview.GoBack()]) # or self.go_bwd_button.Flash(3.0, (255, 0, 0))
            self.go_fwd_button.Bind(wx.EVT_BUTTON, handler=lambda e: [
                print('CanGoForward:', v:=self.browser_panel.webview.CanGoForward(),
                self.browser_panel.webview.ForwardHistory), # CanGoForward: True [<wx._html2.WebViewHistoryItem object at 0x000002D2B762D820>]
                v and self.browser_panel.webview.GoForward()]) # or self.go_fwd_button.Flash(3.0, (255, 0, 0))
            self.refresh_button.Bind(wx.EVT_BUTTON, handler=lambda e: self.browser_panel.webview.Reload(flags=wx.html2.WEBVIEW_RELOAD_NO_CACHE))
            self.url_textctrl.Bind(wx.EVT_TEXT_ENTER, handler=lambda e: self.browser_panel.webview.LoadURL(e.GetString() or 'http://codingsimplifylife.blogspot.tw/'))
        __init_events_from_extra_panel(self)

        def __init_events_from_translate_radiobuttons(self: MainPanel):
            # translate option events
            def handler_gen(nav):
                def handler(e: wx.CommandEvent):
                    b: MyRadioButton = e.GetEventObject()
                    # b.Flash(1.0, (0, 0, 255))
                    nav()
                return handler
            self.google_translate_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler=handler_gen(lambda: self.Navigate(translate_provider=TranslateProvider.GoogleTranslate)))
            self.bing_translate_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler=handler_gen(lambda: self.Navigate(translate_provider=TranslateProvider.BingTranslate)))
            self.yahoo_dictionary_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler=handler_gen(lambda: self.Navigate(translate_provider=TranslateProvider.YahooDictionary)))
            self.translate_direction_Auto_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler=handler_gen(lambda: self.Navigate(translate_direction=TranslateDirection.Auto)))
            self.translate_direction_CE_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler_gen(lambda: self.Navigate(translate_direction=TranslateDirection.CE)))
            self.translate_direction_EC_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler_gen(lambda: self.Navigate(translate_direction=TranslateDirection.EC)))
        __init_events_from_translate_radiobuttons(self)

        def __init_events_from_webview(self: MainPanel):
            # browser panel events
            def handler_gen(prefix: str, *, goto_URL: bool = False) -> Callable[[wx.html2.WebViewEvent], None]:
                def handler(e: wx.html2.WebViewEvent):
                    self.refresh_button.SetToolTip('⟳ refresh\n\n%s\n%s' % (self.browser_panel.webview.CurrentTitle, self.browser_panel.webview.CurrentURL))

                    # self.go_bwd_button.Enable(self.browser_panel.webview.CanGoBack())
                    h: List[wx.html2.WebViewHistoryItem] = self.browser_panel.webview.BackwardHistory
                    self.go_bwd_button.SetToolTip('← go backward%s\n%s' % (' (%d)' % len(h) if len(h) else '', (h[-1].Title + '\n' + h[-1].Url) if len(h) else '🛈 No backward history'))

                    # self.go_fwd_button.Enable(self.browser_panel.webview.CanGoForward())
                    h: List[wx.html2.WebViewHistoryItem] = self.browser_panel.webview.ForwardHistory
                    self.go_fwd_button.SetToolTip('→ go forward%s\n%s' % (' (%d)' % len(h) if len(h) else '', (h[0].Title + '\n' + h[0].Url) if len(h) else '🛈 No forward history'))
                    
                    self.__SetTitle(prefix + (e.GetTarget() or e.GetURL()))
                    self.url_textctrl.SetValue(self.browser_panel.webview.CurrentURL)
                    self.url_textctrl.SetToolTip('You\'re now at:\n%s\n%s' % (self.browser_panel.webview.CurrentTitle, self.browser_panel.webview.CurrentURL))
                    if goto_URL:
                        self.browser_panel.webview.LoadURL(e.GetURL())
                return handler

            self.browser_panel.webview.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, handler=handler_gen('⏳'))
            self.browser_panel.webview.Bind(wx.html2.EVT_WEBVIEW_NAVIGATED, handler=handler_gen('⌛'))
            self.browser_panel.webview.Bind(wx.html2.EVT_WEBVIEW_LOADED, handler=handler_gen('✓'))
            self.browser_panel.webview.Bind(wx.html2.EVT_WEBVIEW_ERROR, handler=handler_gen('⚠'))
            self.browser_panel.webview.Bind(wx.html2.EVT_WEBVIEW_NEWWINDOW, handler=handler_gen('🆕', goto_URL=True))
            self.browser_panel.webview.Bind(wx.html2.EVT_WEBVIEW_TITLE_CHANGED, handler=handler_gen('✏'))
        __init_events_from_webview(self)
    
    def __SetTitle(self, title: str, footprint: bool = True):
        self.TopLevelParent.SetTitle(title)
        if footprint:
            self.__lasttime_change_title = datetime.now()
    
    def __GetTitle(self) -> str:
        return self.TopLevelParent.GetTitle()

    
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

    def Navigate(self, *, keyword: Optional[str] = None,
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
        self.url_textctrl.ChangeValue(url)
        self.browser_panel.LoadURL(url)
