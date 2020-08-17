import csv
import random
from kivy.core.audio import SoundLoader


class PlayGame:
    attempts = 6
    letter_list = []
    hidden_word = []
    original_word = ""
    word = ""

    drawing_sound = SoundLoader.load('drawing_sound.mp3')

    def get_word_list(self, category):
        filename = category
        words = []
        with open(filename) as f:
            reader = csv.reader(f)
            for row in reader:
                words.append(row[0])

        words = words[1:]
        return words

    def get_word(self, words):
        word = random.choice(words)
        self.original_word = word
        return word

    def show_hidden_word(self, word):
        word = word.replace(" ", "_")
        self.word = word
        hidden_word = []
        letter_list = list(word)
        self.letter_list = letter_list
        for i in letter_list:
            if not i.isalpha():
                hidden_word.append(i)
            else:
                hidden_word.append("*")
        self.hidden_word = hidden_word
        return hidden_word

    def check_letter(self, letter):
        if letter.upper() in self.letter_list:
            letter = letter.upper()
            x = self.letter_list.index(letter)
            self.hidden_word[x] = letter
            self.letter_list[x] = "*"
        elif letter not in self.letter_list:
            self.attempts -= 1
            self.drawing_sound.play()
        else:
            x = self.letter_list.index(letter)
            self.hidden_word[x] = letter
            self.letter_list[x] = "*"
