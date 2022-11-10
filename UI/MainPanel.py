from typing import Callable, List, Optional
import wx
import wx.html2
import time
import threading
import pathlib
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
from Utility.Translator import Abbreviation, GoogleTranslate, Translator, YahooDictionary, Wikitionary
import Utility.SingleInstanceChecker

class MainPanel(wx.Panel):
    
    def __SetTitle(self, title: str, footprint: bool = True):
        self.TopLevelParent.SetTitle(title)
        if footprint:
            self.__lasttime_change_title = datetime.now()
    
    def __GetTitle(self) -> str:
        return self.TopLevelParent.GetTitle()
    
    def __Raise(self):
        f: wx.Frame = self.GetTopLevelParent()
        f.Iconize(iconize=False)
        if not f.HasFlag(wx.STAY_ON_TOP):
            f.ToggleWindowStyle(wx.STAY_ON_TOP)
        f.Raise()
        if f.HasFlag(wx.STAY_ON_TOP):
            f.ToggleWindowStyle(wx.STAY_ON_TOP)

    class Settings:
        last_selected_translate_direction: str = ""
        translator: Translator = GoogleTranslate
        keyword: str = ""
        
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
                try:
                    pathlib.Path(Utility.SingleInstanceChecker.touchname).unlink(missing_ok=False)
                    self.__Raise() # touchfile exists. This means there are other invocations found me existing, and need me to raise up instead.
                except FileNotFoundError:
                    pass
                if self.__lasttime_change_title is not None and (datetime.now() - self.__lasttime_change_title).total_seconds() > 1.0:
                    self.__SetTitle('☑' + self.__settings.keyword, footprint=False)
                    self.__lasttime_change_title = None
                new_text = self.__clipboard_listener.check_text()
                if new_text is not None:
                    self.__SetTitle('📋' + new_text, footprint=False)
                    if self.keyword_textcheckbox.checkbox.IsChecked():
                        self.__Raise()
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
        self.yahoo_dictionary_radiobutton = MyRadioButton(self, font=font, tooltip='Yahoo Dictionary', label='Yahoo', size=(0, -1))
        self.wikitionary_radiobutton = MyRadioButton(self, font=font, tooltip='Wiktionary', label='Wiktionary', size=(0, -1))
        self.abbreviation_radiobutton = MyRadioButton(self, font=font, tooltip='www.abbreviation.com', label='Abbreviation', size=(0, -1))

        self.translate_direction_radiobuttons: List[MyRadioButton] = []

        def __init_UI_layout(self: MainPanel):
            self.translate_provider_panel.sizer = MyGridBagSizer(self.translate_provider_panel, 1, 10, addmany_list=[
                (self.google_translate_radiobutton, (0, 0, 1, 2)),
                (self.yahoo_dictionary_radiobutton, (0, 2, 1, 2)),
                (self.wikitionary_radiobutton, (0, 4, 1, 3)),
                (self.abbreviation_radiobutton, (0, 7, 1, 3))
            ])

            self.control_panel.sizer = MyGridBagSizer(self.control_panel, 1, 16, addmany_list=[
                (self.keyword_textcheckbox, (0, 0, 1, 8)),
                (self.translate_provider_panel, (0, 8, 1, 5)),
                (self.translate_direction_panel, (0, 13, 1, 2)),
                (self.expand_button, (0, 15))
            ])
            
            self.extra_panel.sizer = MyGridBagSizer(self.extra_panel, 1, 12, addmany_list=[
                (self.refresh_button, (0, 0)),
                (self.go_bwd_button, (0, 1)),
                (self.go_fwd_button, (0, 2)),
                (self.url_textctrl, (0, 3, 1, 9)),
            ])

            self.google_translate_radiobutton.SetValue(True)
            self.__refresh_translate_direction_panel(reset_last_selected_translate_direction_to_default=True)

            self.__set_expanded(False)
        __init_UI_layout(self)
    
    def __refresh_translate_direction_panel(self, *, reset_last_selected_translate_direction_to_default: bool = False):
        translator: Translator = self.__settings.translator
        if reset_last_selected_translate_direction_to_default:
            self.__settings.last_selected_translate_direction = translator.default_translate_direction
        translate_direction: str = self.__settings.last_selected_translate_direction

        small_font = wx.Font(7, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        for rb in self.translate_direction_radiobuttons:
            rb.Destroy()
        self.translate_direction_radiobuttons.clear()
        addmany_list = []
        default_rb: Optional[MyRadioButton] = None
        # translate option events
        def handler_gen(nav):
            def handler(e: wx.CommandEvent):
                b: MyRadioButton = e.GetEventObject()
                # b.Flash(1.0, (0, 0, 255))
                nav()
            return handler

        for i, c in enumerate(translator.ctrls):
            rb = MyRadioButton(self, font=small_font, tooltip=c.tooltip, label=c.text, size=(0, 0), **({"style": wx.RB_GROUP} if i == 0 else {}))
            rb.Bind(wx.EVT_RADIOBUTTON, handler=handler_gen(lambda td=c.text: self.Navigate(selected_translate_direction=td)))
            if c.text == translate_direction or (default_rb is None and c.text == translator.default_translate_direction):
                default_rb = rb
            self.translate_direction_radiobuttons.append(rb)
            addmany_list.append((rb, c.rect))
        assert(default_rb is not None)
        self.translate_direction_panel.sizer = MyGridBagSizer(self.translate_direction_panel, translator.n_rows, translator.n_cols, addmany_list=addmany_list)
        default_rb.SetValue(True)
        self.Layout()
    
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
            self.google_translate_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler=handler_gen(lambda: self.Navigate(translator=GoogleTranslate)))
            self.yahoo_dictionary_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler=handler_gen(lambda: self.Navigate(translator=YahooDictionary)))
            self.wikitionary_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler=handler_gen(lambda: self.Navigate(translator=Wikitionary)))
            self.abbreviation_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler=handler_gen(lambda: self.Navigate(translator=Abbreviation)))
            # self.translate_direction_Auto_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler=handler_gen(lambda: self.Navigate(translate_direction=TranslateDirection.Auto)))
            # self.translate_direction_CE_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler_gen(lambda: self.Navigate(translate_direction=TranslateDirection.CE)))
            # self.translate_direction_EC_radiobutton.Bind(wx.EVT_RADIOBUTTON, handler_gen(lambda: self.Navigate(translate_direction=TranslateDirection.EC)))
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
    
    @staticmethod
    def GetUrl(settings: Settings) -> str:
        translator: Translator = settings.translator
        translate_direction: str = next((c.text for c in translator.ctrls if c.text == settings.last_selected_translate_direction), translator.default_translate_direction)
        callback: Callable[[str], str] = next(c.keywork_url_callback for c in translator.ctrls if c.text == translate_direction)
        return callback(settings.keyword)

    def Navigate(self, *, keyword: Optional[str] = None,
                         translator: Optional[Translator] = None,
                         selected_translate_direction: Optional[str] = None):
        if keyword is not None:
            self.__settings.keyword = keyword
        if translator is not None and translator != self.__settings.translator:
            self.__settings.translator = translator
            self.__refresh_translate_direction_panel()
        if selected_translate_direction is not None:
            self.__settings.last_selected_translate_direction = selected_translate_direction
        self.TopLevelParent.SetTitle('⟳' + (s[:50] + '...' if len(s:=repr(self.__settings.keyword)[1:-1]) > 50 else s))
        url = self.GetUrl(self.__settings)
        self.url_textctrl.ChangeValue(url)
        self.browser_panel.LoadURL(url)
