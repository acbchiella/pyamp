import tkinter as tk
from PIL import ImageTk, Image
import glob
from gui.components.button import WButton
from gui.components.slider import WSlider
from gui.components.spectrum import Spectrum
from player.player_interface import MusicPlayer
from tkinter import filedialog as fd
from typing import Optional

class MainApp(tk.Tk):
    def __init__(
        self,
        skin_path: str = './skins/classic/',
        player: MusicPlayer = MusicPlayer,
        change_skin: Optional[callable] = None,
     ):
        super().__init__()
        self.wm_attributes('-type', 'splash')
        # self.withdraw()
        # self.overrideredirect(True)
        self.player = player
        self.play_list_window = tk.Toplevel(self)
        # self.play_list_window.overrideredirect(True)
        self.play_list_window.wm_attributes('-type', 'splash')
        self.play_list_window.geometry('275x116+675+300')
        self.play_list_window.bind("<B1-Motion>", self.do_move_pl)
        self.play_list_window.bind("<ButtonPress-1>", self.start_move_pl)
        self.play_list_window.bind("<ButtonRelease-1>", self.stop_move_pl)
        self.play_list_hide = False
        
        self.atach_playlist = False
        
        self.Skinself = skin_path
        
        self.change_skin = change_skin
        
        self.window_components = {}
        
        self.load_skin_files()
        self.build_main_window()
    
    def build_main_window(self):
        
        self.w = tk.Canvas(self, width=275, height=116,highlightthickness=0)
        self.bg = self.w.create_image(0,0,image=self.images['bg'],anchor="nw")
        self.titlebar = self.w.create_image(0,0,image=self.images['titlebar'],disabledimage=self.getImage("TITLEBAR","disabled_titlebar",27,16,303,29),anchor="nw")
        self.w.pack()
        self.w.bind("<ButtonPress-1>", self.start_move)
        self.w.bind("<ButtonRelease-1>", self.stop_move)
        self.w.bind("<B1-Motion>", self.do_move)
        
        colors = self.get_spectrum_colors()
        coord = 24, 42, 102, 59
        self.spectrum = Spectrum(self.w, coord, colors=colors)
        self.player = self.player(spectrum=self.spectrum )
        
        # window buttons
        self.window_components['close_b'] = WButton(self, self.images['close_pressed'], self.images['close_released'], 264, 3, 8, 8, self.on_close)
        self.window_components['minimize_b'] = WButton(self, self.images['minimize_pressed'], self.images['minimize_released'], 254, 3, 8, 8, lambda : print('teste'))
        self.window_components['reduce_b'] = WButton(self, self.images['reduce_pressed'], self.images['reduce_released'], 244, 3, 8, 8, lambda : print('teste'))
        self.window_components['menu_b'] = WButton(self, self.images['menu_pressed'], self.images['menu_released'], 6, 3, 8, 8, lambda : print('teste'))
        self.window_components['eq_'] = WButton(self, self.images['eq_off_released'], self.images['eq_off_pressed'], 219, 58, 10, 21, lambda : print('teste'), True, self.images['eq_on_released'], self.images['eq_on_pressed'])
        self.window_components['pl_'] = WButton(self, self.images['pl_off_released'], self.images['pl_off_pressed'], 241, 58, 10, 21, self._hide_or_show_play_list, True, self.images['pl_on_released'], self.images['pl_on_pressed'])
        
        # player buttons
        self.prev = WButton(self, self.images['prev_released'], self.images['prev_pushed'], 16, 88, 18, 23, self.player._previous)
        self.play = WButton(self, self.images['play_released'], self.images['play_pushed'], 39, 88, 18, 23, self.player._play)
        self.pause = WButton(self, self.images['pause_released'], self.images['pause_pushed'], 62, 88, 18, 23, self.player._pause)
        self.stop = WButton(self, self.images['stop_released'], self.images['stop_pushed'], 85, 88, 18, 23, self.player._stop)
        self.next_ = WButton(self, self.images['next_released'], self.images['next_pushed'], 108, 88, 18, 22, self.player._next)
        self.open_ = WButton(self, self.images['open_released'], self.images['open_pushed'], 135, 89, 15, 21, self.player._open)
        self.repeat_ = WButton(self, self.images['repeat_off_released'], self.images['repeat_off_pressed'], 210, 89, 15, 27, lambda : print('teste'), True, self.images['repeat_on_released'], self.images['repeat_on_pressed'])
        self.sufle_ = WButton(self, self.images['shufle_off_released'], self.images['shufle_off_pressed'], 165, 89, 15, 45, lambda : print('teste'), True, self.images['shufle_on_released'], self.images['shufle_on_pressed'])
        
        self.pos_bar = WSlider(self, self.images['elapsed'], self.images['elapsed_pushed'], [self.images['elapsed_bg1']], 15, 72, 10, 29, 10, 248, lambda : print('teste'))
        self.vol_bar = WSlider(self, self.images['volume_released'], self.images['volume_pressed'], [self.images[f'volume_bg{i}'] for i in range(27)], 108, 58, 10, 14, 13, 67, lambda : print('teste'))
        self.balance_bar = WSlider(self, self.images['balance_released'], self.images['balance_pressed'], [self.images[f'balance_bg{i}'] for i in range(27)], 178, 58, 10, 13, 13, 37, lambda : print('teste'))
             
    def on_close(self):
        self.destroy()
    
    def get_spectrum_colors(self):
        a = self.txt_file['VISCOLOR'].read()
        a = [i.split('//')[0].split(',')[0:3] for i in a.split('\n')]

        colors_rgb = []
        for i in a[2:18]:
            c = tuple([int(j) for j in i])
            colors_rgb.append(self._from_rgb(c))
        
        return colors_rgb
    
    def _from_rgb(cls, rgb):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % rgb
    
    def async_spectrum(self):
        while True:
            self.spectrum.values = self.player.data
           
    def getImage(self, name,rename,cx,cy,cw,ch):
        if not rename in self.images: 
            self.images[rename] = ImageTk.PhotoImage(self.imgFile[name].crop((cx,cy,cw,ch)))
        return self.images[rename]

    def load_skin_files(self):
        self.txt_file = {
            file.split('/')[-1][:-4].upper(): open(file) for file in glob.glob(f"{self.Skinself}/*") 
            if file[-3:].upper() in ['TXT']
        }
        
        self.images = {}
        self.imgFile = {
            image.split('/')[-1][:-4].upper(): Image.open(image) for image in glob.glob(f"{self.Skinself}/*") 
            if image[-3:].upper() in ['PNG', 'BMP']
        }
        self.getImage("MAIN","bg",0,0,275,116)
        self.getImage("TITLEBAR","titlebar",27,0,303,14)
        
        self.getImage("CBUTTONS","prev_released",0,0,23,18)
        self.getImage("CBUTTONS","prev_pushed",0,18,23,36)

        self.getImage("CBUTTONS","play_released",23,0,46,18)
        self.getImage("CBUTTONS","play_pushed",23,18,46,36)

        self.getImage("CBUTTONS","pause_released",46,0,69,18)
        self.getImage("CBUTTONS","pause_pushed",46,18,69,36)

        self.getImage("CBUTTONS","stop_released",69,0,92,18)
        self.getImage("CBUTTONS","stop_pushed",69,18,92,36)

        self.getImage("CBUTTONS","next_released",92,0,114,18)
        self.getImage("CBUTTONS","next_pushed",92,18,114,36)

        self.getImage("CBUTTONS","open_released",114,0,135,15)
        self.getImage("CBUTTONS","open_pushed",114,16,135,31)


        self.getImage("POSBAR","elapsed",248,0,277,10)
        self.getImage("POSBAR","elapsed_pushed",278,0,307,10)
        self.getImage("POSBAR","elapsed_bg1",0,0,248,10)

        self.getImage("VOLUME","volume_released",15, 422,82,432)
        self.getImage("VOLUME","volume_pressed",0, 422,52,432)
        for i in range(28):
            if i == 0:
                self.getImage("VOLUME",f"volume_bg{i}",0,i*10,67,432)
            else:
                self.getImage("VOLUME",f"volume_bg{i}",0,i*15,67,i*15 + 13)


        self.getImage("BALANCE","balance_released",15, 422,28,432)
        self.getImage("BALANCE","balance_pressed",0, 422,13,432)
        for i in range(28):
            if i == 0:
                self.getImage("BALANCE",f"balance_bg{i}",9,i*10,46,432)
            else:
                self.getImage("BALANCE",f"balance_bg{i}",9,i*15,46,i*15 + 13)


        self.getImage("SHUFREP","repeat_on_released",0,30,27,45)
        self.getImage("SHUFREP","repeat_off_released",0,0,27,15)
        self.getImage("SHUFREP","repeat_on_pressed",0,15,27,30)
        self.getImage("SHUFREP","repeat_off_pressed",0,45,27,60)

        self.getImage("SHUFREP","shufle_on_released",29,30,74,45)
        self.getImage("SHUFREP","shufle_off_released",29,0,74,15)
        self.getImage("SHUFREP","shufle_on_pressed",29,15,74,30)
        self.getImage("SHUFREP","shufle_off_pressed",29,45,74,60)

        self.getImage("SHUFREP","eq_on_released",0,73,21,83)
        self.getImage("SHUFREP","eq_off_released",0,61,21,72)
        self.getImage("SHUFREP","eq_on_pressed",46,73,67,84)
        self.getImage("SHUFREP","eq_off_pressed",46,62,67,72)

        self.getImage("SHUFREP","pl_on_released",23,73,44,83)
        self.getImage("SHUFREP","pl_off_released",23,61,44,72)
        self.getImage("SHUFREP","pl_on_pressed",68,73,90,84)
        self.getImage("SHUFREP","pl_off_pressed",68,62,90,72)

        self.getImage("TITLEBAR","close_released",18,9,26,17)
        self.getImage("TITLEBAR","close_pressed",18,0,26,8)

        self.getImage("TITLEBAR","minimize_released",9,18,17,26)
        self.getImage("TITLEBAR","minimize_pressed",0,18,8,26)

        self.getImage("TITLEBAR","reduce_released",9,9,17,17)
        self.getImage("TITLEBAR","reduce_pressed",9,0,17,8)

        self.getImage("TITLEBAR","menu_released",0,9,8,17)
        self.getImage("TITLEBAR","menu_pressed",0,0,8,8)
        
        # playlist
        
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")
        
        if not self.atach_playlist:
            self.distx = self.play_list_window.winfo_x() - self.winfo_x()
            self.disty = self.play_list_window.winfo_y() - self.winfo_y()
        
        if  self.distx - 275 < 10 and self.distx - 275 >= 0 and abs(self.disty)-116 < 10:
            self.play_list_window.geometry(f"+{x+275}+{y+self.disty}")
            self.atach_playlist = True
        
        if  self.disty - 116 < 10 and self.disty - 116 >= 0 and abs(self.distx)-275 < 10:
            self.play_list_window.geometry(f"+{x+self.distx}+{y+116}")
            self.atach_playlist = True
            
        if  self.distx + 275 > -10 and self.distx + 275 <= 0 and abs(self.disty)-116 < 10:
            self.play_list_window.geometry(f"+{x-275}+{y+self.disty}")
            self.atach_playlist = True
            
        if  self.disty + 116 > -10 and self.disty + 116 <= 0 and abs(self.distx)-275 < 10:
            self.play_list_window.geometry(f"+{x+self.distx}+{y-116}")
            self.atach_playlist = True
    
    def do_move_pl(self, event):
        deltax = event.x - self.x_pl
        deltay = event.y - self.y_pl
        x = self.play_list_window.winfo_x() + deltax
        y = self.play_list_window.winfo_y() + deltay
        self.play_list_window.geometry(f"+{x}+{y}")
        
        distx = self.play_list_window.winfo_x() -  self.winfo_x()
        disty = self.play_list_window.winfo_y() - self.winfo_y()
        if abs(distx) > 10 or abs(disty)>10:
            self.atach_playlist = False
        
    def start_move_pl(self, event):
        self.x_pl = event.x
        self.y_pl = event.y

    def stop_move_pl(self, event):
        self.x_pl = None
        self.y_pl = None
    
    def _hide_or_show_play_list(self):
        if not self.play_list_hide:
            self.play_list_hide = True
            self.play_list_window.withdraw()
        else:
            self.play_list_hide = False
            self.play_list_window.deiconify()
        