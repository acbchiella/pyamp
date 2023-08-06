from tkinter import Canvas
from typing import Optional, Tuple, Dict
from PIL.ImageTk import PhotoImage

class Label():
    
    def __init__(
        self,
        canvas: Canvas,
        coord: Tuple,
        text: str,
        font: Dict[str, PhotoImage],
        shift: int = 0,
        is_scroll: bool = False
    ) -> None:
        
        self.canvas = canvas
        self.coord = coord
        self.font = font
        self.text = text.upper()
        self.shift = shift
        
        self.create_label()
        
        return
    
    def create_label(self):
        x0 = self.coord[0]
        x1 = self.coord[2]
        y0 = self.coord[1]
        y1 = self.coord[3]
        
        self.width = x1 - x0
        first_font_element = list(self.font.items())[0][1]
        font_width = first_font_element.width()
        # self.canvas.create_image(font_width + x0, 0 + y0, image=self.font[self.text[0]], anchor="nw")
        max_label_chars = self.width // font_width
        print(max_label_chars)
        for i in range(len(self.text)):
            if i > max_label_chars - 1:
                break
            self.canvas.create_image((font_width + self.shift)*i + x0, y0, image=self.font[self.text[i]], anchor="nw")
    
    def refresh(self, font):
        self.font = font
        self.create_label()