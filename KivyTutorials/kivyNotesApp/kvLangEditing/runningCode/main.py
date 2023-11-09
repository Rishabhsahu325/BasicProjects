'''
Kivy Catalog
============

The Kivy Catalog viewer showcases widgets available in Kivy
and allows interactive editing of kivy language code to get immediate
feedback. You should see a two panel screen with a menu spinner button
(starting with 'Welcome') and other controls across the top.The left pane
contains kivy (.kv) code, and the right side is that code rendered. You can
edit the left pane, though changes will be lost when you use the menu
spinner button. The catalog will show you dozens of .kv examples controlling
different widgets and layouts.

The catalog's interface is set in the file kivycatalog.kv, while the
interfaces for each menu option are set in containers_kvs directory. To
add a new .kv file to the Kivy Catalog, add a .kv file into the container_kvs
directory and reference that file in the ScreenManager section of
kivycatalog.kv.

Known bugs include some issue with the drop
'''
import kivy
kivy.require('1.4.2')
import os
import sys
from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder, Parser, ParserException
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.codeinput import CodeInput
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivy.uix.filechooser import FileChooserListView
CATALOG_ROOT = os.path.dirname(__file__)

# Config.set('graphics', 'width', '1024')
# Config.set('graphics', 'height', '768')

'''List of classes that need to be instantiated in the factory from .kv files.
'''
CONTAINER_KVS = os.path.join(CATALOG_ROOT, 'container_kvs')
CONTAINER_CLASSES = [c[:-3] for c in os.listdir(CONTAINER_KVS)
    if c.endswith('.kv')]


class Container(BoxLayout):
    '''A container is essentially a class that loads its root from a known
    .kv file.

    The name of the .kv file is taken from the Container's class.
    We can't just use kv rules because the class may be edited
    in the interface and reloaded by the user.
    See :meth: change_kv where this happens.
    '''

    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
        self.previous_text = open(self.kv_file).read() 
        
        
        try:
            parser = Parser(content=self.previous_text)
            widget = Factory.get(parser.root.name)()
            Builder._apply_rule(widget, parser.root, parser.root)
            
        except(SyntaxError, ParserException,AttributeError) as e:
            #Load the standard error widget
            self.error_text= str(e).encode('utf-8')
            self.error_container=open('/mnt/c/Users/HP/ONEDRI~1/DOCUME~1/GitHub/kivy/examples/demo/KIVYCA~1/container_kvs/ErrorContainer.kv')
            self.error_container_content=self.error_container.read()
            parser2=Parser(content=self.error_container_content)
            widget2=Factory.get(parser2.root.name)()
            Builder._apply_rule(widget2, parser2.root, parser2.root)
            widget=widget2
        except Exception as e:    
            self.error_text= str(e).encode('utf-8')
            self.error_container=open('/mnt/c/Users/HP/ONEDRI~1/DOCUME~1/GitHub/kivy/examples/demo/KIVYCA~1/container_kvs/ErrorContainer.kv')
            self.error_container_content=self.error_container.read()
            parser2=Parser(content=self.error_container_content)
            widget2=Factory.get(parser2.root.name)()
            Builder._apply_rule(widget2, parser2.root, parser2.root)
            widget=widget2
            #print(self.error_text)
            
        finally:
            self.add_widget(widget) 
            

            

    @property
    def kv_file(self):
        '''Get the name of the kv file, a lowercase version of the class
        name.
        '''
        return os.path.join(CONTAINER_KVS, self.__class__.__name__ + '.kv')


for class_name in CONTAINER_CLASSES:
    globals()[class_name] = type(class_name, (Container,), {})


class KivyRenderTextInput(CodeInput):
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        is_osx = sys.platform == 'darwin'
        # Keycodes on OSX:
        ctrl, cmd = 64, 1024
        key, key_str = keycode

        if text and key not in (list(self.interesting_keys.keys()) + [27]):
            # This allows *either* ctrl *or* cmd, but not both.
            if modifiers == ['ctrl'] or (is_osx and modifiers == ['meta']):
                if key == ord('s'):
                    self.catalog.change_kv(True)
                    return

        return super(KivyRenderTextInput, self).keyboard_on_key_down(
            window, keycode, text, modifiers)


class Catalog(BoxLayout):
    '''Catalog of widgets. This is the root widget of the app. It contains
    a tabbed pain of widgets that can be displayed and a textbox where .kv
    language files for widgets being demoed can be edited.

    The entire interface for the Catalog is defined in kivycatalog.kv,
    although individual containers are defined in the container_kvs
    directory.

    To add a container to the catalog,
    first create the .kv file in container_kvs
    The name of the file (sans .kv) will be the name of the widget available
    inside the kivycatalog.kv
    Finally modify kivycatalog.kv to add an AccordionItem
    to hold the new widget.
    Follow the examples in kivycatalog.kv to ensure the item
    has an appropriate id and the class has been referenced.

    You do not need to edit any python code, just .kv language files!
    '''
    language_box = ObjectProperty()
    screen_manager = ObjectProperty()
    _change_kv_ev = None

    def __init__(self, **kwargs):
        self._previously_parsed_text = ''
        super(Catalog, self).__init__(**kwargs)
        self.show_kv(None, 'Welcome')
        self.carousel = None

    def show_kv(self, instance, value):
        '''Called when an a item is selected, we need to show the .kv language
        file associated with the newly revealed container.'''

        self.screen_manager.current = value
        
        child = self.screen_manager.current_screen.children[0]
        self.file_name=child.kv_file
        with open(child.kv_file, 'rb') as file:
            self.language_box.text = file.read().decode('utf8')
        if self._change_kv_ev is not None:
            self._change_kv_ev.cancel()
        self.change_kv()
