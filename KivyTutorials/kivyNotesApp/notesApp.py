#include libraries of kivy for gui
from kivy.app import App #base class for creating and starting kivy applications
from kivy.uix.widget import Widget #Widget class for all ui classes to inherit from
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
#probable libraries for packaging application


#classes to manage ui components
# This part is to check for difference

#Builder.load_file("notes.kv")

class InsertNote(BoxLayout): #text field for creating object in todo list

    def addNote(self):
        #collect content from Text input and store in variable
        noteContent= self.ids.enterNote.text #Indexing starts from bottom
        #open notes file .fnote if exists ,otherwise create a new file
        try :
            with open("./notes.fnote","a") as noteFile:
                #Break and format above content into format of note to be inserted in the notes file
                #write above content to that file
               
                noteFile.write("||||")
                noteFile.write(noteContent)
                noteFile.write("$$$$")
        except FileExistsError:
            print("Notes storage file doesn't exist yet. Creating new file")
            with open("./notes.fnote","w") as noteFile:
                noteFile.write("||||")
                noteFile.write(noteContent)
                noteFile.write("$$$$")
    # def removeText(self):
        # self.ids.enterNote.text=''
class listItem(Widget):#items in our todo list : tickbox ; description ; (optionally a delete button through a cross)
    pass
class displayList(Widget): #for displaying list of Todo's that are inserted
    pass
    #try to open notes file

    #if it exists then collect todos from that file and display

        # Decode each note as a separate listItem

    #otherwise return None ,indicating no notes exist yet 
    
#handle root widget
class NoteManager(BoxLayout):
    pass
    #after addNote portion loads, load the display List portion

    
class NotesApp(App):
    def build(self):
        return NoteManager()

if __name__ == '__main__':
    NotesApp().run()



