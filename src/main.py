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


# Load in config
try:
    # Load in translations
    with open(resource_path("assets/translate.json"), "r", encoding='utf-8') as translate:
        translations = json.load(translate)
    # Load in word list
    with open(resource_path("assets/words.json"), "r", encoding='utf-8') as words:
        wordList = json.load(words)
except FileNotFoundError:
    # THIS IS NOT TRANSLATED BECAUSE WE DON'T WANT A CRASH ONCE IT CANT FIND THE FILES. WE WANT THIS ERROR MESSAGE
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
        if games <= 0:
            raise ValueError
    except IndexError:
        print(translations["log"]["args"]["noneFound"])
        sys.exit(1)
    except ValueError:
        print(translations["log"]["args"]["invalid"].replace("[AMOUNT]", sys.argv[sys.argv.index('--games') + 1]))
        sys.exit(1)


class HangmanMenu:
    def __init__(self, pos, gameCount=0, score=0, showButtons=True):
        if debug:
            print(f"==== MENU ====\npos: {pos}, games: {gameCount}, score: {score}, showButtons: {showButtons}")
        if not games == "INFINITE" and gameCount == 0:
            main()
            return

        self.win = GraphWin(translations["gui"]["menuName"], width, height)
        self.win.setBackground("#121212")

        self.games = gameCount
        self.score = score
        self.showbuttons = showButtons

        self.scoreDisplay = None

        self.playbutton = None
        self.playbuttontext = None
        self.exitbutton = None
        self.exitbuttontext = None

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

        self.win.after(1, lambda: self.win.focus_force())

        self.build_gui()

        if self.showbuttons:
            self.listen_click()
        else:
            try:
                self.win.getMouse()
            except GraphicsError:
                sys.exit()

    def build_gui(self):
        if debug:
            print("Building main menu")

        title = Text(Point(width / 2, 50), translations["gui"]["menuName"]).draw(self.win)
        title.setOutline("white")
        title.setSize(self.textsize)
        if self.games == 0:
            self.playbutton = Rectangle(Point(width / 2 - 100, 100), Point(width / 2 + 100, 150)).draw(self.win)
            self.playbutton.setOutline("white")
            self.playbuttontext = Text(Point(width / 2, 125), translations["gui"]["playButtonText"]).draw(self.win)
            self.playbuttontext.setOutline("white")

            self.exitbutton = Rectangle(Point(width / 2 - 100, 170), Point(width / 2 + 100, 225)).draw(self.win)
            self.exitbutton.setOutline("white")
            self.exitbuttontext = Text(Point(width / 2, 200), translations["gui"]["exitButtonText"]).draw(self.win)
            self.exitbuttontext.setOutline("white")

        else:
            self.scoreDisplay = Text(Point(width / 2, 100), f"""{translations["gui"]["score"]}: {self.score}""").draw(
                self.win)
            self.scoreDisplay.setOutline("white")
            self.scoreDisplay.setSize(self.textsize)

            self.scoreDisplay = Text(Point(width / 2, 150), f"""{translations["gui"]["games"]}: {self.games}""").draw(
                self.win)
            self.scoreDisplay.setOutline("white")
            self.scoreDisplay.setSize(self.textsize)

            if self.showbuttons:
                self.playbutton = Rectangle(Point(width / 2 - 100, 175), Point(width / 2 + 100, 225)).draw(self.win)
                self.playbutton.setOutline("white")
                self.playbuttontext = Text(Point(width / 2, 200), translations["gui"]["playButtonText"]).draw(self.win)
                self.playbuttontext.setOutline("white")

                self.exitbutton = Rectangle(Point(width / 2 - 100, 250), Point(width / 2 + 100, 300)).draw(self.win)
                self.exitbutton.setOutline("white")
                self.exitbuttontext = Text(Point(width / 2, 275), translations["gui"]["exitButtonText"]).draw(self.win)
                self.exitbuttontext.setOutline("white")

    def listen_click(self):
        while True:
            try:
                click = self.win.checkMouse()
                ll = self.playbutton.getP1()
                ur = self.playbutton.getP2()

                if ll.getX() < click.getX() < ur.getX() and ll.getY() < click.getY() < ur.getY():
                    if debug:
                        print("Clicked on playbutton")
                    pos = self.win.master.geometry()
                    self.win.close()
                    main(pos)

                ll = self.exitbutton.getP1()
                ur = self.exitbutton.getP2()

                if ll.getX() < click.getX() < ur.getX() and ll.getY() < click.getY() < ur.getY():
                    if debug:
                        print("Clicked on exitbutton")
                    self.win.close()
                    sys.exit()

                if self.win.checkKey() == "escape":
                    if debug:
                        print(translations["log"]["exit"])
                    self.win.close()
                    sys.exit()

            except GraphicsError:
                sys.exit()
            except AttributeError:
                pass


