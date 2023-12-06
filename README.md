# Anki Automation


## Description

Create Anki flashcard decks (cloze with an optional back-side image) from an Excel template
and a corresponding PDF. The script will attempt to match the PDF pages to the question
template as found in the Excel template and generate cards with the questions and image.

## Installing

You'll need Python 3.x installed on your machine. The script was developed and tested with
Python 3.10.10, but it should also work on other recent versions.

Before running the script, install the required Python packages using the following
command in your terminal:
```
pip install -r requirements.txt
```

## Usage

You can run the script in your Python environment or IDE. If you want to compile the script into an
executable, you can use PyInstaller by running the following command in the terminal:
```
pyinstaller --onefile make_anki_deck.py
```

Please read the associated PDF (instructions.pdf) for detailed instructions on how to use the script
to generate Anki cards.


## License

Users are free to use and distribute however they wish.