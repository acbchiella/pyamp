from PIL import ImageTk, Image
import tkinter as tk
from tkinter import filedialog as fd


def from_rgb(self, rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb



class FileDialog(tk.Tk): # inherits from the tk.Tk class

    def __init__(self):
        super().__init__()
        self.withdraw() # prevents Tkinter window from displaying

    def open(self):
        return fd.askopenfilename(self)

    def saveas(self):
        return fd.asksaveasfilename()