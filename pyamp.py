from gui.app import MainApp
# from player.player import MusicPlayer
import tkinter as tk



def change_skin(self, path):
    self.destroy()
    self.Skinself = './skins/modern/'
    self.__init__()
    
app=MainApp(skin_path='./skins/classic/')
app.mainloop()