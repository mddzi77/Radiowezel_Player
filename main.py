import mutagen
import json
import PySimpleGUI as sg
import datetime as dt
import numpy as np
import pandas as pd
import gui as g
from os import listdir, mkdir, path
from pygame import mixer
from player_db import PlayerDatabase


class Player:
    """
    Module for playing created playlists
    """
    def __init__(self, playlist: list[str], music_dir: str):
        self.playlist = playlist
        self.music_dir = music_dir

        mixer.init()
        self.db = PlayerDatabase()
        self.counter = 0  # which song in the playlist is currently played
        self.loaded = False  # for checking if music file is currently loaded
        self.cur_song = self.playlist[self.counter]  # currently played song

        self.pos = None  # Current position of playback in seconds
        self.pos_playlist = None  # same as pos but relative to playlist

        # get lengths of songs in the playlist in seconds
        self.songs_lengths = []
        for song in playlist:
            self.songs_lengths.append(self.db.songs['duration'].loc[self.db.songs['title'] == song].values[0])
        self.playlist_length = np.sum(self.songs_lengths)

    def play(self):
        mixer.music.set_volume(0.8)
        if not self.loaded:
            mixer.music.load(path.join(self.music_dir, self.playlist[self.counter]))
            mixer.music.play()
            self.loaded = True
        else:
            mixer.music.unpause()

    @staticmethod
    def pause():
        mixer.music.pause()

    def music_clock(self):
        """
        Calculate elpased and left time of the currently played song and playlist,
        and start playing next song if current ended
        :return: Formatted song and playlist elapsed and left time
        """
        self.pos = mixer.music.get_pos() / 1000  # get current position in seconds

        # block position getting out of song length
        if self.songs_lengths[self.counter] < self.pos:
            self.pos = self.songs_lengths[self.counter]

        # get song elapsed and left time
        # change position to minutes and second format
        pos_M = int(self.pos / 60)
        pos_S = int(self.pos - pos_M * 60)
        s_elapsed = dt.time(minute=pos_M, second=pos_S)  # change position to time object
        # calculate time left
        s_left = self.songs_lengths[self.counter] - self.pos
        left_M = int(s_left / 60)
        left_S = int(s_left - left_M * 60)
        s_left = dt.time(minute=left_M, second=left_S)

        # get playlist elapsed and left time
        # sum up the previous lengths of songs for elapsed time
        p_elapsed = 0
        for i in range(0, self.counter):
            p_elapsed += self.songs_lengths[i]
        p_elapsed += self.pos
        self.pos_playlist = p_elapsed
        p_left = self.playlist_length - p_elapsed
        # change values from seconds in int to time
        pos_M = int(p_elapsed / 60)
        pos_S = int(p_elapsed - pos_M * 60)
        left_M = int(p_left / 60)
        left_S = int(p_left - left_M * 60)
        p_elapsed = dt.time(minute=pos_M, second=pos_S)
        p_left = dt.time(minute=left_M, second=left_S)

        # start playing new song if current song ended and if there is still songs to play
        if s_left.minute == 0 and s_left.second == 0 and len(self.playlist) != self.counter + 1:
            self.loaded = False
            self.counter += 1
            self.play()
        # if song ended anf it's the last song in playlist then end player
        elif s_left.minute == 0 and s_left.second == 0 and len(self.playlist) == self.counter + 1:
            print('playlist ended')
            # reset values
            mixer.music.unload()
            self.counter = 0
            self.loaded = False
            mixer.quit()

        return (s_elapsed, s_left), (p_elapsed, p_left)


class App(object):

    def __init__(self):
        with open('settings.json', encoding='UTF-8') as f:
            self.settings = json.load(f)

        PlayerDatabase().refresh_()

        self.window1 = None
        self.window2 = None

        self.player = None
        self.playing = False

    def run(self):
        """
        App main loop
        """

        self.window1 = g.main_window()
        counter = 0

        while True:
            window, event, values = sg.read_all_windows(timeout=100, timeout_key='_clock_') # # #

            print(window, event, values)   # # # debugging # # #

            # closing window
            if event == sg.WIN_CLOSED or event == '_cancel_':
                window.close()
                if window == self.window2:
                    self.window2 = None
                    self.window1.enable()
                elif window == self.window1:
                    break
            # interacting with playback
            elif event == '_play_pause_':
                p = ['Myslovitz-D_ugo__ d_wi_ku samotno_ci.mp3', 'Najnowszy Klip.mp3', 'Myslovitz - Mie_ czy by_ tekst .mp3']
                self.player = Player(p, 'music')
                self.player.play()
                print('krok 3')

            # clock for counting time of the playlists and songs
            elif event == '_clock_':
                if self.player.loaded:
                    song_t, playlist_t = self.player.music_clock()

                    # update progressbars
                    self.window1['_song_progress_'](self.player.pos, self.player.songs_lengths[self.player.counter])
                    self.window1['_playlist_progress_'](self.player.pos_playlist, self.player.playlist_length)

                    # update texts
                    self.window1['_elapsed_s_'](song_t[0].strftime('%M:%S'))
                    self.window1['_left_s_'](song_t[1].strftime('%M:%S'))
                    self.window1['_elapsed_p_'](playlist_t[0].strftime('%M:%S'))
                    self.window1['_left_p_'](playlist_t[1].strftime('%M:%S'))


if __name__ == '__main__':
    App().run()
