import tkinter as tk
from PIL import ImageTk, Image  # Pillow is needed.

def load_image(canvas, filepath):
    """Takes a tk.Canvas and a filepath, loads image into canvas"""

    image_data = Image.open(filename)
    canvas.image = ImageTk.PhotoImage(image_data)
    canvas.create_image(0, 0, image=canvas.image, anchor=tk.NW)

class ImageFrame(tk.Frame):
    """A frame for adding images to GUI."""

    def __init__(
            self,
            parent,
            image=None,
            width=265,
            height=370,
            *args,
            **kwargs):

        self.parent = parent
        self.image = image
        self.width = width
        self.height = height
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.canvas_frame = tk.Frame(self)

        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=self.width,
            height=self.height
        )
        self.canvas.pack(side = tk.LEFT)
        if self.image:
            load_image(canvas, self.image)
        self.canvas_frame.pack()

    def load_image(self, imagepath, width=None, height=None):
        """Loads new image into canvas, updating size if needed."""

        if width:
            self.width = width
            self.canvas["width"] = width
        if height:
            self.height = height
            self.canvas["height"] = height

        self.image = imagepath
        load_image(self.canvas, self.image)
        self.update_idletasks()  # Might have to be done to canvas instead
