from typing import Final, Optional
import wx
from Utility.Event import Event, ArgEvent

class ClipboardListener:
    def __init__(self):
        self.__cached_text: Optional[str] = None
        self.TextChanged: Final[ArgEvent[str]] = Event.Of(str)
    def check_text(self) -> Optional[str]:
        clipboard: wx.Clipboard = wx.TheClipboard
        assert(clipboard is not None)
        assert(clipboard.Open() == True)
        try:
            if clipboard.GetData(text_data:=wx.TextDataObject()):
                text: str = text_data.GetText()
                if text != self.__cached_text:
                    self.__cached_text = text
                    self.TextChanged.notify(text)
                    return text
        finally:
            clipboard.Close()
    @property
    def CachedText(self):
        return self.__cached_text



'''
A wx.DataFormat is an encapsulation of a platform-specific format handle which is used by the system for the clipboard and drag and drop operations.

The applications are usually only interested in, for example, pasting data from the clipboard only if the data is in a format the program understands and a data format is something which uniquely identifies this format.

On the system level, a data format is usually just a number ( CLIPFORMAT under Windows or Atom under X11, for example) and the standard formats are, indeed, just numbers which can be implicitly converted to wx.DataFormat. The standard formats are:

wx.DF_INVALID

An invalid format - used as default argument for functions taking a wx.DataFormat argument sometimes.

wx.DF_TEXT

Text format (String ).

wx.DF_BITMAP

A bitmap ( wx.Bitmap).

wx.DF_METAFILE

A metafile ( wx.Metafile, Windows only).

wx.DF_FILENAME

A list of filenames.

wx.DF_HTML

An HTML string. This is currently only valid on Mac and MSW.

wx.DF_PNG

A PNG file. This is valid only on MSW. This constant is available since wxWidgets 3.1.5.
'''