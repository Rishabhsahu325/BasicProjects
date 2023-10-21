# File name:comiccreator.py
from kivy.app import App
from kivy.lang import Builder
#from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager

Builder.load_file('toolbox.kv')
Builder.load_file('comicwidgets.kv')
Builder.load_file('drawingspace.kv')
Builder.load_file('generaloptions.kv')
Builder.load_file('statusbar.kv')
Builder.load_file('comiccreator.kv')

#chapter2 graphics
class ComicScreenManager(ScreenManager):
	pass
class ComicScreenManagerApp(App):
	def build(self):
		return ComicCreator()
class ComicScreenManagerApp(App):
	def build(self):
		return ComicScreenManager()
if __name__=="__main__":
	ComicScreenManagerApp().run()
