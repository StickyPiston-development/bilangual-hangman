# Bilingual-Hangman
*Hangman, but in two languages*
### Installation
Download the latest release. On Windows you have to get around windows defender, on linux you have to make the file executable using `chmod +x bilingual-hangman`

### Build
To build you use the following commands (with python3.11 and git):
 - `git clone https://github.com/StickyPiston-development/bilingual-hangman.git`
 - `cd bilingual-hangman`
 - `pip install -r src/requirements.txt`
 - `pyinstaller build.spec`  
You can find the build(s) in src/dist/

### Modification
You are free to edit the program, but always credit StickyPiston-development.  
#### Words
To edit the words, you place your word list in the form below in `dev/words.txt`
After that you run `dev/convert.py`

Copy the resulting `dev/words.json` to `src/assets/words.json` and build using `pyinstaller build.spec`.
The resulting file will be in `src/dist/`


```txt
lang1word1 = lang2word1
lang1word2 = lang2word2
lang1word3 = lang2word3
etc
```

#### GUI translations
All gui translations are stored as json in `src/assets/translate.json`.
The use of the values is explained by the keys.
Please note that you may need to fiddle around a bit with the x and y positions.

#### Icons
Replace the `src/assets/hangman.ico` with an ico image. 
This will change the taskbar and executable icon.
Replace the `src/assets/hangmat.png` with a transparent png image.
This will change the unix app icon (non file) and the upper left icon.

