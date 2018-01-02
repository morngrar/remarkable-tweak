import tkinter as tk

class MainFrame(tk.Frame):
    """Your application's main window content frame. Meant for subclassing.

    Override the content() method to add your widgets.
    """

    def __init__(self, parent, title, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.interrupt = False

        self.content_frame = tk.Frame(self, width=300, height=400)
        self.content(self.content_frame)
        self.content_frame.pack(expand=True)
        self.pack(expand=True, fill=tk.BOTH, padx=100, pady=100)

        # Center parent window
        parent.update_idletasks()
        width = parent.winfo_width()
        frame_width = parent.winfo_rootx() - parent.winfo_x()
        window_width = width + 2*frame_width
        height = parent.winfo_height()
        titlebar_height = parent.winfo_rooty() - parent.winfo_y()
        window_height = height + titlebar_height + frame_width
        x = parent.winfo_screenwidth() // 2 - window_width // 2
        y = parent.winfo_screenheight() // 2 - window_height // 2
        parent.geometry("{}x{}+{}+{}".format(width, height, x, y))

        # Run parent window
        parent.deiconify()
        parent.title(title)
        parent.resizable(False, False)
        parent.update_idletasks()
        parent.mainloop()

    def content(self, master):
        """Override this to add your content"""

        pass

if __name__=="__main__":
    class Main(MainFrame):
        def content(self, master):
            self.button = tk.Button(
                master,
                text = "Hello World!",
                command = self.on_click_hello
            )
            self.button.pack(padx=2, pady=2, fill=tk.X)

        def on_click_hello(self):
            print("hello world!")

    Main(tk.Tk(), "Hello!")
