from gui.app import MainApp
from player.player import MusicPlayer
    
app=MainApp(skin_path='./skins/classic/', player=MusicPlayer)
app.mainloop()