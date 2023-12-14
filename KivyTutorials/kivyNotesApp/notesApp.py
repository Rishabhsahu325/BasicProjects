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
class listItem(Widget):#items)
    def addNoteItem(self,content):
        this.ids.noteContent.text=content
    
class DisplayList(BoxLayout): #for displaying list of Notes that are inserted
    def updateNotes():
        pass
    #SHOULD i KEEP THE Notes FILE OPEN?
        #Probably store in some temporary variable
            
        #try :
        #    with open("./notes.fnote","a") as noteFile:
                #Break and format above content into format of note to be inserted in the notes file
                #write above content to that file
               
                #noteFile.read("||||\n")
                #read until encountering end of the note list time
                #noteFile.read(noteContent)
                #noteFile.write("\n$$$$\n")
        #try to open notes file

        #if it exists then collect todos from that file and display

            # Decode each note as a separate listItem

        #otherwise return None ,indicating no notes exist yet 
        #dynamically add a new widget for each note text
        #for noteObj in whatever:
        #    this.add_widget(listItem(noteObj))
    def display(self):
        notesList=self.ids.noteList #box layout section
        for i in range(20):
            try:
                notesList.add_widget(Label(text="Demo"+str(i),color="black"))
                notesList.height=len(notesList.children)*40
            except Exception as e:
                print("Some error in adding widget")
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



