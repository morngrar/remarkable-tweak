#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
import re  # For geometry string parsing


def parse_geometry(geometry):
    """Takes a geometry string, returns map of parameters."""

    m = re.match("(\d+)x(\d+)([-+]\d+)([-+]\d+)", geometry)
    if not m:
        raise ValueError("failed to parse geometry string")
    return map(int, m.groups())


class BetterDialog(tk.Toplevel):
    """A simple dialog for subclassing"""

    def __init__(self, parent, master, title=None):
        tk.Toplevel.__init__(self, parent)
        self.withdraw()
        if parent.winfo_viewable():
            self.transient(parent)

        self.parent = parent
        self.master = master

        if title:
            self.title(title)

        content = tk.Frame(self, width=300, height=400)
        self.initial_focus = self.content(content)
        content.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.buttons(self)

        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        parent_params = list(parse_geometry(parent.geometry()))
        self.geometry(
            "+{}+{}".format(
                parent_params[2]+50,
                parent_params[3]+50
            )
        )

        self.deiconify()
        self.initial_focus.focus_set()
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def buttons(self, master):
        """Adds 'OK' and 'Cancel' buttons to standard button frame.

        Override if need for different configuration.
        """

        subframe = tk.Frame(master)
        subframe.pack(side=tk.RIGHT)

        ttk.Button(
            subframe,
            text="OK",
            width=10,
            command=self.ok,
            default=tk.ACTIVE
        ).pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(
            subframe,
            text="Cancel",
            width=10,
            command=self.cancel,
            default=tk.ACTIVE
        ).pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)


    def content(self, master):
        """Create dialog contentframe (everything but the button frame)

        This method should be overridden to add your content. Return
        the widget that you wish to have initial focus.
        """

        pass

    def check_input(self):
        """Method for checking that dialog input is valid.

        This method is automatically called before the dialog is
        destroyed. By default it always returns OK. Override to implement
        your input-checking to make sure the dialog doesn't accept
        invalid data.
        """

        return 1

    def execute(self):
        """Process dialog input.

        This method is called automatically after the dialog is
        destroyed. By default it does nothing. Override it to implement
        your own functionality.
        """

        pass

    def ok(self, event=None):
        """Function called when OK-button is clicked.

        This method calls check_input(), and if that returns ok it calls
        execute(), and then destroys the dialog.
        """

        if not self.check_input():
            self.initial_focus.focus_set()
            return

        self.withdraw()
        self.update_idletasks()

        try:
            self.execute()
        finally:
            self.cancel()

    def cancel(self, event=None):
        """Function called when Cancel-button clicked.

        This method returns focus to parent, and destroys the dialog.
        """

        if self.parent != None:
            self.parent.focus_set()

        self.destroy()

    def destroy(self):
        """Destroy the dialog."""

        self.initial_focus = None
        tk.Toplevel.destroy(self)

