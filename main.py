import mutagen
import json
import PySimpleGUI as sg
import pandas as pd
import os.path as path
import datetime as dt
import numpy as np
import pandas as pd
from gui import Gui
from os import listdir, mkdir
from pygame import mixer


class PlayerDatabase(object):
    def __init__(self, ):
        self.music_folder_dir = None

        # initialize pandas dataframes
        try:
            self.songs = pd.DataFrame(
                self.load_data('songs.db', 'sisb'),
                columns=['title', 'duration', 'category', 'used']
            )
        except FileNotFoundError:
            self.songs = pd.DataFrame(
                columns=['title', 'duration', 'category', 'used']
            )
        try:
            self.day_playlists = pd.DataFrame(
                self.load_data('day_playlist.db', 'lsii'),
                columns=['songs', 'start time', 'break length', 'playlist duration']
            )
        except FileNotFoundError:
            self.day_playlists = pd.DataFrame(
                columns=['songs', 'start time', 'break length', 'playlist duration']
            )

    @staticmethod
    def load_data(filename: str, cols: str):
        """
        Load data from .db files with specified columns
        :param filename: Name of the file to load
        :param cols: Specified in order content datatypes of the columns,
        s - string, i - int, f - float, b - boolean, l - list in joined string
        :return: Appended table with saved data
        """
        cols = list(cols)
        file = open(filename, encoding='UTF-8')
        content_in = file.read().split('\n')  # split rows
        content_out = []  # output list to append
        file.close()

        # start to loading data only if file is not empty
        if len(content_in) > 1:
            # split the rows and change datatypes
            for row in content_in:
                new_row = row.split('\t')  # split columns

                # change datatypes
                for i in range(len(new_row)):
                    if cols[i] == 's':
                        pass
                    elif cols[i] == 'i':
                        new_row[i] = int(new_row[i])
                    elif cols[i] == 'f':
                        new_row[i] = float(new_row[i])
                    elif cols[i] == 'b':
                        new_row[i] = bool(new_row[i])
                    elif cols[i] == 'l':
                        new_row[i] = list(new_row[i])

                content_out.append(new_row)

        return content_out

    def save_data(self, filename: str, data: pd.DataFrame):
        """
        Save data from pandas' DataFrame to .db file
        :param filename: Name of the file to save in
        :param data: DataFrame to save in file
        :return: None
        """
        file = open(filename, 'w', encoding='UTF-8')

        content = ''
        for row in self.songs.values:
            for v in row:
                file.write(str(v))
                if v != row[len(row) - 1]:
                    file.write('\t')
            if row.any() != self.songs.values[len(self.songs) - 1].any():
                file.write('\n')

    def refresh_(self):
        """
        Checks missing or new audio files and deletes or adds them to database
        :return: None
        """
        files = listdir('music')  # [f for f in listdir('music') if isfile(join('music', f))]  # get list of files

        # add file to database if it doesn't exist in there
        for f in files:
            if f not in self.songs.values:
                duration = mutagen.File(path.join('music', f)).info.length
                self.songs.loc[len(self.songs)] = [f, int(duration), 'None', False]

        # remove song from database if it doesn't exist in music folder
        for s in self.songs['title']:
            if s not in files:
                self.songs = self.songs.drop(self.songs.loc[self.songs['title'] == s].index)
                print(self.songs.loc[self.songs['title'] == s].index)

        self.save_data('songs.db', self.songs)


class Player:
    """
    Module for playing created playlists
    """
    def __init__(self, playlist: list[str], music_dir: str):
        mixer.init()

        # values passed at initialization
        self.playlist = playlist
        self.music_dir = music_dir

        self.db = PlayerDatabase()
        self.counter = 0  # which song in the playlist is currently played
        self.loaded = False  # for checking if music file is currently loaded
        self.cur_song = self.playlist[self.counter]  # currently played song
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
        pos = mixer.music.get_pos() / 1000  # get current position in seconds

        # block position getting out of song length
        if self.songs_lengths[self.counter] < pos:
            pos = self.songs_lengths[self.counter]

        # get song elapsed and left time
        # change position to minutes and second format
        pos_M = int(pos / 60)
        pos_S = int(pos - pos_M * 60)
        s_elapsed = dt.time(minute=pos_M, second=pos_S)  # change position to time object
        # calculate time left
        s_left = self.songs_lengths[self.counter] - pos
        left_M = int(s_left / 60)
        left_S = int(s_left - left_M * 60)
        s_left = dt.time(minute=left_M, second=left_S)

        # get playlist elapsed and left time
        # sum up the previous lengths of songs for elapsed time
        p_elapsed = 0
        for i in range(0, self.counter):
            p_elapsed += self.songs_lengths[i]
        p_elapsed += pos
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

        self.window1 = None
        self.window2 = None
        self.gui = Gui()

    def run(self):
        """
        App main loop
        """

        self.window1 = Gui().main_window()
        counter = 0

        while True:
            window, event, values = sg.read_all_windows(timeout=1000, timeout_key='_clock_') # # #

            print(event, values)   # # # debugging # # #

            # closing specified window at event
            if event == sg.WIN_CLOSED or event == '_cancel_':
                window.close()
                if window == self.window2:
                    self.window2 = None
                    self.window1.enable()
                elif window == self.window1:
                    break
            elif event == '_clock_':
                counter += 1
                self.window1['_song_progress_'].update(counter)


if __name__ == '__main__':
    App().run()
