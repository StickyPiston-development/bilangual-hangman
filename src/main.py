import json, random, unicodedata
import sys
from tkinter import PhotoImage
from graphics import *
import random, time

# DECLARATIONS
width = 800
height = 600


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


try:
    # Load in translations
    with open(resource_path("assets/translate.json"), "r", encoding='utf-8') as translate:
        translations = json.load(translate)
    # Load in word list
    with open(resource_path("assets/words.json"), "r", encoding='utf-8') as words:
        wordList = json.load(words)
except FileNotFoundError:
    print("Config files not found")
    sys.exit(1)

# Process command line args
debug = False
games = "INFINITE"

if "--debug" in sys.argv:
    debug = True
if "--games" in sys.argv:
    try:
        games = int(sys.argv[sys.argv.index("--games") + 1])
    except IndexError:
        print("Invalid game amount")
        sys.exit(1)
    except ValueError:
        print("Invalid game amount")
        sys.exit(1)

class Hangman:
    def __init__(self, solution, pos):
        self.win = GraphWin("Hangman", width, height)
        self.win.setBackground("#121212")

        # Set position to middle
        if pos == "None":
            x = self.win.winfo_screenwidth() // 2 - width // 2
            y = self.win.winfo_screenheight() // 2 - height // 2
            self.win.master.geometry(f"{width}x{height}+{x}+{y}")
        else:
            self.win.master.geometry(pos)

        self.textsize = 16 if os.name == "posix" else 24

        # Fix icon
        img = PhotoImage(file=resource_path('assets/hangman.png'), master=self.win.master)
        self.win.master.iconphoto(False, img)
        self.win.master.wm_iconphoto(False, img)

        self.solution = solution
        self.guessed = []

        self.scoreDisplay = Text(Point(50, 50), 0).draw(self.win)
        self.scoreDisplay.setOutline("white")
        self.scoreDisplay.setSize(self.textsize)

        text = Text(Point(translations["lang1"]["word_x"], 420), translations["lang1"]["word"]).draw(self.win)
        text.setOutline("white")
        text.setSize(self.textsize)

        p = 10
        self.DisplayWord1 = []
        for i in solution[0]:
            p += 25
            if i == " " or not i.isalpha():
                pass
            else:
                text = Text(Point(p, 450), "_").draw(self.win)
                text.setOutline("white")
                text.setSize(self.textsize)

        text = Text(Point(translations["lang2"]["word_x"], 500), translations["lang2"]["word"]).draw(self.win)
        text.setOutline("white")
        text.setSize(self.textsize)
        p = 10
        self.DisplayWord2 = []
        for i in solution[1]:
            p += 25
            if i == " " or not i.isalpha():
                pass
            else:
                text = Text(Point(p, 530), "_").draw(self.win)
                text.setOutline("white")
                text.setSize(self.textsize)

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
        for i in self.DisplayWord1:
            i.undraw()
        self.DisplayWord1 = []
        p = 10
        for i in self.solution[0]:
            p += 25
            if i == " ":
                pass
            elif strip_accents(i) in self.guessed or not i.isalpha():
                self.DisplayWord1.append(Text(Point(p, 450), i).draw(self.win))
                self.DisplayWord1[len(self.DisplayWord1) - 1].setOutline("white")
                self.DisplayWord1[len(self.DisplayWord1) - 1].setSize(self.textsize)
        for i in self.DisplayWord2:
            i.undraw()
        self.DisplayWord2 = []
        p = 10
        for i in self.solution[1]:
            p += 25
            if i == " ":
                pass
            elif strip_accents(i) in self.guessed or not i.isalpha():
                self.DisplayWord2.append(Text(Point(p, 530), i).draw(self.win))
                self.DisplayWord2[len(self.DisplayWord2) - 1].setOutline("white")
                self.DisplayWord2[len(self.DisplayWord2) - 1].setSize(self.textsize)

    def display_guessed(self):
        for i in self.DisplayGuessed:
            i.undraw()
        self.DisplayGuessed = []
        p = 10
        for i in self.guessed:
            p += 25
            if i == " ":
                pass
            color = "green" if i in strip_accents(self.solution[0] + self.solution[1]) else "red"
            self.DisplayGuessed.append(Text(Point(p, 570), i).draw(self.win))
            self.DisplayGuessed[len(self.DisplayGuessed) - 1].setOutline(color)
            self.DisplayGuessed[len(self.DisplayGuessed) - 1].setSize(self.textsize)

    def defeat(self):
        p = 10
        for i in self.solution[0]:
            p += 25
            if i == " ":
                pass
            elif not strip_accents(i) in self.guessed:
                time.sleep(0.2)
                self.DisplayWord1.append(Text(Point(p, 450), i).draw(self.win))
                self.DisplayWord1[len(self.DisplayWord1) - 1].setOutline("red")
                self.DisplayWord1[len(self.DisplayWord1) - 1].setSize(self.textsize)
        p = 10
        for i in self.solution[1]:
            p += 25
            if i == " ":
                pass
            elif not strip_accents(i) in self.guessed:
                time.sleep(0.2)
                self.DisplayWord1.append(Text(Point(p, 530), i).draw(self.win))
                self.DisplayWord1[len(self.DisplayWord1) - 1].setOutline("red")
                self.DisplayWord1[len(self.DisplayWord1) - 1].setSize(self.textsize)
        time.sleep(1)

    def success(self):
        p = 10
        for i in self.solution[0]:
            p += 25
            if i == " ":
                pass
            else:
                time.sleep(0.2)
                self.DisplayWord1.append(Text(Point(p, 450), i).draw(self.win))
                self.DisplayWord1[len(self.DisplayWord1) - 1].setOutline("green")
                self.DisplayWord1[len(self.DisplayWord1) - 1].setSize(self.textsize)
        p = 10
        for i in self.solution[1]:
            p += 25
            if i == " ":
                pass
            else:
                time.sleep(0.2)
                self.DisplayWord1.append(Text(Point(p, 530), i).draw(self.win))
                self.DisplayWord1[len(self.DisplayWord1) - 1].setOutline("green")
                self.DisplayWord1[len(self.DisplayWord1) - 1].setSize(self.textsize)
        time.sleep(1)

    def update_score(self, score):
        self.scoreDisplay.undraw()
        self.scoreDisplay = Text(Point(50, 50), score).draw(self.win)
        self.scoreDisplay.setOutline("white")
        self.scoreDisplay.setSize(self.textsize)

    def get_pos(self):
        return self.win.master.geometry()


