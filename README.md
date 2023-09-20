# Wordle Game Built with Pygame
This is a Python implementation of the popular game Wordle, built using Pygame. The code in this project is based on the tutorial series found [here](https://youtu.be/LP7Lja8ePpg?si=6ISR-HhaBQUqM53t) (I did not create these tutorials.) I have modified it to add some extra features (e.g. showing the QWERTY keyboard with coloured feedback), updating some game logic regarding valid/invalid words, and refactoring some parts to improve modularity and ease of modification.

## Demo
Here is a gameplay demo. (Note the screen recording and conversion to GIF have introduced some artefacts in the background and have made the animations appear less smooth.)
<br>

![wordle_clone_GIF_small](https://github.com/rg1990/pywordle/assets/70291897/0d1f33a8-8dfb-41fe-aae6-8ac8b8e7cc06)


## Summary
- There are 2,309 five-letter words used in the game, stored in `data/wordle_word_list.txt`. The user must be able to enter other words with five letters that are not in `data/wordle_word_list.txt`, so a separate text file containing many more (and many more obscure) five-letter words is also provided at `data/five_letter_words.txt`. This larger file contains around 16,000 words.
- Cell-level animations occur when the user enters a letter into a cell
- Row-level animations occur if the user's input is invalid (word contains fewer than 5 characters, or is not present in `five_letter_words.txt`.)
- The main game board tiles, and the QWERTY keyboard keys are coloured to show the feedback from previous guesses.
- Improvement: some UI element positions and animation parameter values are hard-coded. These could instead be stored in `config.py`.

## How to Play
<!--The user must correctly deduce a five-letter word by following a process of submitting guesses and receiving feedback. The feedback tells the user which letters (if any) from their guess are present in the unknown word, and provides information about the correctness of the position of the guessed letter. If a letter from the user's guess is present in the unknown word, but is in the wrong place, the letter will be coloured orange. If the letter from the user's guess is present in the unknown word, and it is also in the correct place, the letter will be coloured green. -->

- Guess a five-letter word using the keyboard.
- Press the Enter key to submit your guess.
- The game will provide feedback on your guess:
  - Correct letters in the correct position are highlighted green.
  - Correct letters in the wrong position are highlighted orange.
- Continue guessing until you solve the puzzle or run out of attempts.

The user has six attempts to deduce the unknown word. If they fail, the game is over and the solution is displayed at the top of the window.

## Prerequisites
- Python 3.x
- PyGame (install via pip)

## Extra Features
The following extra features could be added:
- A timer to time the user's game.
- A scoring system.
- Multiple user profiles, each containing records of previous scores and times.


## Licence
This project is licensed under the MIT Licence.

---
The list of valid five-letter words is a subset of the list found [here](https://github.com/dwyl/english-words/tree/master). I have not checked this list for inappropriate words.
