from tkinter import Tk, Canvas
from PIL.ImageTk import PhotoImage
from PIL import ImageTk
from gui.components.button import WButton
from gui.components.slider import WSlider
from gui.components.spectrum import Spectrum
from gui.utils import from_rgb
from typing import Dict, Union, List

class MainWindow():
    def __init__(
        self,
        parent: Tk,
        skin_files: Dict[str, Union[List, PhotoImage]]
    ) -> None:
        self.parent = parent
        self.skin_files = skin_files
        self.images = {}
        self._load_skin_images()
        self._build_window()
    
    def _build_window(self):
        self.w = Canvas(self.parent, width=275, height=116,highlightthickness=0)
        self.bg = self.w.create_image(0,0,image=self.images['bg'])
        self.titlebar = self.w.create_image(0,0,image=self.images['titlebar'],disabledimage=self._getImage("TITLEBAR","disabled_titlebar",27,16,303,29))
        self.w.pack()
        # self.w.bind("<ButtonPress-1>", self.start_move)
        # self.w.bind("<ButtonRelease-1>", self.stop_move)
        # self.w.bind("<B1-Motion>", self.do_move)
        #buttons
        self.prev = WButton(self.parent, self.images['prev_released'], self.images['prev_pushed'], 16, 88, 18, 23, lambda : print('teste'))
        self.play = WButton(self.parent, self.images['play_released'], self.images['play_pushed'], 39, 88, 18, 23, lambda : print('teste'))
        self.pause = WButton(self.parent, self.images['pause_released'], self.images['pause_pushed'], 62, 88, 18, 23, lambda : print('teste'))
        self.stop = WButton(self.parent, self.images['stop_released'], self.images['stop_pushed'], 85, 88, 18, 23, lambda : print('teste'))
        self.next_ = WButton(self.parent, self.images['next_released'], self.images['next_pushed'], 108, 88, 18, 22, lambda : print('teste'))
        self.open_ = WButton(self.parent, self.images['open_released'], self.images['open_pushed'], 135, 89, 15, 21, lambda : print('teste'))
        self.repeat_ = WButton(self.parent, self.images['repeat_off_released'], self.images['repeat_off_pressed'], 210, 89, 15, 27, lambda : print('teste'), True, self.images['repeat_on_released'], self.images['repeat_on_pressed'])
        self.sufle_ = WButton(self.parent, self.images['shufle_off_released'], self.images['shufle_off_pressed'], 165, 89, 15, 45, lambda : print('teste'), True, self.images['shufle_on_released'], self.images['shufle_on_pressed'])
        self.eq_ = WButton(self.parent, self.images['eq_off_released'], self.images['eq_off_pressed'], 219, 58, 10, 21, lambda : print('teste'), True, self.images['eq_on_released'], self.images['eq_on_pressed'])
        self.pl_ = WButton(self.parent, self.images['pl_off_released'], self.images['pl_off_pressed'], 241, 58, 10, 21, lambda : print('teste'), True, self.images['pl_on_released'], self.images['pl_on_pressed'])
        self.pos_bar = WSlider(self.parent, self.images['elapsed'], self.images['elapsed_pushed'], [self.images['elapsed_bg1']], 15, 72, 10, 29, 10, 248, lambda : print('teste'))
        self.vol_bar = WSlider(self.parent, self.images['volume_released'], self.images['volume_pressed'], [self.images[f'volume_bg{i}'] for i in range(27)], 108, 58, 10, 14, 13, 67, None)
        self.balance_bar = WSlider(self.parent, self.images['balance_released'], self.images['balance_pressed'], [self.images[f'balance_bg{i}'] for i in range(27)], 178, 58, 10, 13, 13, 37, lambda : print('teste'))
        self.close_b = WButton(self.parent, self.images['close_pressed'], self.images['close_released'], 264, 3, 8, 8, self.parent.on_close)
        self.minimize_b = WButton(self.parent, self.images['minimize_pressed'], self.images['minimize_released'], 254, 3, 8, 8, lambda : print('teste'))
        self.reduce_b = WButton(self.parent, self.images['reduce_pressed'], self.images['reduce_released'], 244, 3, 8, 8, lambda : print('teste'))
        self.menu_b = WButton(self.parent, self.images['menu_pressed'], self.images['menu_released'], 6, 3, 8, 8, lambda : print('teste'))

        # colors = self._get_spectrum_colors()
        coord = 24, 42, 102, 59
        # self.spectrum = Spectrum(self.w, coord, colors=colors)
        
    def _get_spectrum_colors(self):
        a = self.skin_files['VISCOLOR'].read()
        a = [i.split('//')[0].split(',')[0:3] for i in a.split('\n')]

        colors_rgb = []
        for i in a[2:18]:
            c = tuple([int(j) for j in i])
            colors_rgb.append(from_rgb(c))
        
        return colors_rgb
    
    def _load_skin_images(self):
        
        self._getImage("MAIN","bg",0,0,275,116)
        self._getImage("TITLEBAR","titlebar",27,0,303,14)
        self._getImage("CBUTTONS","prev_released",0,0,23,18)
        self._getImage("CBUTTONS","prev_pushed",0,18,23,36)
        self._getImage("CBUTTONS","play_released",23,0,46,18)
        self._getImage("CBUTTONS","play_pushed",23,18,46,36)
        self._getImage("CBUTTONS","pause_released",46,0,69,18)
        self._getImage("CBUTTONS","pause_pushed",46,18,69,36)
        self._getImage("CBUTTONS","stop_released",69,0,92,18)
        self._getImage("CBUTTONS","stop_pushed",69,18,92,36)
        self._getImage("CBUTTONS","next_released",92,0,114,18)
        self._getImage("CBUTTONS","next_pushed",92,18,114,36)
        self._getImage("CBUTTONS","open_released",114,0,135,15)
        self._getImage("CBUTTONS","open_pushed",114,16,135,31)
        self._getImage("POSBAR","elapsed",248,0,277,10)
        self._getImage("POSBAR","elapsed_pushed",278,0,307,10)
        self._getImage("POSBAR","elapsed_bg1",0,0,248,10)
        self._getImage("VOLUME","volume_released",15, 422,82,432)
        self._getImage("VOLUME","volume_pressed",0, 422,52,432)
        for i in range(28):
            if i == 0:
                self._getImage("VOLUME",f"volume_bg{i}",0,i*10,67,432)
            else:
                self._getImage("VOLUME",f"volume_bg{i}",0,i*15,67,i*15 + 13)

        self._getImage("BALANCE","balance_released",15, 422,28,432)
        self._getImage("BALANCE","balance_pressed",0, 422,13,432)
        for i in range(28):
            if i == 0:
                self._getImage("BALANCE",f"balance_bg{i}",9,i*10,46,432)
            else:
                self._getImage("BALANCE",f"balance_bg{i}",9,i*15,46,i*15 + 13)

        self._getImage("SHUFREP","repeat_on_released",0,30,27,45)
        self._getImage("SHUFREP","repeat_off_released",0,0,27,15)
        self._getImage("SHUFREP","repeat_on_pressed",0,15,27,30)
        self._getImage("SHUFREP","repeat_off_pressed",0,45,27,60)
        self._getImage("SHUFREP","shufle_on_released",29,30,74,45)
        self._getImage("SHUFREP","shufle_off_released",29,0,74,15)
        self._getImage("SHUFREP","shufle_on_pressed",29,15,74,30)
        self._getImage("SHUFREP","shufle_off_pressed",29,45,74,60)
        self._getImage("SHUFREP","eq_on_released",0,73,21,83)
        self._getImage("SHUFREP","eq_off_released",0,61,21,72)
        self._getImage("SHUFREP","eq_on_pressed",46,73,67,84)
        self._getImage("SHUFREP","eq_off_pressed",46,62,67,72)
        self._getImage("SHUFREP","pl_on_released",23,73,44,83)
        self._getImage("SHUFREP","pl_off_released",23,61,44,72)
        self._getImage("SHUFREP","pl_on_pressed",68,73,90,84)
        self._getImage("SHUFREP","pl_off_pressed",68,62,90,72)
        self._getImage("TITLEBAR","close_released",18,9,26,17)
        self._getImage("TITLEBAR","close_pressed",18,0,26,8)
        self._getImage("TITLEBAR","minimize_released",9,18,17,26)
        self._getImage("TITLEBAR","minimize_pressed",0,18,8,26)
        self._getImage("TITLEBAR","reduce_released",9,9,17,17)
        self._getImage("TITLEBAR","reduce_pressed",9,0,17,8)
        self._getImage("TITLEBAR","menu_released",0,9,8,17)
        self._getImage("TITLEBAR","menu_pressed",0,0,8,8)
    
    def _getImage(self, name,rename,cx,cy,cw,ch):
        if not rename in self.images: 
            self.images[rename] = ImageTk.PhotoImage(self.skin_files[name].crop((cx,cy,cw,ch)))
        return self.images[rename]
