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

#classes to manage ui components

class InsertNote(BoxLayout): #text field for creating object in todo list

    def addNote(self):
        try:
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
           
            #depending on the requirement you might use a single connection object for all data manipulation operations 
            #after all notes have been edited display status of operation
            
            noteListBox=self.parent.parent.ids["noteListParent"]
            #In sqlite insertion query does not return inserted rows and result is typically emtpy
            #commit changes 
            conn.commit()                    
            #close the connection 
            cursor.close()
            conn.close()
            noteListBox.addListItem(title="DefaultTitle",content=noteObj.text)
            
        except Exception as e:
            print("Error in inserting data and creating new noteList Item widget")
            print(e)
            
    def removeText(self):
        textfield=self.ids.enterNote
        textfield.select_all()
        textfield.delete_selection()
        
class ListItem(BoxLayout):# Note items
    def __init__(self,noteTitle,noteContent,noteHash,**kwargs):
        self.title=noteTitle
        self.content=noteContent        
        super().__init__(**kwargs)
    
class DisplayList(BoxLayout): #for displaying list of Notes that are inserted
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


    def addListItem(self,title,content,*tags):   
        print(content)
        self.ids['noteList'].add_widget(Label(text=content,color="black")) #row[2]
        self.ids['noteList'].height=len(self.ids['noteList'].children)*40
           
    # def updateNotes(self):
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
                
        #create a connection object
        
        script_dir = os.path.abspath( os.path.dirname( __file__ ) )
        #conn =sqlite3.connect(script_dir+"/notes.fnote")
        conn =sqlite3.connect("./notes.fnote")
        #use cursor for data manipulation
        cursor= conn.cursor()
        
        #uSING tags as text for now ,maybe will convert to indexed field that will act like a key to find same hash value notes
        
        #note insert query string
        query="SELECT * FROM  notes"
        
        #execute the query
        cursor.execute(query)
        for row in cursor:
            try:
                self.addListItem(title="defTitle",content=row[2])
                print("Display of this note successful")
            except Exception as e:
                print("Error in adding widget")
                print(e)
                
        #commit changes
        conn.commit()

        #close the connection 
        cursor.close()
        conn.close()
        
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



