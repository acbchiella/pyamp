from tkinter import Tk, Label, Menu
from PIL.ImageTk import PhotoImage
from tkinter.messagebox import showinfo
from typing import Optional, Dict, Union

class WButton(Label):
    
    def __init__(
        self,
        parent: Tk,  
        command: Optional[callable] = None,
        command_args: Optional[tuple] = None,
        is_toggle: bool = False,
        button_properties: Dict[str, Union[int, PhotoImage, None]] = {
            'pos_x': 0, 
            'pos_y': 0,
            'height': 10,
            'width': 10,
            'image_pressed': None, 
            'image_released': None,
            'image_released_toggle_true': None,
            'image_pressed_toggle_true': None
        },
        menu: Optional[Menu] = None
    ) -> None:
        self.parent = parent
        self.height = button_properties['height']
        self.width = button_properties['width']
        self.command = command
        self.is_toggle = is_toggle
        self.toggle = False
        self.command_args = command_args
        self.menu = menu
        self.set_images(button_properties)
        
        super().__init__(
            master=parent,
            image=self.image_released,
            relief='sunken',
            height=self.height,
            width=self.width,
            bd=0,
            anchor="nw"
        )
        self.place(x=button_properties['pos_x'], y=button_properties['pos_y'])
        self.bind('<Button>', func=lambda event :self.button_pressed(event))
        self.bind('<ButtonRelease>', func=lambda event :self.button_released(event))
        # print(self.keys())
    
    def set_images(self, button_images):
        self.image_pressed = button_images['image_pressed']
        self.image_released = button_images['image_released']
        self.image_released_toggle_true = button_images['image_released_toggle_true']
        self.image_pressed_toggle_true = button_images['image_pressed_toggle_true']
    
    def refresh(self, button_images):
        self.set_images(button_images)
        self['image'] = self.image_released
    
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
        
        if self.command:
            if self.command_args:
                self.command(*self.command_args)
            else:
                self.command()
        elif self.menu:
            # try:
            #     self.menu.tk_popup(self.parent.winfo_x() + event.x, self.parent.winfo_y() + event.y, 1)
            # finally:
            #     self.menu.grab_release()
            self.menu.post(self.parent.winfo_x() + event.x, self.parent.winfo_y() + event.y)
        
        