#MAY HAVE TO EDIT CONDITION TO SOMETHING ELSE FROM child.kv_file TO SOME OTHER CRITERIA
        if child.kv_file == str(os.path.dirname(__file__)) +"/container_kvs/TrialContainer.kv"   : 
            #activate the save button that calls save_kv which on clicking saves text to original kv file
            #button will call the function save_kv defined  below
            self.savebtn.disabled =False
            #activate option to choose file for kv lang editing
            self.chooseFile.disabled=False
            print("Chosen default file in kv lang savecontent editor")
        #check if child kv file lies in container_kvs directory or not and if it lies outside then keep state of saveBtn and chooseFile unchanged
        elif  os.path.commonprefix([child.kv_file,"/mnt/c/Users/HP/ONEDRI~1/DOCUME~1/GitHub/kivy/examples/demo/KIVYCA~1/container_kvs"]) !=   "/mnt/c/Users/HP/ONEDRI~1/DOCUME~1/GitHub/kivy/examples/demo/KIVYCA~1/container_kvs" :
            print("Chosen custom location file in kv lang savecontent editor")
            self.savebtn.disabled=False
            self.chooseFile.disabled=False
        else:
            self.savebtn.disabled= True
            self.chooseFile.disabled=True
            
        # reset undo/redo history
        self.language_box.reset_undo()
    def choose_file(self,*largs):
        
        # Create a popup and pass the file chooser as the content
        filechooser = FileChooserListView()
        self.popup = Popup(title="Choose a file", content=filechooser, size_hint=(0.9, 0.9), auto_dismiss=False)
        filechooser.path="."
        selectFileButton = Button(text="Open", size_hint=(1, 0.1))
        selectFileButton.bind(on_release=self.load_file)
        
        filechooser.add_widget(selectFileButton)
        # Open the popup
        self.popup.open()
        self.filechooser=filechooser
        
        
    def load_file(self, instance):
        # Get the selected file name
        self.file_name = self.popup.content.selection[0]
        
        # Open the file and read its contents
        with open(self.file_name, "r") as f:
            file_content = f.read()
        self.language_box.text= file_content
        #self.language_box.text = file.read().decode('utf8')
        if self._change_kv_ev is not None:
            self._change_kv_ev.cancel()
        self.change_kv()
        self.popup.dismiss()
    def close_popup(self,instance):
        self.popup.dismiss()
        
# '/mnt/c/Users/HP/ONEDRI~1/DOCUME~1/GitHub/kivy/examples/demo/KIVYCA~1/container_kvs/TrialContainer.kv'
#(os.path.get)"/TrialContainer.kv":
#os.path.join(CONTAINER_KVS, 'TrialContainer.kv'): This one worked

# if os.path.isfile(file_path):
#   # Get the common prefix of the file path and the directory path
#   common_prefix = os.path.commonprefix([file_path, dir_path])
#   # Check if the common prefix is equal to the directory path
#   if common_prefix == dir_path:
#     print("The file lies within the directory")

    
    def schedule_reload(self):
        if self.auto_reload:
            txt = self.language_box.text
            child = self.screen_manager.current_screen.children[0]
            if txt == child.previous_text:
                return
            child.previous_text = txt
            if self._change_kv_ev is not None:
                self._change_kv_ev.cancel()
            if self._change_kv_ev is None:
                self._change_kv_ev = Clock.create_trigger(self.change_kv, 2)
            self._change_kv_ev()
    def save_kv(self,*largs):
        '''Called when save kv button is clicked. It will save the text in editor window to the original kv file.'''
        txt = self.language_box.text
        try:
            child = self.screen_manager.current_screen.children[0]
            with open(self.file_name, 'w') as file:
                file.write(txt) #self.language_box.text = file.write(txt)
        except Exception as e:
            self.show_error(e)
    def change_kv(self, *largs):
        '''Called when the update button is clicked. Needs to update the
        interface for the currently active kv widget, if there is one based
        on the kv file the user entered. If there is an error in their kv
        syntax, show a nice popup.'''

        txt = self.language_box.text
        kv_container = self.screen_manager.current_screen.children[0]
        try:
            parser = Parser(content=txt)
            kv_container.clear_widgets()
            widget = Factory.get(parser.root.name)()
            Builder._apply_rule(widget, parser.root, parser.root)
            kv_container.add_widget(widget)
        except (SyntaxError, ParserException) as e:
            self.show_error(e)
        except Exception as e:
            self.show_error(e)

    def show_error(self, e):
        self.info_label.text = str(e).encode('utf-8')
        self.anim = Animation(top=190.0, opacity=1, d=2, t='in_back') +\
            Animation(top=190.0, d=3) +\
            Animation(top=0, opacity=0, d=2)
        self.anim.start(self.info_label)


class KivyCatalogApp(App):
    '''The kivy App that runs the main root. All we do is build a catalog
    widget into the root.'''

    def build(self):
        return Catalog()

    def on_pause(self):
        return True


if __name__ == "__main__":
    KivyCatalogApp().run()
