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

#For notes data management
import sqlite3
import os


#classes to manage ui components

class InsertNote(BoxLayout): #text field for creating object in todo list

    def addNote(self):
        #collect content from Text input and store in variable
        noteObj= self.ids.enterNote #Indexing starts from bottom
        
        #create a connection object
        
        script_dir = os.path.abspath( os.path.dirname( __file__ ) )
        #conn =sqlite3.connect(script_dir+"/notes.fnote")
        conn =sqlite3.connect("./notes.fnote")
        #use cursor for data manipulation
        cursor= conn.cursor()
        
        #uSING tags as text for now ,maybe will convert to indexed field that will act like a key to find same hash value notes
        #create table query string        
        createQry= "CREATE TABLE IF NOT EXISTS notes(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT, content TEXT,tags TEXT)"
        cursor.execute(createQry)
        
        #note insert query string
        query="INSERT INTO notes(title,content,tags) VALUES (?,?,?)"
        parameters=(noteObj.title,noteObj.text,noteObj.tag)
        #execute the query
        cursor.execute(query,parameters)
        print(cursor)
        for row in cursor:
            print(row)
        #commit changes
        conn.commit()
        #depending on the requirement you might use a single connection object for all data manipulation operations 
        #after all notes have been edited display status of operation

        #close the connection 
        cursor.close()
        conn.close()
        
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

    # def updateNotes():
        # #create a connection object
        # conn =sqlite3.connect("notes.fnote")
        # #use cursor for data manipulation
        # cursor= conn.cursor()
        # #note update query string
        # 
        # #iterate and edit the modified notes through the use of the connection object
    # 
        # #commit changes
# 
        # #depending on the requirement you might use a single connection object for all data manipulation operations
        # #after all notes have been edited display status of operation
# 
        # #close the connection
            # 
   
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



