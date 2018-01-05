#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
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
        self.result = None

        self.template_names = [os.path.split(e)[1] for e in template_paths]
        self.template_paths = {}
        i = 0
        for path in template_paths:
            self.template_paths[self.template_names[i]] = path
            i += 1

        self.local_paths = local_paths


        # Context menu
        self.context_menu = tk.Menu(parent, tearoff=0)
        self.context_menu.add_command(
            label="Save local copy",
            command=self.on_right_click_copy
        )
        self.context_menu.add_command(
            label="Delete",
            command=self.on_right_click_delete
        )

        bd.BetterDialog.__init__(self, parent, title)

    def content(self, master):
        """Widgets and their bindings in the content frame of the dialog"""

        self.tree = ttk.Treeview(master)
        self.tree_ids = dict()

        scrollbar = ttk.Scrollbar(master, command=self.tree.yview)

        # Makes it so that scrollbar moves.
        self.tree['yscroll'] = scrollbar.set

        # Treeview configuration
        self.tree["columns"] = ("filenames",)
        self.tree.heading("filenames", text="Templates")
        self.tree["show"] = "headings"

        self.populate_tree()

        self.image_frame = bd.images.ImageFrame(
            master,
            width=1404/4,
            height=1872/4,
        )

        # Event bindings
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<ButtonRelease-3>", self.on_right_click)
        self.tree.bind("<Delete>", self.on_right_click_delete)
        self.tree.bind("<ButtonRelease-1>", self.on_click)

        self.tree.grid(row=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.image_frame.grid(row=0, column=2, sticky="nw")

        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)


    
    def buttons(self, master):
        """Overridden. Adds buttons to lower frame."""

        leftframe = tk.Frame(master)
        leftframe.pack(side=tk.LEFT)
        rightframe = tk.Frame(master)
        rightframe.pack(side=tk.RIGHT)

        ttk.Button(
            leftframe,
            text="Take backup",
            width=10,
            command=self.backup,
            default=tk.ACTIVE
        ).pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(
            rightframe,
            text="Add new",
            width=10,
            command=self.add_new_template,
            default=tk.ACTIVE
        ).pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(
            rightframe,
            text="Upload",
            width=10,
            command=self.ok,
            default=tk.ACTIVE
        ).pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(
            rightframe,
            text="Cancel",
            width=10,
            command=self.cancel,
            default=tk.ACTIVE
        ).pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

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

    def refresh_tree(self):
        self.purge_tree()
        self.populate_tree()

    def add_new_template(self):
        # - 'Add new template'
        #   - Spawns file-open dialog
        #   - Adds file path to template_paths
        #   - Refresh treeview
        file_path = fd.askopenfilename()
        name = os.path.split(file_path)[1]

        self.template_paths[name] = file_path
        print(self.template_paths)
        self.template_names.append(name)
        print(self.template_names)
        self.template_names.sort()
        print(self.template_names)

        self.refresh_tree()

    def backup(self):
        """Saves all templates currently in view to local dir."""
        pass

    def on_click(self, event):
        print("on_click")

        selection = self.tree.focus()
        item = self.tree.item(selection)
        name = item["values"][0]

        self.image_frame.load_image(self.template_paths[name])

    def on_double_click(self, event):
        pass

    def on_right_click(self, event):
        """Show pop-up context menu"""

        self.context_menu.tk_popup(event.x_root, event.y_root, 0)
#        try:
#            self.context_menu.tk_popup(event.x_root, event.y_root, 0)
#        finally:
#            self.context_menu.grab_release()

    def on_right_click_copy(self):
        """Open file save dialog. Save a copy to selected location."""

        # TODO: filesavedialog here
        pass

    def on_right_click_delete(self, event=None):
        print("on_right_click_delete called")

        selection = set(
            [self.tree.item(e)["values"][0] for e in self.tree.selection()]
        )
        superset = set(self.template_names)
        self.template_names = list(superset - selection)

        for name in self.template_names:
            del self.template_paths[name]

        self.refresh_tree()

    def execute(self):
        # TODO: Do remote purge and upload. After having gotten permission
        # from message box. Finally remove local cache.
        # NO: simply put list of local paths to be uploaded into
        # result variable! Let backend do the rest.
        self.result = self.template_paths


class Main(bd.MainFrame):
    def content(self, master):
        self.button = ttk.Button(
            master, text="Test", command=self.on_click_hello
        )
        self.button.pack(padx=2, pady=2, fill=tk.X)

    def on_click_hello(self):
        print("hello, world!")

        testlist = []
        for f in os.listdir("backup"):
            testlist.append(os.path.join("backup/", f))
        d = Browser(self.parent, testlist)

        print(d.result)

if __name__=="__main__":
    Main(tk.Tk(), "Test")
