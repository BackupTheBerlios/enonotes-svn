#!/usr/bin/python

import wx

from notebook import *
from notes import *

IDM_NOTE = wx.NewId()
IDM_CONFIG = wx.NewId()
IDM_EXIT = wx.NewId()

class SysIcon(wx.TaskBarIcon):

    def __init__(self,app):
        wx.TaskBarIcon.__init__(self)
        self.app = app

        self.Bind(wx.EVT_MENU, self.OnNewNote, id=IDM_NOTE)
        self.Bind(wx.EVT_MENU, self.OnExit, id=IDM_EXIT)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(IDM_NOTE,"neue Notiz")
        menu.Append(IDM_CONFIG,"Konfiguration")
        menu.AppendSeparator()
        menu.Append(IDM_EXIT,"Beenden")
        return menu

    def OnExit(self,event):
        self.app.CloseAll()
        self.Destroy()

    def OnNewNote(self,event):
        self.app.CreateNote()

class enoNotes(wx.App):

    activeNotes = []
    noteMan = []

    def OnInit(self):
        sysIcon = SysIcon(self)
        sysIcon.SetIcon(wx.Icon("favicon.ico",
                                wx.BITMAP_TYPE_ICO,16,16),
                                "enoNotes")
        self.noteMan = NoteManager()
        self.Bind(wx.EVT_TASKBAR_LEFT_UP, self.ToggleNotes)

        return True

    def ToggleNotes(self,event):
        if self.activeNotes != []:
            self.CloseAll()
        else:
            for note in self.noteMan.getNotes():
                self.CreateNote(note)

    def CreateNote(self,note=None):
        id = wx.NewId()
        noteWin = noteFrame(None,id,"enoNotes",self,note)
        noteWin.Show(True)
        self.SetTopWindow(noteWin)
        self.activeNotes.append((id,noteWin))

    def OnWindowClosing(self,id):
        self.activeNotes = [note for note in self.activeNotes[:]
                            if note[0] != id]

    def CloseAll(self):
        for note in self.activeNotes:
            note[1].Close()

if __name__ == "__main__":
    app = enoNotes(0)
    app.MainLoop()
