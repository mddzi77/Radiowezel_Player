import mutagen
import json
import pandas as pd
from os import listdir, mkdir, path


class PlayerDatabase(object):
    def __init__(self, ):
        # get settings
        with open('settings.json', encoding='UTF-8') as f:
            self.settings = json.load(f)['options']

        # initialize pandas dataframes
        try:
            self.songs = pd.DataFrame(
                self.load_data('archive\\songs.db', 'ssisb'),
                columns=['title', 'path', 'duration', 'category', 'used']
            )
        except FileNotFoundError:
            self.songs = pd.DataFrame(
                columns=['title', 'path', 'duration', 'category', 'used']
            )
        try:
            self.day_playlists = pd.DataFrame(
                self.load_data('archive\\day_playlist.db', 'lsii'),
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
        filename = path.join('archive', filename)
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
        filename = path.join('archive', filename)
        file = open(filename, 'w', encoding='UTF-8')

        content = ''
        for row in self.songs.values:
            for v in row:
                file.write(str(v))
                if v != row[len(row) - 1]:
                    file.write('\t')
            if row.any() != self.songs.values[len(self.songs) - 1].any():
                file.write('\n')

    @staticmethod
    def ismusic(file: str):

        if file.endswith('.mp3'):
            return True
        elif file.endswith('.wav'):
            return True
        else:
            return False

    def change_use(self, to: str):
        pass

    def get_songs(self, nums=False, condition=(None, None)):
        """
        Get formatted values from songs dataframe
        :param nums: Indicates if there should be first column with numbers
        :param condition: First value is for the column name, second is for content that is looked for
        :return: Dataframe values formatted toa list
        """
        # get list
        if condition == (None, None):
            data = self.songs[['title', 'duration']].values.tolist()
        else:
            data = self.songs[['title', 'duration']].loc[self.songs[condition[0]] == condition[1]].values.tolist()

        # change duration in seconds to formatted string and add numbers if needed
        out = []
        i = 1
        for d in data:
            m = int(d[1] / 60)
            s = d[1] - m * 60
            row = [d[0], f'{m}:{s}']
            if nums:
                row = [i + 1] + row
            out.append(row)
            i += 1

        return out

    def refresh_(self):
        """
        Checks missing or new audio files and deletes or adds them to database
        :return: None
        """
        directories = self.settings[1]['value']

        # do all checkings for all directories
        for d in directories:
            files = [f for f in listdir(d) if path.isfile(path.join(d, f)) and self.ismusic(f)]  # get list of files

            # add file to database if it doesn't exist in there
            for f in files:
                if f not in self.songs.values:
                    duration = mutagen.File(path.join(d, f)).info.length
                    self.songs.loc[len(self.songs)] = [f, d, int(duration), 'None', False]

            # remove song from database if it doesn't exist in music folder
            for s in self.songs['title'].loc[self.songs['path'] == d]:
                if s not in files:
                    self.songs = self.songs.drop(self.songs.loc[self.songs['title'] == s].index)
                    print(self.songs.loc[self.songs['title'] == s].index)

        self.save_data('songs.db', self.songs)
