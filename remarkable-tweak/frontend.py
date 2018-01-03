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

        bd.BetterDialog.__init__(self, parent, title)

    def content(self, master):
        self.tree = ttk.Treeview(master)
        scrollbar = ttk.Scrollbar(master, command=self.tree.yview)

        # Makes it so that scrollbar moves.
        self.tree['yscroll'] = scrollbar.set

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

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        print("on_double_clicked")
        self.purge_tree()
        self.populate_tree()

    def on_right_click(self, event):
        # show pop-up context menu
        self.context_menu.post(event.x_root, event.y_root)

    def on_right_click_update(self):
        # Do update-dialog
        #print("on_right_click_update called")
        item = self.tree.selection()[0]
        UpdateEntryDialog(self, title="Oppdater detektor", entry=self.tree_ids[item])
        self.purge_tree()
        self.populate_tree()

    def on_right_click_delete(self):
        # Delete relevant record from DB with delete_record()
        # Remember messagebox dialog with confirmation of delete intention.
        #print("on_right_click_delete called")
        item = self.tree.selection()[0]
        tag = self.tree_ids[item][0]
        #print("tag: ", tag)
        if mb.askquestion("Slette?", "Vil du virkelig slette denne?") == "yes":
            delete_record(tag)
            self.purge_tree()
            self.populate_tree()

