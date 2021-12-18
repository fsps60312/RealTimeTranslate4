# To install wxpython
## need gtk+-3.0 to build wheels for wxpython on Ubuntu

### Scenario:
    pip install wxpython

><font color=#ff0000>No package 'gtk+-3.0' found</font>

### Solution:
    sudo apt install libgtk-3-dev

### References:
* [wxPython Downloads | wxPython](https://wxpython.org/pages/downloads/index.html)


# To use wx.html2.WebView
### Scenario:
    import wx.html2 import WebView
    // something else...
    self.webview = wx.html2.WebView(self, url='http://codingsimplifylife.blogspot.tw/')

><font color=#ff0000>NotImplementedError</font>

### Solution:
    sudo apt install libwebkit2gtk-4.0-dev
    # reinstall wxpython
    pip uninstall wxpython
    pip cache remove wxPython # Watch out: use wxPython instead of wxpython, you need to use exactly english letter case here
    pip install wxpython

### References:
* [wx.html2.WebView — wxPython Phoenix 4.1.2a1 documentation](https://wxpython.org/Phoenix/docs/html/wx.html2.WebView.html)
* [wx.html2.WebView NotImplementedError (Ubuntu GTK) - WxWidgets/Phoenix](https://issueexplorer.com/issue/wxWidgets/Phoenix/2028)