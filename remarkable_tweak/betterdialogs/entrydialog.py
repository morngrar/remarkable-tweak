#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from betterdialog import BetterDialog

class EntryDialog(BetterDialog):

    def __init__(self, parent, prompt, title=None):
        self.text = tk.StringVar()
        self.prompt = prompt
        self.result = None

        BetterDialog.__init__(self, parent, title)

    def content(self, master):
        ttk.Label(master, text=self.prompt).grid(row=0)
        self.entry = ttk.Entry(master, textvariable=self.text)
        self.entry.grid(row=0, column=1)
        return self.entry

    def execute(self):
        self.result = self.text.get()

if __name__ == "__main__":
    d = EntryDialog(tk.Tk(), "test")
    print(d.result)
