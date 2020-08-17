from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from category_selection import SelectedCategory as SelC
from play_game import PlayGame as PG
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivmob import KivMob


class Categories(Screen):
    click_sound = SoundLoader.load('button_click.mp3')
    view = ObjectProperty(None)
    Window.size = (580, 580)

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.create_scrollview)

    def create_scrollview(self, dt):
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=(0, 50, 0, 0))
        layout.bind(minimum_height=layout.setter('height'))

        for category in SelC.category_list:
            text = category
            btn = Button(text=text, size=(50, 50), size_hint=(1, None),
                         background_color=(0.5, 0.5, 0.5, 1), color=(1, 1, 1, 1), font_size=20)
            btn.bind(on_press=self.get_category)
            layout.add_widget(btn)

        scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scrollview.add_widget(layout)
        self.view.add_widget(scrollview)

    def get_category(self, instance):
        x = SelC.file_list[instance.text]
        SelC.current_category = x
        self.manager.transition.direction = 'left'
        self.manager.current = "play"
        screen_2 = self.manager.get_screen('play')
        screen_2.start_game()
        screen_2.get_banner()


class Play(Screen):
    hw = ObjectProperty(None)
    attempts = ObjectProperty(None)
    hangman = ObjectProperty(None)

    click_sound = SoundLoader.load('button_click.mp3')

    def start_game(self):
        category = SelC.current_category
        words = PG.get_word_list(PG, category)
        word = PG.get_word(PG, words)
        hidden_word = PG.show_hidden_word(PG, word)
        PG.attempts = 6
        attempts = "Attempts: " + str(PG.attempts)
        self.attempts.text = attempts
        self.hw.text = ''.join(hidden_word)
        self.hangman.source = 'play_6.png'

    def enter_letter(self, letter):
        PG.check_letter(PG, letter)
        attempts = "Attempts: " + str(PG.attempts)
        hidden_word = PG.hidden_word
        self.attempts.text = attempts
        self.hw.text = ''.join(hidden_word)
        self.hangman.source = "play_" + str(PG.attempts) + ".png"
        if PG.attempts == 0:
            word = PG.original_word
            self.result('You Lose!', word)
            self.hangman.source = 'play_dead.png'
        elif ''.join(PG.hidden_word) == PG.word:
            word = PG.original_word
            self.result('You win!', word)
            self.hangman.source = 'play_alive.png'

    def result(self, result, word):
        pop = Popup(title='Result', size_hint=(.75, .75), auto_dismiss=False)
        text = result + "\nThe Character was:" + "\n" + word + "!"
        layout = FloatLayout()
        btn_1 = Button(text='Play Again', font_size=20, size_hint=(.5, .25), pos_hint={'x': 0, 'y': 0})
        btn_1.bind(on_press=self.play_again, on_release=pop.dismiss)
        btn_2 = Button(text='Change category', font_size=20, size_hint=(.5, .25), pos_hint={'x': .5, 'y': 0})
        btn_2.bind(on_press=self.go_back, on_release=pop.dismiss)
        label = Label(text=text, font_size=20, size_hint=(1, .75), pos_hint={'x': 0, 'y': .25})
        layout.add_widget(btn_1)
        layout.add_widget(btn_2)
        layout.add_widget(label)
        pop.add_widget(layout)
        pop.open()

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = "categories"

    def play_again(self, instance):
        self.start_game()

    def get_banner(self):
        app_id = 'ca-app-pub-4692537890276195~5726828306'
        banner_id = 'ca-app-pub-4692537890276195/6098664719'
        ads = KivMob(app_id)
        ads.new_banner(banner_id)
        ads.request_banner()
        ads.show_banner()


class WindowManager(ScreenManager):
    pass
