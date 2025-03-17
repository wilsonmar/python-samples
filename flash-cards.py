#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

""" flash-cards.py at https://github.com/wilsonmar/python-samples/blob/main/flash-cards.py

STATUS: Working on Apple macOS sw_vers = 15.3.1 / uname = 24.3.0
git commit -m "v001 as gen'd by Perplexity :flash-cards.py"

This is a sample program that shows how to create a GUI application using tkinter.

1. In Terminal: one time to initialize run environment:
    python3 -m venv venv
    source venv/bin/activate
    brew install python-tk  # on macOS
    chmod +xflash-cards.py
2. USAGE: run command:
    ./flash-cards.py

# Gen'd by https://www.perplexity.ai/search/write-python-code-to-show-flas-ArfCeDixS_2GlAf61CJPEw#0
# https://www.datacamp.com/tutorial/gui-tkinter-python
# PyGame https://www.youtube.com/watch?v=JQAeQUZxiz4&t=51s of https://github.com/poly451/Tutorials/tree/master/Flashcards/Video02 
# CustomTkinter.com https://www.youtube.com/watch?v=Miydkti_QVE  https://www.youtube.com/watch?v=NSiGL723ykA
# TODO: PySide6 using QtDesigner https://github.com/py4all1/memory_game/tree/main/game https://www.youtube.com/watch?v=3KzLg6gBASc
$ Database of flashcards also used in an voice app (showing video?) after translation
pygame event handler https://www.youtube.com/watch?v=y9VG3Pztok8
Gamify like Duolingo
"""

import tkinter as tk
from tkinter import messagebox

# TODO: https://www.youtube.com/watch?v=eaxPK9VIkFM
class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")
        self.flashcards = [
            {"question": "What is the capital of France?", "answer": "Paris"},
            {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"},
            # TODO: Add more flashcards here from a database
        ]
        self.current_card = 0
        self.score = 0
        self.display_card()

    def display_card(self):
        self.clear_screen()
        question_label = tk.Label(self.root, text=self.flashcards[self.current_card]["question"], wraplength=400)
        question_label.pack(pady=20)
        
        entry = tk.Entry(self.root, width=50)
        entry.pack(pady=10)
        
        submit_button = tk.Button(self.root, text="Submit", command=lambda: self.check_answer(entry.get()))
        submit_button.pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def check_answer(self, user_answer):
        if user_answer.lower() == self.flashcards[self.current_card]["answer"].lower():
            self.score += 1
            messagebox.showinfo("Correct!", "Your answer is correct!")
        else:
            messagebox.showinfo("Incorrect", f"Sorry, the correct answer is {self.flashcards[self.current_card]['answer']}.")
        
        self.current_card += 1
        if self.current_card < len(self.flashcards):
            self.display_card()
        else:
            self.show_results()

    def show_results(self):
        self.clear_screen()
        result_label = tk.Label(self.root, text=f"Quiz finished! Your score is {self.score} out of {len(self.flashcards)}")
        result_label.pack(pady=20)
        restart_button = tk.Button(self.root, text="Restart", command=self.restart)
        restart_button.pack(pady=10)

    def restart(self):
        self.current_card = 0
        self.score = 0
        self.display_card()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
