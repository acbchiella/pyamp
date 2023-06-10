from tkinter import Tk, Label
from PIL.ImageTk import PhotoImage
from tkinter.messagebox import showinfo
from typing import Optional, List

class WSlider(Label):
    
    def __init__(
        self,
        parent: Tk, 
        image_released: PhotoImage, 
        image_pressed: PhotoImage, 
        image_bg: List[PhotoImage],
        pos_x: int, 
        pos_y: int,
        b_height: int,
        b_width: int,
        s_height: int,
        s_width: int,
        command: Optional[callable] = None
    ) -> None:
        self.image_pressed = image_pressed
        self.image_released = image_released
        self.b_height = b_height
        self.b_width = b_width
        self.s_height = s_height
        self.s_width = s_width
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.command = command
        self.move = False
        self.value = 0
        self.slider_x = pos_x
        self.image_bg = image_bg 
        self.bg = Label(
            master=parent,
            image=image_bg[0],
            relief='sunken',
            height=self.s_height,
            width=self.s_width,
            bd=0
        )
        self.bg.place(x=pos_x, y=pos_y)
        super().__init__(
            master=parent,
            image=self.image_released,
            relief='sunken',
            height=self.b_height,
            width=self.b_width,
            bd=0,
            anchor="nw"
        )
        self.place(x=pos_x, y=pos_y)
        self.bind('<Button>', func=lambda event :self.button_pressed(event))
        self.bind('<ButtonRelease>', func=lambda event :self.button_released(event))
        self.bind('<B1-Motion>', func=lambda event :self.button_move(event))
        
        self.bg.bind('<Button>', func=lambda event :self.bg_pressed(event))
        self.bg.bind('<ButtonRelease>', func=lambda event :self.bg_released(event))
        
        
        # print(self.keys())
    
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
        
        