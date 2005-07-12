import os,cPickle,md5
from StringIO import StringIO
from bz2 import compress,decompress

class Note:

    text = ""
    position = (-1,-1)
    size = (250,200)
    filepath = ""

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

    def setFilepath(self,path):
        self.filepath = path

    def getFilepath(self):
        return self.filepath

path = "notes/active/"

class NoteManager:

    noteList = []

    def __init__(self):
        for note in os.listdir(path):
            filepath = os.path.join(path,note)
            if os.path.isfile(filepath):
                self.loadNote(filepath)

    def getNotes(self):
        for note in self.noteList:
            yield note

    def loadNote(self,file):
        note = cPickle.load(open(file,"rb"))
        note.setFilepath(file)
        note.setText(unicode(decompress(note.getText()),'utf-8'))

        if note not in self.noteList:
            self.noteList.append(note)
    
        return note

    def removeNote(self,note):
        if note.getFilepath() != "":
            try: os.remove(note.getFilepath())
            except OSError: pass

        if note in self.noteList:
            self.noteList.remove(note)

    def saveNote(self,note):

        self.removeNote(note)

        if note.getText() != "":

            note.setFilepath("")
            note.setText(compress(note.getText().encode('utf-8')))
        
            cFile = StringIO()
            cPickle.dump(note,cFile,-1)

            filepath = os.path.join(path,md5.new(cFile.getvalue()).hexdigest())

            nFile = file(filepath,"wb")
            nFile.write(cFile.getvalue())

            nFile.close()
            cFile.close()

            note = self.loadNote(filepath)
