from kivy.app import App
from kivy.lang import Builder
from window_manager import *

game = Builder.load_file("game.kv")


class GameApp(App):
    def build(self):
        return game


GameApp().run()
