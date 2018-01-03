#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
import os

import betterdialogs as bd

class Browser(bd.BetterDialog):
    """Dialog for browsing templates."""

    def __init__(
            self,
            parent,
            template_paths,
            local_paths=None,
            title=None):

        self.parent = parent

        self.template_paths = template_paths
        self.template_names = [
            os.path.split(e)[1] for e in self.template_paths
        ]
        self.local_paths = local_paths

        self.tree_ids = {}

        # Context menu
        self.context_menu = tk.Menu(parent, tearoff=0)
        self.context_menu.add_command(
            label="Oppdater",
            command=self.on_right_click_update
        )
        self.context_menu.add_command(
            label="Slett",
            command=self.on_right_click_delete
        )
#        self.context_menu.bind("<FocusOut>", self.context_menu_focusout)

        bd.BetterDialog.__init__(self, parent, title)

    def content(self, master):
        self.tree = ttk.Treeview(master)
        scrollbar = ttk.Scrollbar(master, command=self.tree.yview)

        # Makes it so that scrollbar moves.
        self.tree['yscroll'] = scrollbar.set

        # Treeview configuration
        self.tree["columns"] = ("filenames",)
        self.tree.heading("filenames", text="Templates")
        self.tree["show"] = "headings"

        self.populate_tree()

        # TODO: Canvas-part should go here.

        # Event bindings
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Button-3>", self.on_right_click)

        self.tree.grid(row=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

    def populate_tree(self):
        """Populates the treeview with the template names."""

        for name in self.template_names:
            row_id = self.tree.insert(
                "",
                0,
                values = (name,)
            )
            self.tree_ids[row_id] = name

    def purge_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.tree_ids = {}

    def on_double_click(self, event):
        print("on_double_clicked")
        item = self.tree.selection()[0]

        # Perhaps not needed?

        self.purge_tree()
        self.populate_tree()

    def on_right_click(self, event):
        """show pop-up context menu"""

        try:
            self.context_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.context_menu.grab_release()

    def on_right_click_update(self):
        print("on_right_click_update called")
        item = self.tree.selection()[0]

        # Perhaps not needed?

        self.purge_tree()
        self.populate_tree()

    def on_right_click_delete(self):
        print("on_right_click_delete called")
        item = self.tree.selection()[0]
        name = self.tree_ids[item][0]

        # TODO: Delete template locally here

        self.purge_tree()
        self.populate_tree()


class Main(bd.MainFrame):
    def content(self, master):
        self.button = ttk.Button(
            master, text="Test", command=self.on_click_hello
        )
        self.button.pack(padx=2, pady=2, fill=tk.X)

    def on_click_hello(self):
        print("hello, world!")
        testlist = [
            "aasda",
            "asdfg",
            "kockney"
        ]

        d = Browser(self.parent, testlist)

if __name__=="__main__":



    Main(tk.Tk(), "Test")
#    dialog = Browser(main, )
