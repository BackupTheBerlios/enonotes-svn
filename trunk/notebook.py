import wx
from notes import *

IDB_SAVE = wx.NewId()
IDB_ACTIVE = wx.NewId()

tbTools = {IDB_SAVE:"OnSaveClick"}

class noteFrame(wx.Frame):

    def __init__(self,parent,ID,title,app,note=None):
        wx.Frame.__init__(self,parent,ID,title)
        self.app = app
        self.id = ID

        self.note = note or Note()

        self.SetIcon(self.app.appIcon)
        self.SetSize(self.note.size)
        self.SetPosition(self.note.position)

        toolbar = self.CreateToolBar(wx.TB_FLAT |
                                    wx.TB_TEXT |
                                    wx.TB_VERTICAL |
                                    wx.NO_BORDER)
        toolbar.SetToolBitmapSize((16,16))
#        toolbar.AddTool(IDB_SAVE,
#                        wx.Bitmap("buttonSave.xpm",wx.BITMAP_TYPE_XPM))
        toolbar.AddCheckTool(IDB_ACTIVE,
                        wx.Bitmap("buttonTick.xpm",wx.BITMAP_TYPE_XPM),
                        shortHelp="Notiz de-/aktivieren")
        toolbar.ToggleTool(IDB_ACTIVE,True)

        toolbar.Realize()

        box = wx.BoxSizer(wx.VERTICAL)
        self.edit = wx.TextCtrl(self,wx.NewId(),style = wx.TE_MULTILINE)
        if self.note: self.edit.SetValue(self.note.getText())

        box.Add(self.edit,1,wx.ALL | wx.EXPAND)
        self.SetSizer(box)

#        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=IDB_SAVE)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnToolClick(self,event):
        handler = getattr(self,tbTools[event.GetId()])
        handler()

    def OnSaveClick(self):
        pass

    def OnClose(self,event):
        self.UpdateNote()
        self.app.noteMan.saveNote(self.note)
        self.app.OnWindowClosing(self.id)
        self.Destroy()

    def UpdateNote(self):
        self.note.setText(self.edit.GetValue())
        self.note.size = self.GetSize()
        self.note.position = self.GetPosition()
        
