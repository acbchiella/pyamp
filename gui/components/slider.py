from tkinter import Tk, Label
from PIL.ImageTk import PhotoImage
from tkinter.messagebox import showinfo
from typing import Optional, List, Dict, Union

class WSlider(Label):
    
    def __init__(
        self,
        parent: Tk,
        command: Optional[callable] = None,
        command_args: Optional[tuple] = None,
        slider_properties: Dict[str, Union[int, PhotoImage, List[PhotoImage], None]] = {
            'pos_x': 0, 
            'pos_y': 0,
            'b_height': 10,
            'b_width': 10,
            's_height': 10,
            's_width': 100,
            'image_pressed': None, 
            'image_released': None,
            'image_bg': None
        }
    ) -> None:
        
        self.b_height = slider_properties['b_height']
        self.b_width = slider_properties['b_width']
        self.s_height = slider_properties['s_height']
        self.s_width = slider_properties['s_width']
        self.pos_x = slider_properties['pos_x']
        self.pos_y = slider_properties['pos_y']
        self.command = command
        self.move = False
        self.value = 0
        self.slider_x = slider_properties['pos_x']
        self.command_args = command_args
        self.set_images(slider_properties)
        
        self.bg = Label(
            master=parent,
            image=self.image_bg[0],
            relief='sunken',
            height=self.s_height,
            width=self.s_width,
            bd=0
        )
        self.bg.place(x=slider_properties['pos_x'], y=slider_properties['pos_y'])
        super().__init__(
            master=parent,
            image=self.image_released,
            relief='sunken',
            height=self.b_height,
            width=self.b_width,
            bd=0,
            anchor="nw"
        )
        self.place(x=slider_properties['pos_x'], y=slider_properties['pos_y'])
        self.bind('<Button>', func=lambda event :self.button_pressed(event))
        self.bind('<ButtonRelease>', func=lambda event :self.button_released(event))
        self.bind('<B1-Motion>', func=lambda event :self.button_move(event))
        
        self.bg.bind('<Button>', func=lambda event :self.bg_pressed(event))
        self.bg.bind('<ButtonRelease>', func=lambda event :self.bg_released(event))
        
        
        # print(self.keys())
    
    def set_images(self, slider_images):
        self.image_pressed = slider_images['image_pressed']
        self.image_released = slider_images['image_released']
        self.image_bg = slider_images['image_bg']
        
    def refresh(self, slider_images):
        self.set_images(slider_images)
        self['image'] = self.image_released
        self.bg['image'] = self.image_bg[0]
    
    def button_move(self, event):
        if self.move:
            self.slider_x += event.x - self.b_width / 2
            if self.slider_x > self.pos_x + self.s_width - self.b_width:
                self.slider_x = self.pos_x + self.s_width - self.b_width
            if self.slider_x < self.pos_x:
                self.slider_x = self.pos_x
            self.place(x=self.slider_x)
            self.value = (self.slider_x - self.pos_x)/(self.s_width- self.b_width)
            self.bg['image'] = self.image_bg[int(self.value*(len(self.image_bg)-1))]
            print(self.value, )
    
    def button_pressed(self, event):
        self.move = True
        self['image'] = self.image_pressed
   

    def button_released(self, event):
        self.move = False
        self['image'] = self.image_released
        
        if self.command_args:
            self.command(*self.command_args)
        else:
            self.command()
    
    def bg_pressed(self, event):
        # self.slider_x += event.x - self.b_width / 2
        # if self.slider_x > self.pos_x + self.s_width - self.b_width:
        #     self.slider_x = self.pos_x + self.s_width - self.b_width
        # if self.slider_x < self.pos_x:
        #     self.slider_x = self.pos_x
        # self.place(x=self.slider_x)
        # self.value = (self.slider_x - self.pos_x)/(self.s_width- self.b_width)
        # self.bg['image'] = self.image_bg[int(self.value*(len(self.image_bg)-1))]
        # print(self.value, )
        pass
    
    def bg_released(self, event):
        self.move = False
        pass
        
        