from kivy.app import App 
from kivy.uix.widget import Widget 
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.uix.label import Label 
from kivy.uix.dropdown import DropDown # for getting tags
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.properties import StringProperty,BooleanProperty
from kivy.lang import Builder

class TagItem(BoxLayout):
    tagName=StringProperty("") 
    status=BooleanProperty()
    def __init(self,tagName,**kwargs):
        super(TagItem,self).__init__(**kwargs)
        self.tagName=tagName
        
    def checkbox_click(self,instance,value):
        self.status=value

class TagsDropDown(BoxLayout):
    
    def __init__(self,*args,**kwargs):
        super(TagsDropDown,self).__init__(*args,**kwargs)
        self.dropDown=DropDown()        
        self.mainButton=Button(text='Choose',size_hint=(None,None))
        self.mainButton.bind(on_press=self.getTags)
        self.mainButton.bind(on_release= self.dropDown.open)        
        self.add_widget(self.mainButton)
    def getTags(self,instance):

        findTagQry="SELECT DISTINCT tagName FROM tags " 
        self.dropDown.clear_widgets()
       
        qryResult=[("Red","tomato"),("Blue","sky")]
        for row in qryResult:
       
            tI=TagItem(tagName=row[0])
            #tI=Button(text=row[0],size_hint=(None,None))
            tI.bind(on_release= lambda tagBtn: self.dropDown.select(tagBtn.text))
            self.dropDown.add_widget(tI)        
        

Builder.load_string("""
<TagItem>:
    size_hint_y:None
	orientation:"horizontal"
	Label:
		text: root.tagName
		#size: self.texture_size
		height:40
	CheckBox:
		on_active: root.checkbox_click(self, self.active)
		size_hint_x: .20
TagsDropDown:
    id:tgDrop
    size_hint_y:0.25 
          	
    """)

class TestApp(App):
    def build(self):
        return TagsDropDown()

if __name__ == '__main__':
    TestApp().run()
