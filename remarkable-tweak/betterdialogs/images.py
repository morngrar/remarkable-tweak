from PIL import ImageTk, Image  # Pillow is needed.

def load_image(canvas, filepath):
    """Takes a tk.Canvas and a filepath to an image, loads image into canvas"""

    image_data = Image.open(filename)
    canvas.image = ImageTk.PhotoImage(image_data)
    canvas.create_image(0, 0, image=canvas.image, anchor='nw')