class Hangman:
    def __init__(self, solution, pos, gameCount):
        self.win = GraphWin(translations["gui"]["gameName"].replace("[GAME]", str(gameCount)), width, height, autoflush=False)
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

        self.win.after(1, lambda: self.win.focus_force())

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

        update()
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
        update()

    def head(self):
        p1 = Point(520, 200)
        Circle(p1, 50).draw(self.win).setOutline("white")
        update()

    def chest(self):
        p1 = Point(440, 250)
        p2 = Point(600, 500)
        Oval(p1, p2).draw(self.win).setOutline("white")
        update()

    def arm_left(self):
        p1 = Point(570, 290)
        p2 = Point(600, 440)
        Oval(p1, p2).draw(self.win).setOutline("white")
        update()

    def arm_right(self):
        p1 = Point(470, 290)
        p2 = Point(440, 440)
        Oval(p1, p2).draw(self.win).setOutline("white")
        update()

    def leg_left(self):
        p1 = Point(540, 450)
        p2 = Point(580, 580)
        Oval(p1, p2).draw(self.win).setOutline("white")
        update()

    def leg_right(self):
        p1 = Point(500, 450)
        p2 = Point(460, 580)
        Oval(p1, p2).draw(self.win).setOutline("white")
        update()

    def display_word(self):
        for i in self.DisplayWord1:
            i.undraw()
        self.DisplayWord1 = []
        p = 10
        for i in self.solution[0]:
            p += 25
            if i == " ":
                pass
            elif strip_accents(i).lower() in self.guessed or not i.isalpha():
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
            elif strip_accents(i).lower() in self.guessed or not i.isalpha():
                self.DisplayWord2.append(Text(Point(p, 530), i).draw(self.win))
                self.DisplayWord2[len(self.DisplayWord2) - 1].setOutline("white")
                self.DisplayWord2[len(self.DisplayWord2) - 1].setSize(self.textsize)
        update()

    def display_guessed(self):
        for i in self.DisplayGuessed:
            i.undraw()
        self.DisplayGuessed = []
        p = 10
        for i in self.guessed:
            p += 25
            if i == " ":
                pass
            color = "green" if i.lower() in strip_accents(self.solution[0] + self.solution[1]).lower() else "red"
            self.DisplayGuessed.append(Text(Point(p, 570), i).draw(self.win))
            self.DisplayGuessed[len(self.DisplayGuessed) - 1].setOutline(color)
            self.DisplayGuessed[len(self.DisplayGuessed) - 1].setSize(self.textsize)
        update()

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
                update()
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
                update()
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
                update()
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
                update()
        time.sleep(1)

    def update_score(self, score):
        self.scoreDisplay.undraw()
        self.scoreDisplay = Text(Point(50, 50), score).draw(self.win)
        self.scoreDisplay.setOutline("white")
        self.scoreDisplay.setSize(self.textsize)
        update()

    def get_pos(self):
        return self.win.master.geometry()


def game(score, pos, gameCount):
    solution = random.choice(list(wordList.items()))
    if debug:
        print(f"solution: {solution}")

    hangman = Hangman(solution, pos, gameCount)
    hangman.update_score(score)

    lives = 6
    hangman.display_word()
    while lives != 0:
        letter = hangman.win.getKey().lower()
        if letter == "escape":
            message = translations["log"]["exit"]
            pos = hangman.get_pos()
            hangman.win.close()

            if debug:
                print(f"{message}: {letter}")

            return [pos]
        elif len(letter) != 1:
            message = translations["log"]["unknown"]
        elif letter in hangman.guessed:
            message = translations["log"]["already_chose"]
        elif letter in strip_accents(solution[0]).lower() or letter in strip_accents(solution[1]).lower():
            message = translations["log"]["correct"]
            hangman.guessed.append(letter)
        else:
            message = translations["log"]["incorrect"]
            hangman.guessed.append(letter)
            lives -= 1

        if debug:
            print(f"{message}: {letter}")

        hangman.display_word()
        hangman.display_guessed()

        counter = 0
        for i in solution[0]:
            if strip_accents(i).lower() in hangman.guessed or not i.isalpha():
                counter += 1
        if counter == len(solution[0]):
            counter = 0
            for i in solution[1]:
                if strip_accents(i).lower() in hangman.guessed or not i.isalpha():
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


def main(pos="None"):
    score = 0
    gameCount = 0

    if games == "INFINITE":
        while True:
            try:
                if debug:
                    print(f"=== NEW GAME ===\ngame: {gameCount + 1}")

                game_results = game(score, pos, gameCount + 1)
                pos = game_results[1]

                if game_results[0]:
                    score += 10
                    message = translations["log"]["game_won"]
                else:
                    score -= 5
                    message = translations["log"]["game_lost"]

                if debug:
                    print(f"{message}\ngui position: {pos}")

                gameCount += 1

            except GraphicsError:
                break
            except IndexError:
                pos = game_results[0]
                break
        HangmanMenu(pos, gameCount, score, True)

    else:
        try:
            for gameCount in range(games):
                if debug:
                    print(f"=== NEW GAME ===\ngame {gameCount + 1}")

                game_results = game(score, pos, gameCount + 1)
                pos = game_results[1]

                if game_results[0]:
                    score += 10
                    message = translations["log"]["game_won"]
                else:
                    score -= 5
                    message = translations["log"]["game_lost"]
                if debug:
                    print(f"{message}\ngui position: {pos}")
            gameCount += 1
        except GraphicsError:
            if gameCount == 0:
                return
        except IndexError:
            pos = game_results[0]
        if debug:
            print(f"score: {score} in {gameCount} games ({score / (gameCount)}/10.0)")
        HangmanMenu(pos, gameCount, score, False)


if __name__ == "__main__":
    HangmanMenu("None", 0, 0, games == "INFINITE")
    sys.exit(0)
