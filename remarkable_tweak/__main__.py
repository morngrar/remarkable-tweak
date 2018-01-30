#!/usr/bin/python3

import tkinter as tk
from remarkable_tweak import frontend

def main():
    frontend.Main(tk.Tk(), "reMarkable Tweak Tool")

if __name__=="__main__":
    main()
