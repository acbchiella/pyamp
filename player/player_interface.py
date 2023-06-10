class MusicPlayer:
    def __init__(self, spectrum=None):
        self.playlist = []
        self.current_song = None
        self.playing = False
        self.spectrum = spectrum

    def _add_song(self, song):
        self.playlist.append(song)
    
    def _open(self):
        print("Open.")

    def _remove_song(self, song):
        self.playlist.remove(song)

    def _play(self):
        if not self.playlist:
            print("No songs in playlist.")
            return
        if not self.current_song:
            self.current_song = self.playlist[0]
        print(f"Now playing: {self.current_song}")
        self.playing = True

    def _pause(self):
        if not self.playing:
            print("Player is not currently playing.")
            return
        print("Player paused.")
        self.playing = False
    
    def _stop(self):
        if not self.playing:
            print("Player is not currently playing.")
            return
        print("Player stoped.")
        self.playing = False

    def _next(self):
        if not self.playlist:
            print("No songs in playlist.")
            return
        if not self.current_song:
            self.current_song = self.playlist[0]
        else:
            current_index = self.playlist.index(self.current_song)
            if current_index == len(self.playlist) - 1:
                self.current_song = self.playlist[0]
            else:
                self.current_song = self.playlist[current_index + 1]
        print(f"Now playing: {self.current_song}")

    def _previous(self):
        if not self.playlist:
            print("No songs in playlist.")
            return
        if not self.current_song:
            self.current_song = self.playlist[0]
        else:
            current_index = self.playlist.index(self.current_song)
            if current_index == 0:
                self.current_song = self.playlist[-1]
            else:
                self.current_song = self.playlist[current_index - 1]
        print(f"Now playing: {self.current_song}")