import mutagen
import pandas as pd
from os import listdir, mkdir, path


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