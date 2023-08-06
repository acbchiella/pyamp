import tkinter as tk
from PIL import ImageTk, Image
import glob
from gui.components.button import WButton
from gui.components.slider import WSlider
from gui.components.spectrum import Spectrum
from player.player_interface import MusicPlayer
from tkinter import filedialog as fd
from typing import Optional

SKINS_DIR = './skins/*'

class MainApp(tk.Tk):
    def __init__(
        self,
        skin_path: str = './skins/classic',
        player: MusicPlayer = MusicPlayer,
        change_skin: Optional[callable] = None,
     ):
        super().__init__()
        self.wm_attributes('-type', 'splash')
        # self.withdraw()
        # self.overrideredirect(True)
        self.player = player
        
        self.play_list_window = tk.Toplevel(self)
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
        
        self.get_skins()
        self.load_skin_files()
        self.build_main_window()
    
    def set_skin(self, skin):
        self.Skinself = skin
        self.refresh_skin()
        # print(self.skins)
        
    def build_main_window(self):
        
        self.w = tk.Canvas(self, width=275, height=116,highlightthickness=0)
        self.bg = self.w.create_image(0, 0, image=self.image_bg['image'],anchor="nw")
        self.titlebar = self.w.create_image(0, 0, image=self.image_title_bar['image'], disabledimage=self.image_title_bar['disabledimage'], anchor="nw")
        self.w.pack()
        self.w.bind("<ButtonPress-1>", self.start_move)
        self.w.bind("<ButtonRelease-1>", self.stop_move)
        self.w.bind("<B1-Motion>", self.do_move)
        
        self.spectrum = Spectrum(self.w, (24, 42, 102, 59), colors=self.spectrum_color)
        self.player = self.player(spectrum=self.spectrum )
        
        # window buttons
        self.close = WButton(self, button_properties=self.property_close, command=self.on_close)
        self.minimize = WButton(self, button_properties=self.property_minimize, command=lambda : print('teste'))
        self.reduce = WButton(self, button_properties=self.property_reduce, command=lambda : print('teste'))
        
        # Menu
        self.menu_items = tk.Menu(self, tearoff=0)
        def set_skin(skin):
            self.Skinself = skin
            self.refresh_skin()
        
        def command(skin):
            return lambda: set_skin(skin)
        
        for item in self.skins:
            self.menu_items.add_command(label=item, command=command(self.skins[item]))

        self.menu = WButton(self, button_properties=self.property_menu, menu=self.menu_items)
        
        # player buttons
        self.prev = WButton(self, button_properties=self.property_prev, command=self.player._previous)
        self.play = WButton(self, button_properties=self.property_play, command=self.player._play)
        self.pause = WButton(self, button_properties=self.property_pause, command=self.player._pause)
        self.stop = WButton(self, button_properties=self.property_stop, command=self.player._stop)
        self.next = WButton(self, button_properties=self.property_next, command=self.player._next)
        self.open = WButton(self, button_properties=self.property_open, command=self.player._open)
        
        self.repeat = WButton(self, button_properties=self.property_repeat, is_toggle=True, command=lambda : print('teste'))
        self.shufle = WButton(self, button_properties=self.property_shufle, is_toggle=True, command=lambda : print('teste'))
        
        self.eq = WButton(self, button_properties=self.property_eq, is_toggle=True, command=lambda : print('teste'))
        self.pl = WButton(self, button_properties=self.property_pl, is_toggle=True, command=self._hide_or_show_play_list)
        
        self.pos_bar = WSlider(self, slider_properties=self.property_pos_bar, command=lambda : print('teste'))
        self.vol_bar = WSlider(self, slider_properties=self.property_vol_bar, command=lambda : print('teste'))
        self.balance_bar = WSlider(self, slider_properties=self.property_balance_bar, command=lambda : print('teste'))
          
    def on_close(self):
        self.destroy()
    
    def get_spectrum_colors(self):
        a = self.txt_file['VISCOLOR'].read()
        a = [i.split('//')[0].split(',')[0:3] for i in a.split('\n')]
        rgb_to_tkinter = lambda x: "#%02x%02x%02x" % x
        colors_rgb = []
        for i in a[2:18]:
            c = tuple([int(j) for j in i])
            colors_rgb.append(rgb_to_tkinter(c))
        
        return colors_rgb
    
    def async_spectrum(self):
        while True:
            self.spectrum.values = self.player.data

    def load_skin_files(self):
        
        self.txt_file = {
            file.split('/')[-1][:-4].upper(): open(file) for file in glob.glob(f"{self.Skinself}/*") 
            if file[-3:].upper() in ['TXT']
        }
        
        self.imgFile = {
            image.split('/')[-1][:-4].upper(): Image.open(image) for image in glob.glob(f"{self.Skinself}/*") 
            if image[-3:].upper() in ['PNG', 'BMP']
        }
        
        self.spectrum_color = self.get_spectrum_colors()
        
        self.image_bg = {
            'image': ImageTk.PhotoImage(self.imgFile['MAIN'].crop((0, 0, 275, 116))),
            'disabledimage': None
        }
        self.image_title_bar = {
            'image': ImageTk.PhotoImage(self.imgFile['TITLEBAR'].crop((27, 0, 303, 14))),
            'disabledimage': ImageTk.PhotoImage(self.imgFile['TITLEBAR'].crop((27, 16, 303, 29)))
        }
        
        self.property_close = {
            'pos_x': 264, 
            'pos_y': 3,
            'height': 8,
            'width': 8,
            'image_released': ImageTk.PhotoImage(self.imgFile['TITLEBAR'].crop((18,0,26,8))), 
            'image_pressed': ImageTk.PhotoImage(self.imgFile['TITLEBAR'].crop((18,9,26,17))),
            'image_released_toggle_true': None,
            'image_pressed_toggle_true': None
        }
        
        self.property_minimize = {
            'pos_x': 254, 
            'pos_y': 3,
            'height': 8,
            'width': 8,
            'image_released': ImageTk.PhotoImage(self.imgFile['TITLEBAR'].crop((0,18,8,26))), 
            'image_pressed': ImageTk.PhotoImage(self.imgFile['TITLEBAR'].crop((9,18,17,26))),
            'image_released_toggle_true': None,
            'image_pressed_toggle_true': None
        }
        
        self.property_reduce = {
            'pos_x': 244, 
            'pos_y': 3,
            'height': 8,
            'width': 8,
            'image_released': ImageTk.PhotoImage(self.imgFile['TITLEBAR'].crop((9,0,17,8))), 
            'image_pressed': ImageTk.PhotoImage(self.imgFile['TITLEBAR'].crop((9,9,17,17))),
            'image_released_toggle_true': None,
            'image_pressed_toggle_true': None
        }
        
        self.property_menu = {
            'pos_x': 6, 
            'pos_y': 3,
            'height': 8,
            'width': 8,
            'image_released': ImageTk.PhotoImage(self.imgFile['TITLEBAR'].crop((0,0,8,8))), 
            'image_pressed': ImageTk.PhotoImage(self.imgFile['TITLEBAR'].crop((0,9,8,17))),
            'image_released_toggle_true': None,
            'image_pressed_toggle_true': None
        }

        self.property_prev = {
            'pos_x': 16, 
            'pos_y': 88,
            'height': 18,
            'width': 23,
            'image_pressed': ImageTk.PhotoImage(self.imgFile['CBUTTONS'].crop((0, 18, 23, 36))), 
            'image_released': ImageTk.PhotoImage(self.imgFile['CBUTTONS'].crop((0, 0, 23, 18))),
            'image_released_toggle_true': None,
            'image_pressed_toggle_true': None
        }
        
        self.property_play = {
            'pos_x': 39, 
            'pos_y': 88,
            'height': 18,
            'width': 23,
            'image_pressed': ImageTk.PhotoImage(self.imgFile['CBUTTONS'].crop((23, 18, 46, 36))), 
            'image_released': ImageTk.PhotoImage(self.imgFile['CBUTTONS'].crop((23, 0, 46, 18))),
            'image_released_toggle_true': None,
            'image_pressed_toggle_true': None
        }
        
        self.property_pause = {
            'pos_x': 62, 
            'pos_y': 88,
            'height': 18,
            'width': 23,
            'image_pressed': ImageTk.PhotoImage(self.imgFile['CBUTTONS'].crop((46,18,69,36))), 
            'image_released': ImageTk.PhotoImage(self.imgFile['CBUTTONS'].crop((46,0,69,18))),
            'image_released_toggle_true': None,
            'image_pressed_toggle_true': None
        }
        
        self.property_stop = {
            'pos_x': 85, 
            'pos_y': 88,
            'height': 18,
            'width': 23,
            'image_pressed': ImageTk.PhotoImage(self.imgFile['CBUTTONS'].crop((69,18,92,36))), 
            'image_released': ImageTk.PhotoImage(self.imgFile['CBUTTONS'].crop((69,0,92,18))),
            'image_released_toggle_true': None,
            'image_pressed_toggle_true': None
        }
        
        self.property_next = {
            'pos_x': 108, 
            'pos_y': 88,
            'height': 18,
            'width': 22,
            'image_pressed': ImageTk.PhotoImage(self.imgFile['CBUTTONS'].crop((92,18,114,36))), 
            'image_released': ImageTk.PhotoImage(self.imgFile['CBUTTONS'].crop((92,0,114,18))),
            'image_released_toggle_true': None,
            'image_pressed_toggle_true': None
        }
        
        self.property_open = {
            'pos_x': 135, 
            'pos_y': 89,
            'height': 15,
            'width': 21,
            'image_pressed': ImageTk.PhotoImage(self.imgFile['CBUTTONS'].crop((114,16,135,31))), 
            'image_released': ImageTk.PhotoImage(self.imgFile['CBUTTONS'].crop((114,0,135,15))),
            'image_released_toggle_true': None,
            'image_pressed_toggle_true': None
        }
        
        self.property_repeat = {
            'pos_x': 210, 
            'pos_y': 89,
            'height': 15,
            'width': 27,
            'image_pressed': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((0,45,27,60))), 
            'image_released': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((0,0,27,15))),
            'image_released_toggle_true': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((0,30,27,45))),
            'image_pressed_toggle_true': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((0,15,27,30)))
        }
        
        self.property_shufle = {
            'pos_x': 165, 
            'pos_y': 89,
            'height': 15,
            'width': 45,
            'image_pressed': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((29,45,74,60))), 
            'image_released': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((29,0,74,15))),
            'image_released_toggle_true': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((29,30,74,45))),
            'image_pressed_toggle_true': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((29,15,74,30)))
        }
        
        self.property_eq = {
            'pos_x': 219, 
            'pos_y': 58,
            'height': 10,
            'width': 21,
            'image_pressed': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((46,62,67,72))), 
            'image_released': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((0,61,21,72))),
            'image_released_toggle_true': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((0,73,21,83))),
            'image_pressed_toggle_true': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((46,73,67,84)))
        }

        self.property_pl = {
            'pos_x': 241, 
            'pos_y': 58,
            'height': 10,
            'width': 21,
            'image_pressed': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((68,62,90,72))), 
            'image_released': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((23,61,44,72))),
            'image_released_toggle_true': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((23,73,44,83))),
            'image_pressed_toggle_true': ImageTk.PhotoImage(self.imgFile['SHUFREP'].crop((68,73,90,84)))
        }

        self.property_pos_bar = {
            'pos_x': 15, 
            'pos_y': 72,
            'b_height': 10,
            'b_width': 29,
            's_height': 10,
            's_width': 248,
            'image_pressed': ImageTk.PhotoImage(self.imgFile['POSBAR'].crop((278,0,307,10))), 
            'image_released': ImageTk.PhotoImage(self.imgFile['POSBAR'].crop((248,0,277,10))),
            'image_bg': [ImageTk.PhotoImage(self.imgFile['POSBAR'].crop((0,0,248,10)))]
        }
        
        self.property_vol_bar = {
            'pos_x': 108, 
            'pos_y': 58,
            'b_height': 10,
            'b_width': 14,
            's_height': 13,
            's_width': 67,
            'image_pressed': ImageTk.PhotoImage(self.imgFile['VOLUME'].crop((0, 422,52,432))), 
            'image_released': ImageTk.PhotoImage(self.imgFile['VOLUME'].crop((15, 422,82,432))),
            'image_bg': [ImageTk.PhotoImage(self.imgFile['VOLUME'].crop((0,i*15,67,i*15 + 13))) for i in range(1, 28)]
        }
        
        self.property_balance_bar = {
            'pos_x': 178, 
            'pos_y': 58,
            'b_height': 10,
            'b_width': 13,
            's_height': 13,
            's_width': 37,
            'image_pressed': ImageTk.PhotoImage(self.imgFile['BALANCE'].crop((0, 422,13,432))), 
            'image_released': ImageTk.PhotoImage(self.imgFile['BALANCE'].crop((15, 422,28,432))),
            'image_bg': [ImageTk.PhotoImage(self.imgFile['BALANCE'].crop((9,i*15,46,i*15 + 13))) for i in range(1, 28)]
        }
        
    def get_skins(self):
        paths = glob.glob(SKINS_DIR)
        
        self.skins = {path.split('/')[-1]:path for path in paths}
        
    def refresh_skin(self):
        self.load_skin_files()
        
        self.w.itemconfig(self.bg,image=self.image_bg['image'])
        self.w.itemconfig(self.titlebar,image=self.image_title_bar['image'], disabledimage=self.image_title_bar['disabledimage'])
        self.close.refresh(self.property_close)
        self.minimize.refresh(self.property_minimize)
        self.reduce.refresh(self.property_reduce)
        self.menu.refresh(self.property_menu)
        
        self.spectrum.refresh(self.spectrum_color)
        
        self.prev.refresh(self.property_prev)
        self.play.refresh(self.property_play)
        self.pause.refresh(self.property_pause)
        self.next.refresh(self.property_next)
        self.stop.refresh(self.property_stop)
        self.open.refresh(self.property_open)
        self.repeat.refresh(self.property_repeat)
        self.shufle.refresh(self.property_shufle)
        self.eq.refresh(self.property_eq)
        self.pl.refresh(self.property_pl)
        
        self.pos_bar.refresh(self.property_pos_bar)
        self.vol_bar.refresh(self.property_vol_bar)
        self.balance_bar.refresh(self.property_balance_bar)
        
    def start_move(self, event):
        self.menu_items.unpost()
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
        