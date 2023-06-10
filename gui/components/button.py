from tkinter import Tk, Label
from PIL.ImageTk import PhotoImage
from tkinter.messagebox import showinfo
from typing import Optional

class WButton(Label):
    
    def __init__(
        self,
        parent: Tk, 
        image_released: PhotoImage, 
        image_pressed: PhotoImage, 
        pos_x: int, 
        pos_y: int,
        height: int,
        width: int,
        command: Optional[callable] = None,
        is_toggle: bool = False,
        image_released_toggle_true: Optional[PhotoImage] = None, 
        image_pressed_toggle_true: Optional[PhotoImage] = None
    ) -> None:
        self.image_pressed = image_pressed
        self.image_released = image_released
        self.height = height
        self.width = width
        self.command = command
        self.is_toggle = is_toggle
        self.toggle = False
        self.image_released_toggle_true = image_released_toggle_true
        self.image_pressed_toggle_true = image_pressed_toggle_true
        
        super().__init__(
            master=parent,
            image=self.image_released,
            relief='sunken',
            height=self.height,
            width=self.width,
            bd=0,
            anchor="nw"
        )
        self.place(x=pos_x, y=pos_y)
        self.bind('<Button>', func=lambda event :self.button_pressed(event))
        self.bind('<ButtonRelease>', func=lambda event :self.button_released(event))
        print(self.keys())
    
    def button_pressed(self, event):
        if not self.is_toggle:
            self['image'] = self.image_pressed
        elif self.is_toggle and self.toggle:
            self['image'] = self.image_pressed_toggle_true
        elif self.is_toggle and not self.toggle:
            self['image'] = self.image_pressed

    def button_released(self, event):
        if not self.is_toggle:
            self['image'] = self.image_released
        elif self.is_toggle and self.toggle:
            self['image'] = self.image_released_toggle_true
        elif self.is_toggle and not self.toggle:
            self['image'] = self.image_released
        
        if (event.x > self.width 
            or event.x < 0
            or event.y > self.height 
            or event.y < 0
        ): 
            return
        
        if self.is_toggle:
            self.toggle = not self.toggle
        
        self.command()
        
        