#include libraries of kivy for gui
from kivy.app import App #base class for creating and starting kivy applications
from kivy.uix.widget import Widget #Widget class for all ui classes to inherit from
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label # for testing adding of widget at the start
#probable libraries for packaging application


#classes to manage ui components

class InsertNote(BoxLayout): #text field for creating object in todo list

    def addNote(self):
        #collect content from Text input and store in variable
        noteContent= self.ids.enterNote.text #Indexing starts from bottom
        #open notes file .fnote if exists ,otherwise create a new file
        try :
            with open("./notes.fnote","a") as noteFile:
                #Break and format above content into format of note to be inserted in the notes file
                #write above content to that file
               
                noteFile.write("||||\n")
                #Need to add a unique note identifier  
                noteFile.write(noteContent)
                noteFile.write("\n$$$$\n")
        except FileExistsError:
            print("Notes storage file doesn't exist yet. Creating new file")
            with open("./notes.fnote","w") as noteFile:
                noteFile.write("||||\n")
                noteFile.write(noteContent)
                noteFile.write("\n$$$$\n")
    def removeText(self):
        textfield=self.ids.enterNote
        textfield.select_all()
        textfield.delete_selection()
class ListItem(BoxLayout):# Note items
    def __init__(self,noteTitle,noteContent,noteHash,**kwargs):
        self.title=noteTitle
        self.content=noteContent
        self.identifier=noteHash
        
        super().__init__(**kwargs)
        
        
    def addNoteItem(self,content):
        this.ids.noteContent.text=content
    
class DisplayList(BoxLayout): #for displaying list of Notes that are inserted
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fileObj="./notes.fnote"
        #notes dictionary by serial number
        self.notesDict={}
        
        
    def updateNotes():
        with open(self.fileObj, "w") as noteFile:
            #maybe store existing notes content in file for backup

            # after storing ,remove existing notes content
            noteFile.seek(0,0)# place pointer at starting
            noteFile.write("")
            #if writing all notes from single object
            noteFile.write(updatedNotes)#assuming updatedNotes contains updated version of notes
            #additional optimization , may only modify the individual edited notes ,instead 
            #of modifying all the notes
            
   
    def display(self):
        notesList=self.ids.noteList #box layout section
        
#handle root widget
class NoteManager(BoxLayout):
    pass
    #after InsertNote portion loads, load the display List portion
    
    
class NotesApp(App):
    def build(self):
        manager= NoteManager()
        manager.ids.noteListParent.display()
        return manager

if __name__ == '__main__':
    NotesApp().run()



