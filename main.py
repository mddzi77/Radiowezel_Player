import mutagen
import json
import PySimpleGUI as sg
import datetime as dt
import numpy as np
import pandas as pd
import gui as g
from os import listdir, mkdir, path
from pygame import mixer
from playerdatabase import PlayerDatabase


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

        self.db = PlayerDatabase()
        self.db.refresh_()

        self.window1 = None
        self.window2 = None

        self.player = None
        self.playing = False

    def close(self, window: sg.Window):
        """
        Close secondary window
        :param window: window element from read_all_windows()
        :return: None
        """
        window.close()
        self.window2 = None
        self.window1.enable()

    def run(self):
        """
        App main loop
        """

        self.window1 = g.main_window()
        self.window1.keep_on_top_set()

        # values to temporarily use in app or to indicate state
        counter = 0
        dir_list = self.settings['options'][1]['value']
        sorting = 'default'

        while True:
            window, event, values = sg.read_all_windows(timeout=1000, timeout_key='_clock_') # # #

            print(event, values)   # # # debugging # # #

            # closing window
            if event == sg.WIN_CLOSED or event == '_cancel_':
                window.close()
                if window == self.window2:
                    self.window2 = None
                    self.window1.enable()
                elif window == self.window1:
                    break

            # main window
            elif event == '_settings_':
                self.window2 = g.settings_window()
                # updating default values
                self.window2['_dir_list_'](dir_list)
                self.window2['_lang_'](self.settings['options'][0]['value'])

                self.window1.disable()
                self.window2.keep_on_top_set()
            elif event == '_music_db_':
                self.window2 = g.music_db_window(self.db)

                self.window1.disable()
                self.window2.keep_on_top_set()

            # music database
            elif event == '_used_unused_':
                # invert used and unused state
                tab = values['_tab_group_']  # get selected tab
                # convert selected tab to selected table
                tab_to_table = {
                    '_tab_all_': '_all_table_',
                    '_tab_unused_': '_unused_table_',
                    '_tab_used_': '_used_table_'
                }
                table = tab_to_table[tab]

                title = self.window2[table].Values[values[table][0]][0]  # get selected title
                # get selected value index in database
                index = self.db.songs['title'].loc[self.db.songs['title'] == title].index.tolist()[0]
                # change to opposite state
                value = self.db.songs['used'].iloc[index]
                self.db.songs.loc[index] = self.db.songs.loc[index].replace(to_replace=value, value=not value)

                # clear inputs in case
                self.window2['_all_browse_']('')
                self.window2['_unused_browse_']('')
                self.window2['_used_browse_']('')
                # update used and unused tables
                self.window2['_unused_table_'](self.db.get_songs(condition=('used', False)))
                self.window2['_used_table_'](self.db.get_songs(condition=('used', True)))
            elif event in ['_all_browse_', '_unused_browse_', '_used_browse_']:
                # search songs in table
                text_in = values[event]  # get typed text
                # get in which table search
                event_to_table = {
                    '_all_browse_': '_all_table_',
                    '_unused_browse_': '_unused_table_',
                    '_used_browse_': '_used_table_'
                }
                table = event_to_table[event]
                # get unfiltered content
                if event == '_all_browse_':
                    content = self.db.get_songs()
                elif event == '_unused_browse_':
                    content = self.db.get_songs(condition=('used', False))
                elif event == '_used_browse_':
                    content = self.db.get_songs(condition=('used', True))

                searched = [value for value in content if text_in.lower() in value[0].lower()]  # filter content

                self.window2[table](searched)

            # settings window
            elif event == '_add_dir_':
                # add new music directory
                dir_list.append(values[event])
                self.window2['_dir_list_'](dir_list)
            elif event == '_remove_dir_':
                # remove selected music directory
                dir_list.pop(self.window2['_dir_list_'].get_indexes()[0])
                self.window2['_dir_list_'](dir_list)
            elif event == '_save_settings_':
                # save settings
                self.settings['options'][1]['value'] = dir_list
                self.settings['options'][0]['value'] = values['_lang_']
                with open('settings.json', 'w', encoding='UTF-8') as f:
                    f.write(json.dumps(self.settings))

                self.db.refresh_()
                self.close(window)

            # interacting with playback
            elif event == '_play_pause_':
                p = ['Myslovitz-D_ugo__ d_wi_ku samotno_ci.mp3', 'Najnowszy Klip.mp3', 'Myslovitz - Mie_ czy by_ tekst .mp3']
                self.player = Player(p, 'music')
                self.player.play()

            # clock for counting time of the playlists and songs
            elif event == '_clock_':
                try:
                    song_t, playlist_t = self.player.music_clock()

                    # update progressbars
                    self.window1['_song_progress_'](self.player.pos, self.player.songs_lengths[self.player.counter])
                    self.window1['_playlist_progress_'](self.player.pos_playlist, self.player.playlist_length)

                    # update texts
                    self.window1['_elapsed_s_'](song_t[0].strftime('%M:%S'))
                    self.window1['_left_s_'](song_t[1].strftime('%M:%S'))
                    self.window1['_elapsed_p_'](playlist_t[0].strftime('%M:%S'))
                    self.window1['_left_p_'](playlist_t[1].strftime('%M:%S'))
                except AttributeError:
                    pass


if __name__ == '__main__':
    App().run()
