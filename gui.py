import PySimpleGUI as sg
from screeninfo import get_monitors


class Gui(object):
    """
    Gui class containing windows and widgets inherited
    from PySimpleGui with changed default values
    """

    ''' Static values to call in inner classes '''
    # gets main screen size
    for m in get_monitors():
        if m.is_primary:
            screen = (m.width, m.height)
    # fonts and font sizes depended on sreen size
    fonts = {
        'MAIN': 'Comic {}'.format(round(19 / 1920 * screen[0])),
        'LISTS': 'Comic {}'.format(round(17 / 1920 * screen[0]))
    }
    # color palette
    colors = {
            'TEXT': '#EFF9F9',
            'COLOR_1': '#448CC9',
            'COLOR_2': '#99D0EE',
            'BGR_1': '#85AEC5',
            'BGR_2': '#7197AD',
            'BGR_3': '#DAECFB',
            'WHITE': '#FFFFFF',
            'SNOW': '#FFFAFA',
            'More Grey': '#7B8FA2'
        }

    def __init__(self):
        pass

    ''' Widgets used in app '''
    class Button(sg.Button):

        def __init__(self, *args, **kwargs):
            super().__init__(
                *args,
                **kwargs,
                border_width=0,
                font='Comic',
                button_color=(Gui.colors['TEXT'], Gui.colors['COLOR_1']),
                mouseover_colors=(Gui.colors['TEXT'], Gui.colors['COLOR_2'])
            )

    class Slider(sg.Slider):

        def __init__(self, *args, **kwargs):
            super().__init__(
                *args,
                **kwargs,
                relief=sg.RELIEF_FLAT,
                font='Comic',
                text_color=Gui.colors['TEXT'],
                trough_color=Gui.colors['BGR_3'],
                background_color=Gui.colors['COLOR_1']
            )

    class Text(sg.Text):

        def __init__(self, *args, **kwargs):
            super().__init__(
                *args,
                **kwargs,
                font='Comic',
                text_color=Gui.colors['TEXT'],
                background_color=Gui.colors['BGR_1']
            )

    class ProgressBar(sg.ProgressBar):

        def __init__(self, *args, **kwargs):
            super().__init__(
                *args,
                **kwargs,
                max_value=100,
                size=(40, 10),
                orientation='horizontal',
                bar_color=(Gui.colors['COLOR_1'], Gui.colors['BGR_3'])
            )

    def music_progressbar(self):
        """
        Container for all information and controls to music playback
        :return: Ready to implement layout
        """

        layout = [
            [
                Gui.Button('play', key='_play_'),
                Gui.Button('pause', key='_pause_'),
                Gui.Button('stop', key='_stop_'),
                sg.Push(background_color=Gui.colors['BGR_1']),
                Gui.Button('No volume', key='_no_volume_')
            ],
            [
                Gui.Text('Song:'),
                sg.Push(background_color=Gui.colors['BGR_1']),
                Gui.Text('--:--'),
                Gui.ProgressBar(key='_song_progress_'),
                Gui.Text('--:--'),
            ],
            [
                Gui.Text('Playlist:'),
                sg.Push(background_color=Gui.colors['BGR_1']),
                Gui.Text('--:--'),
                Gui.ProgressBar(key='_playlist_progress_'),
                Gui.Text('--:--'),
            ]
        ]

        return layout

    ''' Windows used in app '''
    def main_window(self):
        """
        Main window with app menu, table of today's playlists and music progressbar
        :return: Window element
        """

        col_1 = sg.Column([[]])

        col_2 = sg.Column([[]])

        layout = [
            [col_1, col_2],
            [self.music_progressbar()]
        ]

        return sg.Window(
            'Main window',
            layout,
            finalize=True,
            background_color=Gui.colors['BGR_1']
        )

