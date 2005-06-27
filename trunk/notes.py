import os,cPickle,md5
from StringIO import StringIO
from bz2 import compress,decompress

class Note:

    text = ""
    position = (-1,-1)
    size = (250,200)
    filename = ""

    def __init__(self,text = ""):
        self.text = text

    def load(self):
        pass

    def save(self,active):
        print self.text

    def setText(self,text):
        self.text = text

    def getText(self):
        return self.text

class NoteManager:

    noteList = []

    def __init__(self):
        path = "notes/active/"
        for note in os.listdir(path):
            if os.path.isfile(os.path.join(path,note)):
                self.noteList.append(self.loadNote(note))

    def getNotes(self):
        for note in self.noteList:
            yield note

    def loadNote(self,file):
        note = cPickle.load(open("notes/active/%s" % file,"rb"))
        note.text = decompress(note.text)
        return note

    def saveNote(self,note):
        if note not in self.noteList:
            self.noteList.append(note)

        note.text = compress(note.text)
        
        cFile = StringIO()
        cPickle.dump(note,cFile,-1)
        nFile = file("notes/active/%s" %
                    md5.new(cFile.getvalue()).hexdigest(),"wb")
        nFile.write(cFile.getvalue())
        nFile.close()
        cFile.close()

        note.text = decompress(note.text)
