from kivy.app import App 
from kivy.uix.widget import Widget 
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label 
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox 
from kivy.properties import StringProperty,BooleanProperty
class TagItem(BoxLayout):
    tagName=StringProperty("") 
    status=BooleanProperty(False)
    color=StringProperty("black")
    activate=BooleanProperty(False)
    def __init(self,tagName,color="black",activate=False,**kwargs):
        super(TagItem,self).__init__(**kwargs)
        self.tagName=tagName
        self.color=color
        self.activate=activate
        
    def checkbox_click(self,instance,value):
        self.status=value

class AssociatedTags(BoxLayout):
    def __init__(self,*args,**kwargs):
        super(AssociatedTags,self).__init__(*args,**kwargs)
    def addTagItem(self,tagItem):   
        self.ids['tagList'].add_widget(tagItem)
        self.ids['tagList'].width=len(self.ids['tagList'].children)*15
Builder.load_string("""
<TagItem>:
	canvas.before:
	    Line:
	    	width: 1.
	        rectangle: (self.x, self.y, self.width, self.height)
	    Rectangle:
	    	size:self.width,self.height
	    	pos:self.x,self.y
	size_hint_y:None
	size_hint_x:None
	orientation:"horizontal"
	Label:
		id: tagText
		text: root.tagName
		size_hint :(None,None)
		height:self.texture_size[1]
		width:self.texture_size[0]
		color:root.color
	CheckBox:
		id: cb
		on_active: root.checkbox_click(self, self.active)
		active: self.parent.activate
<AssociatedTags>:
	do_scroll_x:True
	BoxLayout:
		id: tagList
        size_hint_x: None
        width: self.minimum_width
		orientation: "horizontal"    
AssociatedTags:
""")
class AssociatedTags(App, ScrollView):
    def build(self):  
        return self
    def on_start(self):
        for count in range(40):
            self.ids['tagList'].add_widget(TagItem(tagName="tagNumber"+str(count),color="blue"))
AssociatedTags().run()
