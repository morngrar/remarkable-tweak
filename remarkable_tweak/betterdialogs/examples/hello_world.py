import betterdialogs as bd
import tkinter as tk

class Main(bd.MainFrame):
    def content(self, master):
        self.button = tk.Button(
            master,
            text="Hello World!",
            command=self.on_click_hello
        )
        self.button.pack(padx=2, pady=2, fill=tk.X)

    def on_click_hello(self):
        print("hello world!")

Main(tk.Tk(), "Hello!")
