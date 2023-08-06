import os
import urllib.request
# import pyaudio
from player.player_interface import MusicPlayer
from tkinter import filedialog as fd
from pydub import AudioSegment
import threading
from math import log, ceil
from scipy import fft
import numpy as np
import time

class MusicPlayer(MusicPlayer):
    pass
    # def __init__(self, spectrum=None):
    #     self.player = pyaudio.PyAudio()
    #     self.CHUNK = 1024
    #     self.audio = None
    #     self.spectrum = spectrum
    #     self.playlist = []
    #     self.current_song = None
    #     self.playing = False
    #     self.pause = False
    #     self.stop = False
    #     self.data = [0 for i in range(19)]
        
    #     self.stream = None
        
        
    
    # def async_player(self):
    #     self.stream.start_stream()
    #     # PLAYBACK LOOP
    #     start = 0
    #     length = self.audio.duration_seconds
    #     volume = 100.0
    #     playchunk = self.audio[start*1000.0:(start+length)*1000.0] - (60 - (60 * (volume/100.0)))
    #     # millisecondchunk = 50 / 1000.0
    #     millisecondchunk = 10 / 1000.0
    #     self.time = 0
    #     for chunks in self.make_chunks(playchunk, millisecondchunk*1000):
    #         self.time += millisecondchunk
    #         self.stream.write(chunks._data)
    #         while self.pause:
    #             time.sleep(0.5)
    #             pass
    #         try:
    #             data = np.frombuffer(chunks._data, dtype=np.int16)
    #             fft_data = fft(data)
    #             fft_mag = np.abs(fft_data[range(20, 19*1 + 20, 1)])
    #             if np.max(fft_mag) > 0:
    #                 fft_mag /= np.max(fft_mag)
    #                 self.spectrum.values = list((fft_mag*16).astype(int))
    #                 # time.sleep(0.01)
    #         except:
    #             print('error')
    #             pass
    #         if self.stop:
    #             break
        
    #     self.stop = False
    
    # def make_chunks(self, audio_segment, chunk_length):
    #     """
    #     Breaks an AudioSegment into chunks that are <chunk_length> milliseconds
    #     long.
    #     if chunk_length is 50 then you'll get a list of 50 millisecond long audio
    #     segments back (except the last one, which can be shorter)
    #     """
    #     number_of_chunks = ceil(len(audio_segment) / float(chunk_length))
    #     return [audio_segment[i * chunk_length:(i + 1) * chunk_length]
    #             for i in range(int(number_of_chunks))]
    
    # def _open(self):
    #     # file type
    #     filetypes = (
    #         ('mp3', '*.mp3'),
    #         ('All files', '*.*')
    #     )
    #     self.current_song = fd.askopenfilename(initialdir = "./",
    #                                       title = "Select a music File",
    #                                       filetypes = filetypes)
        
    #     self._play()
    
    # def _load(self):
    #     if self.stream:
    #         self._stop()
        
    #     self.audio = AudioSegment.from_file(self.current_song)
    #     self.stream = self.player.open(format=self.player.get_format_from_width(self.audio.sample_width),
    #             channels=self.audio.channels,
    #             rate=self.audio.frame_rate,
    #             output=True)
        

    # def _add_song(self, song):
    #     self.playlist.append(song)

    # def _remove_song(self, song):
    #     self.playlist.remove(song)

    # def _play(self):
        
    #     if not self.pause:
    #         self._load()
    #         self.stop = False
    #         self.player_async = threading.Thread(daemon=True, target=self.async_player)
    #         self.player_async.start()
    #         self.playing = True
            
    #     if self.pause:
    #         self.pause = False        
    #     # if self.current_song.startswith("http"):
    #     #     try:
    #     #         urllib.request.urlretrieve(self.current_song, "temp.mp3")
    #     #         self.current_song = "temp.mp3"
    #     #     except:
    #     #         print("Error: Could not retrieve URL.")
    #     #         return
    #     # if not os.path.exists(self.current_song):
    #     #     print("Error: File not found.")
    #     #     return
    #     # pygame.mixer.music.load(self.current_song)
    #     # pygame.mixer.music.play()
    #     # self.playing = True

    # def _pause(self):
    #     self.pause = True

    # def _next_song(self):
    #     pass

    # def _previous_song(self):
    #     pass

    # def _stop(self):
    #     self.stream.stop_stream()
    #     self.stop = True
    #     # self.stream.close()
    
    # # Define callback function for audio stream
    # def _callback(self, in_data, frame_count, time_info, status):
    #     data = self.audio.raw_data[:frame_count]
    #     self.audio = self.audio._spawn(self.audio.raw_data[frame_count:])
    #     return (data, pyaudio.paContinue)