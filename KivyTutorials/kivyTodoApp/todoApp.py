#include libraries of kivy for gui
from kivy.app import App #base class for creating and starting kivy applications
from kivy.uix.widget import Widget #Widget class for all ui classes to inherit from

#probable libraries for packaging application


#classes to manage ui components



class addTodo(Widget): #text field for creating object in todo list
    pass

class insertButton(Widget):# button which inserts recently typed item in the todo list
    pass
class listItem(Widget):#items in our todo list : tickbox ; description ; (optionally a delete button through a cross)
    pass
class displayList(Widget): #for displaying list of Todo's that are inserted
    pass

class TodoApp(App):
    pass

if __name__ == '__main__':
    TodoApp().run()



# The error “NoneType object has no attribute ‘name’” usually occurs when you try to access an attribute
# of an object that is None. This means that the object has not been initialized or assigned a value.
# In the context of Kivy, this error can happen when you use the app object in a kv file before the app
# is created, or when you use a property that does not exist in a widget.

# Some possible solutions are:

# Make sure you create the app object before using it in a kv file. 
# For example, you can use App.get_running_app() instead of app to get the current app instance1.
# Make sure you use the correct property name for a widget. 
# For example, the Image widget has a source property, not a Source property2.
# Make sure you return a value from a method that you use as an attribute. 
# For example, if you have a method b() that sets an attribute name, you should return self from 
# that method so that you can access a.b().name3.
# You can also refer to the Kivy documentation4 for more information on how to create and use kv files.
#     I hope this helps you resolve your error. 