import json, random, unicodedata
from graphics import *
import random, time

guessed = []

with open("words.json", "r", encoding='utf-8') as words:
    wordList = json.load(words)
    solution = random.choice(list(wordList.items()))[0]
    print(wordList)
    print(solution)


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


class Hangman:
    def __init__(self):
        self.win = GraphWin("Hangman", 800, 600)
        self.win.setBackground("#121212")
        text = Text(Point(70, 530), "word: ").draw(self.win)
        text.setOutline("white")
        text.setSize(24)

        p = 10
        self.DisplayWord = []
        for i in solution:
            p += 25
            if i == " " or not i.isalpha():
                pass
            else:
                text = Text(Point(p, 570), "_").draw(self.win)
                text.setOutline("white")
                text.setSize(24)

    def pole(self):
        p1 = Point(700, 600)
        p2 = Point(720, 100)
        Rectangle(p1, p2).draw(self.win).setOutline("white")

        p1 = Point(500, 100)
        p2 = Point(720, 120)
        Rectangle(p1, p2).draw(self.win).setOutline("white")

        p1 = Point(700, 200)
        p2 = Point(520, 120)
        Line(p1, p2).draw(self.win).setOutline("white")

        p1 = Point(520, 120)
        p2 = Point(520, 150)
        Line(p1, p2).draw(self.win).setOutline("white")

    def head(self):
        p1 = Point(520, 200)
        Circle(p1, 50).draw(self.win).setOutline("white")

    def chest(self):
        p1 = Point(440, 250)
        p2 = Point(600, 500)
        Oval(p1, p2).draw(self.win).setOutline("white")

    def arm_left(self):
        p1 = Point(570, 290)
        p2 = Point(600, 440)
        Oval(p1, p2).draw(self.win).setOutline("white")

    def arm_right(self):
        p1 = Point(470, 290)
        p2 = Point(440, 440)
        Oval(p1, p2).draw(self.win).setOutline("white")

    def leg_left(self):
        p1 = Point(540, 450)
        p2 = Point(580, 580)
        Oval(p1, p2).draw(self.win).setOutline("white")

    def leg_right(self):
        p1 = Point(500, 450)
        p2 = Point(460, 580)
        Oval(p1, p2).draw(self.win).setOutline("white")

    def display_word(self):
        for i in self.DisplayWord:
            i.undraw()
        self.DisplayWord = []
        p = 10
        for i in solution:
            p += 25
            if i == " ":
                pass
            elif strip_accents(i) in guessed or not i.isalpha():
                self.DisplayWord.append(Text(Point(p, 570), i).draw(self.win))
                self.DisplayWord[len(self.DisplayWord) - 1].setOutline("white")
                self.DisplayWord[len(self.DisplayWord) - 1].setSize(24)

    def defeat(self):
        p = 10
        for i in solution:
            p += 25
            if i == " ":
                pass
            elif not strip_accents(i) in guessed:
                time.sleep(0.2)
                self.DisplayWord.append(Text(Point(p, 570), i).draw(self.win))
                self.DisplayWord[len(self.DisplayWord) - 1].setOutline("red")
                self.DisplayWord[len(self.DisplayWord) - 1].setSize(24)

    def success(self):
        p = 10
        for i in solution:
            p += 25
            if i == " ":
                pass
            else:
                time.sleep(0.2)
                self.DisplayWord.append(Text(Point(p, 570), i).draw(self.win))
                self.DisplayWord[len(self.DisplayWord) - 1].setOutline("green")
                self.DisplayWord[len(self.DisplayWord) - 1].setSize(24)
        time.sleep(1)

def main():
    hangman = Hangman()
    """
    hangman.pole()
    hangman.head()
    hangman.chest()
    hangman.arm_left()
    hangman.arm_right()
    hangman.leg_left()
    hangman.leg_right()
    hangman.display_word()
    """

    lives = 8
    hangman.display_word()
    while lives != 0:
        letter = hangman.win.getKey().lower()
        if letter in guessed:
            print("You did already choose this item.")
        elif letter in solution:
            print(letter)
            guessed.append(letter)
        else:
            print("Wrong letter")
            guessed.append(letter)
            lives -= 1

        hangman.display_word()

        counter = 0
        for i in solution:
            if i in guessed or not i.isalpha():
                counter += 1
        if counter == len(solution):
            hangman.success()
            break

        match lives:
            case 7:
                hangman.pole()
            case 6:
                hangman.head()
            case 5:
                hangman.chest()
            case 4:
                hangman.arm_left()
            case 3:
                hangman.arm_right()
            case 2:
                hangman.leg_left()
            case 1:
                hangman.leg_right()
            case 0:
                hangman.defeat()
        print(guessed)
        print(lives)


main()
