from tkinter import Canvas
from typing import Optional, Tuple, List
import threading
import time

class Spectrum():
    
    def __init__(
        self, 
        canvas: Canvas,
        coord: Tuple[int],
        values: Optional[List[int]] = None,
        colors: Optional[List[str]] = None
        ) -> None:
        
        self.coord = coord
        self.canvas = canvas
        self.bars = {}
        self.colors = colors
        self.values = values if values else [16 for i in range(0, 19)]
        self.create_bars()
        
        self.spectrum = threading.Thread(daemon=True, target=self.update_bars_async)
        self.spectrum.start()
        
        self.spectrum_top = threading.Thread(daemon=True, target=self.update_top_bars_async)
        self.spectrum_top.start()
        
        return

    def __del__(self):
        self.spectrum_top.stop()
        self.spectrum.stop()

    def create_bars(self):
        for i in range(0, 19):
            x0 = self.coord[0] + i * 4
            y1 = self.coord[3]
            self.bars[f'bar_{i}'] = Bar(canvas=self.canvas, coord=(x0, y1), colors=self.colors)
        for i in range(0, 19):
            x0 = self.coord[0] + i * 4
            y0 = self.coord[3] - self.values[i]
            x1 = x0 + 3
            y1 = y0 + 0
            color = self.colors[-1] if self.colors else 'white'
            self.bars[f'top_bar_{i}'] = self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)
    
    def refresh(self, colors):
        self.colors = colors
        for i in range(0, 19):
            color = self.colors[-1] if self.colors else 'white'
            self.canvas.itemconfig(self.bars[f'top_bar_{i}'], fill=color)
            self.bars[f'bar_{i}'].refresh(self.colors)
            
    def update_bars_async(self):
        prior_values = self.values
        while True:
            for i in range(0, 19):
                if self.values[i] >= prior_values[i]:
                    self.bars[f'bar_{i}'].set_value(self.values[i])
                    self.bars[f'bar_{i}'].update_bar()
                    prior_values[i] = self.values[i]
                elif self.values[i] < prior_values[i]:
                    prior_values[i] -= 1
                    self.bars[f'bar_{i}'].set_value(int(prior_values[i]))
                    self.bars[f'bar_{i}'].update_bar()
                    
                y0 = self.bars[f'bar_{i}'].get_y() + 1
                tx0, ty0, tx1, ty1 = self.canvas.coords(self.bars[f'top_bar_{i}'])
                if y0 <= ty0:
                    ty0 = self.coord[3] - self.values[i]
                    ty1 = ty0 + 1
                    self.canvas.coords(self.bars[f'top_bar_{i}'], tx0, ty0, tx1, ty1) 
            time.sleep(0.00001)     
    
    def update_top_bars_async(self):
        while True:
            for i in range(0, 19):
                y0 = self.bars[f'bar_{i}'].get_y() - 1
                tx0, ty0, tx1, ty1 = self.canvas.coords(self.bars[f'top_bar_{i}'])
                if y0 >= ty0:
                    ty0 = ty0 + 1
                    ty1 = ty0 + 1
                    self.canvas.coords(self.bars[f'top_bar_{i}'], tx0, ty0, tx1, ty1)

            time.sleep(0.1)
 
 
class Bar():
     
    def __init__(
        self, 
        canvas: Canvas,
        coord: Tuple[int],
        value: int = None,
        colors: Optional[List[str]] = None
        ) -> None:
        
        self.value = value
        self.coord = coord
        self.canvas = canvas
        self.blocks = {}
        self.colors = colors
        
        self.max_blocks = 16
        self.create_bar()
    
    def create_bar(self):
        for i in range(1, self.max_blocks):
            x0 = self.coord[0]
            y0 = self.coord[1] - i
            x1 = x0 + 3
            y1 = y0 + 1
            color = self.colors[self.max_blocks-i] if self.colors else 'white'
            self.blocks[f'block_{i}'] = self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)
    
    def update_bar(self):
        for i in range(1, min(self.value, self.max_blocks)):
            self.canvas.itemconfigure(self.blocks[f'block_{i}'], state='normal')
        
        hide_blocks = self.max_blocks - min(self.value, self.max_blocks)
        if hide_blocks:
            for i in range(1, hide_blocks):
                self.canvas.itemconfigure(self.blocks[f'block_{self.max_blocks-i}'], state='hidden')
    
    def refresh(self, colors):
        self.colors = colors
        for i in range(1, self.max_blocks):
            color = self.colors[self.max_blocks-i] if self.colors else 'white'
            self.canvas.itemconfigure(self.blocks[f'block_{i}'], fill=color)
    
    def get_y(self):
        try:
            r = self.coord[1] - min(self.value, self.max_blocks)
        except:
            r = self.coord[1]
        return r
    
    def set_value(self, value):
        self.value = max(1, value)
    
    
    