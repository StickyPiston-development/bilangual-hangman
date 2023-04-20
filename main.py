import json, random, unicodedata
from graphics import *
import random, time

guessed = []

with open("words.json", "r", encoding='utf-8') as words:
    wordList = json.load(words)
    solution = random.choice(list(wordList.items()))
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

        text = Text(Point(70, 420), "word: ").draw(self.win)
        text.setOutline("white")
        text.setSize(24)
        p = 10
        self.DisplayWord1 = []
        for i in solution[0]:
            p += 25
            if i == " " or not i.isalpha():
                pass
            else:
                text = Text(Point(p, 450), "_").draw(self.win)
                text.setOutline("white")
                text.setSize(24)

        text = Text(Point(70, 500), "word: ").draw(self.win)
        text.setOutline("white")
        text.setSize(24)
        p = 10
        self.DisplayWord2 = []
        for i in solution[1]:
            p += 25
            if i == " " or not i.isalpha():
                pass
            else:
                text = Text(Point(p, 530), "_").draw(self.win)
                text.setOutline("white")
                text.setSize(24)

        self.DisplayGuessed = []

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
        p1 = Point(530, 290)
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
        for i in self.DisplayWord1:
            i.undraw()
        self.DisplayWord1 = []
        p = 10
        for i in solution[0]:
            p += 25
            if i == " ":
                pass
            elif strip_accents(i) in guessed or not i.isalpha():
                self.DisplayWord1.append(Text(Point(p, 450), i).draw(self.win))
                self.DisplayWord1[len(self.DisplayWord1) - 1].setOutline("white")
                self.DisplayWord1[len(self.DisplayWord1) - 1].setSize(24)
        for i in self.DisplayWord2:
            i.undraw()
        self.DisplayWord2 = []
        p = 10
        for i in solution[1]:
            p += 25
            if i == " ":
                pass
            elif strip_accents(i) in guessed or not i.isalpha():
                self.DisplayWord2.append(Text(Point(p, 530), i).draw(self.win))
                self.DisplayWord2[len(self.DisplayWord2) - 1].setOutline("white")
                self.DisplayWord2[len(self.DisplayWord2) - 1].setSize(24)

    def display_guessed(self):
        for i in self.DisplayGuessed:
            i.undraw()
        self.DisplayGuessed = []
        p = 10
        for i in guessed:
            p += 25
            if i == " ":
                pass
            color = "green" if i in strip_accents(solution[0] + solution[1]) else "red"
            self.DisplayGuessed.append(Text(Point(p, 570), i).draw(self.win))
            self.DisplayGuessed[len(self.DisplayGuessed) - 1].setOutline(color)
            self.DisplayGuessed[len(self.DisplayGuessed) - 1].setSize(24)

    def defeat(self):
        p = 10
        for i in solution[0]:
            p += 25
            if i == " ":
                pass
            elif not strip_accents(i) in guessed:
                time.sleep(0.2)
                self.DisplayWord1.append(Text(Point(p, 450), i).draw(self.win))
                self.DisplayWord1[len(self.DisplayWord1) - 1].setOutline("red")
                self.DisplayWord1[len(self.DisplayWord1) - 1].setSize(24)
        p = 10
        for i in solution[1]:
            p += 25
            if i == " ":
                pass
            elif not strip_accents(i) in guessed:
                time.sleep(0.2)
                self.DisplayWord1.append(Text(Point(p, 530), i).draw(self.win))
                self.DisplayWord1[len(self.DisplayWord1) - 1].setOutline("red")
                self.DisplayWord1[len(self.DisplayWord1) - 1].setSize(24)
        time.sleep(1)

    def success(self):
        p = 10
        for i in solution[0]:
            p += 25
            if i == " ":
                pass
            else:
                time.sleep(0.2)
                self.DisplayWord1.append(Text(Point(p, 450), i).draw(self.win))
                self.DisplayWord1[len(self.DisplayWord1) - 1].setOutline("green")
                self.DisplayWord1[len(self.DisplayWord1) - 1].setSize(24)
        p = 10
        for i in solution[1]:
            p += 25
            if i == " ":
                pass
            else:
                time.sleep(0.2)
                self.DisplayWord1.append(Text(Point(p, 530), i).draw(self.win))
                self.DisplayWord1[len(self.DisplayWord1) - 1].setOutline("green")
                self.DisplayWord1[len(self.DisplayWord1) - 1].setSize(24)
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
        elif letter in strip_accents(solution[0]) or letter in strip_accents(solution[1]):
            guessed.append(letter)
        else:
            print("Wrong letter")
            guessed.append(letter)
            lives -= 1

        hangman.display_word()
        hangman.display_guessed()

        counter = 0
        for i in solution[0]:
            if strip_accents(i) in guessed or not i.isalpha():
                counter += 1
        if counter == len(solution[0]):
            counter = 0
            for i in solution[1]:
                if strip_accents(i) in guessed or not i.isalpha():
                    counter += 1
            if counter == len(solution[1]):
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


main()
