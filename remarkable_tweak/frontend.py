#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
from tkinter import messagebox as mb
import os
import shutil

import betterdialogs as bd
from remarkable_tweak import system
from remarkable_tweak import backend

class Browser(bd.BetterDialog):
    """Dialog for browsing templates."""

    def __init__(
            self,
            parent,
            master_widget,
            template_directory,
            title=None):

        self.parent = parent
        self.master_widget = master_widget
        self.result = None

        backend.clean_working_dir()
        backend.download()

        template_paths = []
        for f in os.listdir(template_directory):
            template_paths.append(os.path.join(template_directory, f))

        self.template_names = [
            os.path.split(e)[1] for e in template_paths
        ]
        self.template_paths = {}
        i = 0
        for path in template_paths:
            self.template_paths[self.template_names[i]] = path
            i += 1

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

        bd.BetterDialog.__init__(self, parent, master_widget, title)

    def content(self, master):
        """Content frame of the dialog"""

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

        for name in sorted(self.template_names, reverse=True):
            row_id = self.tree.insert(
                "",
                0,
                values = (name,)
            )
            self.tree_ids[row_id] = name

    def purge_tree(self):
        """Deletes all elements of treeview."""

        for i in self.tree.get_children():
            self.tree.delete(i)
        self.tree_ids = {}

    def refresh_tree(self):
        self.purge_tree()
        self.populate_tree()

    def add_new_template(self):
        """Opens a open-file dialog, and adds the file to templates."""

        file_path = fd.askopenfilename(
            filetypes=(("PNG images", "*.png"),)
        )
        name = os.path.split(file_path)[1]

        self.template_paths[name] = file_path
        self.template_names.append(name)

        self.refresh_tree()

    def backup(self):
        """Saves all templates currently in view to local dir."""

        if self.template_names:
            for name in self.template_names:
                shutil.copy(
                    self.template_paths[name],
                    system.BACKUP_DIR
                )

            self.master_widget.backup_button.config(state="normal")
            mb.showinfo(message="Backup taken!")


    def on_click(self, event):
        """Loads last selection into preview"""

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
        """Save selected items to selected location."""

        directory = fd.askdirectory()
        selection = [
            self.tree.item(e)["values"][0] for e in self.tree.selection()
        ]

        for name in selection:
            shutil.copy(
                self.template_paths[name],
                directory
            )


    def on_right_click_delete(self, event=None):
        """Delete all selected entries."""

        selection = set(
            [
                self.tree.item(e)["values"][0]
                for e in self.tree.selection()
            ]
        )
        superset = set(self.template_names)
        self.template_names = list(superset - selection)

        for name in selection:
            del self.template_paths[name]

        self.refresh_tree()

    def execute(self):
        """Put files to be uploaded in result variable.

        If dialog is exited in any other way, the result variable will
        be None.
        """

        self.result = self.template_paths

    def check_input(self):
        """Notifies user about uploading."""

        question = (
            "This will upload your changes to the reMarkable, and might "
            "delete some or all templates on it. Are you sure?"
        )

        answer = mb.askquestion("Upload changes?", question)

        if answer == "yes":
            return 1
        else:
            return 0

class Main(bd.MainFrame):
    """Main menu window of the application."""

    def content(self, master):
        ttk.Button(
            master, text="Browse reMarkable", command=self.on_click_browse
        ).pack(padx=2, pady=2, fill=tk.X)

        ttk.Button(
            master, text="Enter new password", command=self.on_click_password
        ).pack(padx=2, pady=2, fill=tk.X)

        self.backup_button = ttk.Button(
            master, text="Load local backup", command=self.on_click_load
        )
        self.backup_button.pack(padx=2, pady=2, fill=tk.X)

        if not os.listdir(system.BACKUP_DIR):
            self.backup_button.config(state="disabled")

    def on_click_browse(self):
        """Open browser dialog after downloading templates.

        Loads templates from .remarkable-tweak/temp. Uploads changes to
        remarkable.
        """

        try:
            backend.password()
        except:
            mb.showerror(
                    title="No password!",
                    message=(
                        "Couldn't find saved password. You should enter "
                        "the reMarkable's SSH password, and retry."
                )
            )
            return

        try:
            dialog = Browser(
                self.parent,
                self,
                system.WORKING_DIR,
                title="Browsing reMarkable"
            )
        except:
            self.connection_error()
            return

        if dialog.result:
            paths = [
               dialog.result[key] for key in dialog.result.keys()
            ]

            try:
                backend.upload(paths)
            except:
                self.connection_error()

    def on_click_password(self):
        """Saves entered password to config file."""

        dialog = bd.EntryDialog(
            self.parent,
            self,
            "Password:",
            title="Enter new password"
        )

        if dialog.result != None:
            backend.update_password(dialog.result)


    def on_click_load(self):
        """Open browser dialog on local backup"""

        dialog = Browser(
            self.parent,
            self,
            system.BACKUP_DIR,
            title="Browsing backup"
        )

        if dialog.result:
            paths = [
               dialog.result[key] for key in dialog.result.keys()
            ]

            try:
                backend.upload(paths)
            except:
                self.connection_error()

    def connection_error(self):
        mb.showerror(
            title="Error!",
            message=(
                "Something went wrong!. Make sure that your "
                "reMarkable is connected via USB, and retry."
            )
        )

if __name__=="__main__":
    Main(tk.Tk(), "Frontend test")
