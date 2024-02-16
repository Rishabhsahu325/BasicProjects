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
#depending on the requirement you might use a single connection object for all data manipulation operations
script_dir = os.path.abspath( os.path.dirname( __file__ ) )




def removeText(*tfs):
    for textfield in tfs:
        textfield.select_all()
        textfield.delete_selection()
        
#classes to manage ui components

            
class InsertNote(BoxLayout): #text field for creating object in todo list

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.removeText=removeText
    def addNote(self):
        try:
            #collect content from Text input and store in variable
            noteTitle=self.ids.enterTitle
            noteCont= self.ids.enterNote #Indexing starts from bottom
            
            #uSING tags as text for now ,maybe will convert to indexed field that will act like a key to find same hash value notes
            
            #note insert query string
            query="INSERT INTO notes(title,content,tags) VALUES (?,?,?)"
            parameters=(noteTitle.text,noteCont.text,noteCont.tag)
            #execute the query
            cursor.execute(query,parameters)
           
            #depending on the requirement you might use a single connection object for all data manipulation operations 
            #after all notes have been edited display status of operation
            
            noteListBox=self.parent.parent.ids["noteListParent"]
            #In sqlite insertion query does not return inserted rows and result is typically emtpy
            conn.commit()                    
            noteListBox.addListItem(title=noteTitle.text,content=noteCont.text)
            
        except Exception as e:
            print("Error in inserting data and creating new noteList Item widget")
            print(e)
            
    
        
class ListItem(BoxLayout):# Note items
    def __init__(self,noteTitle,noteContent,*tags,**kwargs):
        self.title=noteTitle
        self.content=noteContent        
        super().__init__(**kwargs)
    
class DisplayList(BoxLayout): #for displaying list of Notes that are inserted
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.removeText=removeText

    def addListItem(self,title,content,*tags):   
        # self.ids['noteList'].add_widget(Label(text=content,color="black")) #row[2]
        self.ids['noteList'].add_widget(ListItem(noteTitle=title,noteContent=content))
        self.ids['noteList'].height=len(self.ids['noteList'].children)*100
           
    
    def cleanNotesList(self):
        #First remove any previously existing note List Items
        self.ids['noteList'].clear_widgets()
    def executeQuery(self,command,title,*tags):
        
        if command ==0:#display notes filtered by search title
            query="SELECT * FROM notes WHERE title=(?)"
            parameters=(title,)
        #elif command==1 :#display notes filtered by search tags
        
        else: # display all notes
            query="SELECT * FROM  notes"
            parameters=()
        queryResult=cursor.execute(query,parameters)
        return queryResult

#uSING tags as text for now ,maybe will convert to indexed field that will act like a key to find same hash value notes
    def display(self,queryResult):
        notesList=self.ids.noteList #box layout section        
        for row in queryResult:
            try:
                self.addListItem(title=row[1],content=row[2])
                #print("Display of this note successful")
            except Exception as e:
                print("Error in adding widget")
                print(e)
    def searchCall(self,criteria,title,*tags):
        result=self.executeQuery(criteria,title,*tags)
        self.cleanNotesList()
        self.display(result)
        
#handle root widget
class NoteManager(BoxLayout):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.removeText=removeText
    #after InsertNote portion loads, load the display List portion
    
    
class NotesApp(App):
    def __init__(self):
        super().__init__()
        self.manager=None
    def build(self):
        
        self.manager= NoteManager()
        return self.manager

    def on_start(self):
        global conn
        global cursor
        conn = sqlite3.connect("./notes.fnote")
        cursor= conn.cursor()
        createQry= "CREATE TABLE IF NOT EXISTS notes(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT, content TEXT,tags TEXT)"
        cursor.execute(createQry)
        qr=self.manager.ids['noteListParent'].executeQuery(command=2,title=None)
        self.manager.ids['noteListParent'].display(qr)
        
    def on_stop(self):
        cursor.close()
        conn.close()
if __name__ == '__main__':
    NotesApp().run()



