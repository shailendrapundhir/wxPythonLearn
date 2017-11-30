import wx
import os


class MyApp(wx.App):
    def OnInit(self):
        self.frame = InheritanceFrame(None, title="Virtualized Methods")
        self.SetTopWindow(self.frame)
        self.frame.Show()

        for method in dir(wx.Panel):
            if (method.startswith('base_')):
                print(method)

        return True


class StockFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name="Stock Frame"):
        super(StockFrame, self).__init__(parent, id, title, pos, size, style, name)

        self.panel = wx.Panel(self)

        ok_btn = wx.Button(self.panel, wx.ID_OK)
        cancen_btn = wx.Button(self.panel, wx.ID_CANCEL, pos=(100, 0))

        menu_bar = wx.MenuBar()
        edit_menu = wx.Menu()
        edit_menu.Append(wx.NewId(), "Test")
        edit_menu.Append(wx.ID_PREFERENCES)
        menu_bar.Append(edit_menu, "Edit")
        self.SetMenuBar(menu_bar)


class IconFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name="IconFrame"):
        super(IconFrame, self).__init__(parent, id, title, pos, size, style, name)
        self.panel = wx.Panel(self)
        path = os.path.abspath("./hi.png")
        icon = wx.Icon(path, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)


class NewFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name="MyFrame"):
        super(NewFrame, self).__init__(parent, id, title, pos, size, style, name)
        self.panel = wx.Panel(self)
        img_path = os.path.abspath('./mumbai.jpg')
        bitmap = wx.Bitmap(img_path, type=wx.BITMAP_TYPE_JPEG)
        self.bitmap = wx.StaticBitmap(self.panel, bitmap=bitmap);


class MyFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name="MyFrame"):
        super(MyFrame, self).__init__(parent, id, title, pos, size, style, name)
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.BLACK)
        button = wx.Button(self.panel, label="Click", pos=(50, 50))
        self.btnId = button.GetId()
        self.Bind(wx.EVT_BUTTON, self.OnButton, button)

    def OnButton(self, event):
        print("\nFrame Get Children:")
        for child in self.GetChildren():
            print("%s" % repr(child))

        print("\nPanel FindWindowById:")
        button = self.panel.FindWindowById(self.btnId)
        print("%s" % repr(button))

        button.SetLabel("Changed Label")

        print("\n Button get parent:")
        panel = button.GetParent()
        print("%s" % repr(panel))

        print("\n Get the app object:")
        app = wx.GetApp()
        print("%s" % repr(app))

        print("\n Get frame of app:")
        frame = app.GetTopWindow()
        print("%s" % repr(frame))


class TextFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name="textFrame"):
        super(TextFrame, self).__init__(parent, id, title, pos, size, style, name)
        self.panel = wx.Panel(self)

        button = wx.Button(self.panel, label="Copy", pos=(50, 50))
        self.Bind(wx.EVT_BUTTON, self.SetClipboardText("123Yo"), button)

        button2 = wx.Button(self.panel, label="Get Clipboard Data", pos=(150, 50))
        self.Bind(wx.EVT_BUTTON, self.GetClipboardText(), button2)

    def SetClipboardText(self, text):
        data_o = wx.TextDataObject()
        data_o.SetText(text)

        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data_o)
            wx.TheClipboard.Close()

    def GetClipboardText(self):
        text_obj = wx.TextDataObject()
        rtext = ""
        if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
            if wx.TheClipboard.GetData(text_obj):
                rtext = text_obj.GetText()
            wx.TheClipboard.Close()
        return rtext


class FileAndTextDropTarget(wx.DropTarget):
    def __init__(self, file_callback, text_callback):
        assert callable(file_callback)
        assert callable(text_callback)
        super(FileAndTextDropTarget, self).__init__()

        self.fcallback = file_callback
        self.tcallback = text_callback

        self._data = None
        self.txtDo = None
        self.filedo = None

        self.InitObjects()

    def InitObjects(self):
        self._data = wx.DataObjectComposite()
        self.txtDo = wx.TextDataObject()
        self.filedo = wx.FileDataObject()
        self._data.Add(self.txtDo, False)
        self._data.Add(self.filedo, True)
        self.SetDataObject(self._data)

    def OnData(self, x_cord, y_cord, drag_result):
        if self.GetData():
            data_format = self._data.GetReceivedFormat()
            if data_format.GetType() == wx.DF_FILENAME:
                self.fcallback(self.filedo.GetFilenames())
            else:
                self.tcallback(self.txtDo.GetText())

        return drag_result


class DropTargetFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name="DropTargetFrame"):
        super(DropTargetFrame, self).__init__(parent, id, title, pos, size, style, name)

        choices = ["Drag and Drop text and files here", ]
        self.list = wx.ListBox(self, choices=choices)
        self.dt = FileAndTextDropTarget(self.OnFileDrop, self.OnTextDrop)

        self.list.SetDropTarget(self.dt)

        self.CreateStatusBar()

    def OnFileDrop(self, files):
        self.PushStatusText("Files Dropped")
        for f in files:
            self.list.Append(f)

    def OnTextDrop(self, text):
        self.PushStatusText("Text Dropped")
        self.list.Append(text)



class MyPanel(wx.Panel):
    def __init__(self,parent):
        super(MyPanel,self).__init__(parent)

        sizer = wx.BoxSizer()
        self.SetSizer(sizer)

    def AddChild(self, child):
        sizer = self.GetSizer()
        sizer.Add(child,0,wx.ALIGN_LEFT|wx.ALL,8)
        return super(MyPanel, self).AddChild(child)

class VPanel(wx.PyPanel):
    def __init__(self,parent):
        super(VPanel,self).__init__(parent)

        sizer = wx.BoxSizer()
        self.SetSizer(sizer)


    def AddChild(self,child):
        sizer = self.GetSizer()
        sizer.Add(child,0,wx.ALIGN_LEFT|wx.ALL,8)
        return super(VPanel,self).AddChild(child)


class InheritanceFrame(wx.Frame):
    def __init__(self,parent,*args,**kwargs):
        super(InheritanceFrame,self).__init__(parent,*args,**kwargs)

        self.mypanel = MyPanel(self)
        self.mypanel.SetBackgroundColour(wx.BLACK)
        self.virtPanel = VPanel(self)
        self.virtPanel.SetBackgroundColour(wx.WHITE)

        self.__DoLayout()



    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.mypanel,1,wx.EXPAND)
        sizer.Add(self.virtPanel,1,wx.EXPAND)
        self.SetSizer(sizer)

        for x in range(3):
            wx.Button(self.mypanel,label="MyPanel %d" %x)

        for x in range(3):
            wx.Button(self.virtPanel,label="virtPanel %d" %x)

        self.SetInitialSize(size=(300,200))


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
