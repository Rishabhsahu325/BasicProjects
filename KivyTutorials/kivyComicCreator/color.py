# File name: color.py
from kivy.app import App
from kivy.yix.gridlayout import GridLayout
from kivy.lang import Builder

Builder.load_string("""
<GridLayout>:
	cols:2
	Label:
		color: 0.5,0.5,0.5,1
		canvas:
			Rectangle:
				pos: self.x +10,self.y+10
				size: self.width-20 ,self.height-20
	Widget:
		canvas:
			Rectangle:
				pos: self.x+10,self.y+10
				size: self.width-20,self.height-20
""")

class LabelApp(App):
	def build(self):
		return GridLayout()

if __name__=="__main__":
	LabelApp().run()