def game(score, pos):
    solution = random.choice(list(wordList.items()))
    if debug:
        print(solution)

    hangman = Hangman(solution, pos)
    hangman.update_score(score)

    lives = 6
    hangman.display_word()
    while lives != 0:
        letter = hangman.win.getKey().lower()
        if len(letter) != 1:
            message = translations["log"]["unknown"]
        elif letter in hangman.guessed:
            message = translations["log"]["already_chose"]
        elif letter in strip_accents(solution[0]) or letter in strip_accents(solution[1]):
            message = translations["log"]["correct"]
            hangman.guessed.append(letter)
        else:
            message = translations["log"]["incorrect"]
            hangman.guessed.append(letter)
            lives -= 1

        if debug:
            print(message)

        hangman.display_word()
        hangman.display_guessed()

        counter = 0
        for i in solution[0]:
            if strip_accents(i) in hangman.guessed or not i.isalpha():
                counter += 1
        if counter == len(solution[0]):
            counter = 0
            for i in solution[1]:
                if strip_accents(i) in hangman.guessed or not i.isalpha():
                    counter += 1
            if counter == len(solution[1]):
                hangman.success()
                pos = hangman.get_pos()
                hangman.win.close()
                return [True, pos]

        match lives:
            case 5:
                hangman.pole()
            case 4:
                hangman.head()
            case 3:
                hangman.chest()
            case 2:
                hangman.arm_left()
                hangman.arm_right()
            case 1:
                hangman.leg_left()
                hangman.leg_right()
            case 0:
                hangman.defeat()
                pos = hangman.get_pos()
                hangman.win.close()
                return [False, pos]


def main():
    score = 0
    pos = "None"

    if games == "INFINITE":
        while True:
            try:
                game_results = game(score, pos)
                pos = game_results[1]
                if debug:
                    print(pos, game_results[1])

                if game_results[0]:
                    score += 10
                else:
                    score -= 5

            except GraphicsError:
                break
    else:
        for i in range(games):
            try:
                game_results = game(score, pos)
                pos = game_results[1]
                if debug:
                    print(pos, game_results[1])

                if game_results[0]:
                    score += 10
                else:
                    score -= 5

            except GraphicsError:
                break
    if debug:
        print(f"Score: {score}")


if __name__ == "__main__":
    main()
    sys.exit(0)
