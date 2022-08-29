import PySimpleGUI as sg
from screeninfo import get_monitors
from random import randrange

data = [[randrange(0, 100) for i in range(4)] for j in range(100)]
data2 = [[1, 'GenYoutube.net_Mike-Posner-I-Took-A-Pill-In-Ibiza-Original_41GZVVcxQps', '22:22'],
         [2, '01 Macklemore  Ryan Lewis - Can_t Hold Us _ft Ray Dalton__', '33:33']]

''' Global default values for widgets and windows'''
# color palette used in app
colors = {
    'TEXT_1': '#EFF9F9',
    'TEXT_2': '#28405E',
    'COLOR_1': '#448CC9',
    'COLOR_2': '#99D0EE',
    'COLOR_3': '#DAECFB',
    'BGR_1': '#85AEC5',
    'BGR_2': '#7197AD',
    'BGR_3': '#A2CBE2',
    'WHITE': '#FFFFFF',
    'SNOW': '#FFFAFA',
    'GREY': '#7B8FA2'
        }

# gets main screen size
for m in get_monitors():
    if m.is_primary:
        screen = (m.width, m.height)


# # # Widgets created used class inheritance # # #

class Button(sg.Button):
    def __init__(self, *args, border_width=0, font='Comic', button_color=(colors['TEXT_1'], colors['COLOR_1']),
                 mouseover_colors=(colors['TEXT_1'], colors['COLOR_2']), **kwargs):

        super().__init__(*args, border_width=border_width, font=font, button_color=button_color,
                         mouseover_colors=mouseover_colors, **kwargs)


class Slider(sg.Slider):
    def __init__(self, *args, relief=sg.RELIEF_FLAT, font='Comic', text_color=colors['TEXT_1'],
                 trough_color=colors['BGR_3'], background_color=colors['COLOR_1'], **kwargs):

        super().__init__(*args, relief=relief, font=font, text_color=text_color,
                         trough_color=trough_color, background_color=background_color, **kwargs)


class Text1(sg.Text):
    def __init__(self, *args, font='Comic', text_color=colors['TEXT_1'], background_color=colors['BGR_1'], **kwargs):

        super().__init__(*args, font=font, text_color=text_color, background_color=background_color, **kwargs)


class Text2(sg.Text):
    def __init__(self, *args, font='Comic', text_color=colors['TEXT_2'], background_color=colors['SNOW'], **kwargs):

        super().__init__(*args, font=font, text_color=text_color, background_color=background_color, **kwargs)


class ProgressBar(sg.ProgressBar):
    def __init__(self, *args,  max_value=100, size=(80, 10), orientation='horizontal',
                 bar_color=(colors['COLOR_1'], colors['SNOW']), **kwargs):

        super().__init__(*args,  max_value=max_value, size=size, orientation=orientation,
                         bar_color=bar_color, **kwargs)


class Frame(sg.Frame):
    def __init__(self, *args, background_color=colors['WHITE'], font='Comic', relief=sg.RELIEF_GROOVE,
                 title_color=colors['COLOR_1'], **kwargs):

        super().__init__(*args,  background_color=background_color, font=font, relief=relief,
                         title_color=title_color, **kwargs)


class Table(sg.Table):
    def __init__(self,
                 *args,
                 text_color=colors['TEXT_1'],
                 background_color=colors['BGR_3'],
                 max_col_width=100,
                 selected_row_colors=(colors['GREY'],colors['COLOR_3']),
                 font='Comic',
                 header_text_color=colors['TEXT_1'],
                 header_background_color=colors['COLOR_1'],
                 header_relief=sg.RELIEF_FLAT,
                 sbar_relief=sg.RELIEF_FLAT,
                 sbar_trough_color=colors['BGR_3'],
                 sbar_background_color=colors['COLOR_1'],
                 sbar_arrow_color=colors['COLOR_3'],
                 enable_events=True,
                 auto_size_columns=False,
                 row_colors=None,
                 selected_row: int = None,
                 **kwargs):

        super().__init__(*args,
                         text_color=text_color,
                         background_color=background_color,
                         max_col_width=max_col_width,
                         selected_row_colors=selected_row_colors,
                         font=font,
                         header_text_color=header_text_color,
                         header_background_color=header_background_color,
                         header_relief=header_relief,
                         sbar_relief=sbar_relief,
                         sbar_trough_color=sbar_trough_color,
                         sbar_background_color=sbar_background_color,
                         sbar_arrow_color=sbar_arrow_color,
                         auto_size_columns=auto_size_columns,
                         enable_events=enable_events,
                         row_colors=[(selected_row, colors['COLOR_1'])] if selected_row else row_colors,
                         **kwargs)


class DefWindow(sg.Window):
    """
        Default look of app window
    """

    def __init__(self, *args, layout: list, finalize=True, background_color=colors['BGR_1'], margins=(0, 0),
                 use_custom_titlebar=True, titlebar_background_color=colors['BGR_1'], titlebar_font='Comic',
                 titlebar_text_color=colors['TEXT_1'], **kwargs):
        layout = sg.Column(
            [[sg.Column(layout, background_color=colors['SNOW'], pad=(8, 5), expand_x=True, expand_y=True)]],
            background_color=colors['SNOW'],
            pad=((4, 4), (0, 4)),
            expand_x=True,
            expand_y=True)

        super().__init__(*args, layout=[[layout]], finalize=finalize, background_color=background_color,
                         margins=margins, use_custom_titlebar=use_custom_titlebar,
                         titlebar_font=titlebar_font, titlebar_text_color=titlebar_text_color,
                         titlebar_background_color=titlebar_background_color, **kwargs)


class WindowPlaybar(sg.Window):
    """
    Default window with addition of Playbar
    """
    def __init__(self, *args, layout: list, finalize=True, background_color=colors['BGR_1'], margins=(0, 0),
                 use_custom_titlebar=True, titlebar_background_color=colors['BGR_1'], titlebar_font='Comic',
                 titlebar_text_color=colors['TEXT_1'], **kwargs):

        layout = sg.Column(
            [[sg.Column(layout, background_color=colors['SNOW'], pad=(8, 5), expand_x=True, expand_y=True)]],
            background_color=colors['SNOW'],
            pad=(4, 0),
            expand_x=True,
            expand_y=True)

        layout = [[layout]] + [[playbar()]]

        super().__init__(*args, layout=layout, finalize=finalize, background_color=background_color,
                         margins=margins, use_custom_titlebar=use_custom_titlebar,
                         titlebar_font=titlebar_font, titlebar_text_color=titlebar_text_color,
                         titlebar_background_color=titlebar_background_color, **kwargs)


# # # Ready to implement layouts # # #

def playbar():
    """
    Container for all information and controls to music playback
    :return: Ready to implement layout
    """

    layout = [
        [
            sg.Push(background_color=colors['BGR_1']),
            Button('', key='_play_pause_', image_source='icons\\play.png',
                   button_color=(colors['BGR_1'], colors['BGR_1']), image_size=(30, 30)),
            Button('', key='_stop_', image_source='icons\\stop.png',
                   button_color=(colors['BGR_1'], colors['BGR_1']), image_size=(30, 30)),
            Button('', key='_mute_unmute_', image_source='icons\\volume.png',
                   button_color=(colors['BGR_1'], colors['BGR_1']), image_size=(30, 30)),
            sg.Push(background_color=colors['BGR_1'])
        ],
        [
            sg.Column(
                [[Text1('Song:'),
                  sg.Push(background_color=colors['BGR_1']),
                  Text1('--:--', key='_elapsed_s_', justification='c', size=(7, 1)),
                  ProgressBar(key='_song_progress_'),
                  Text1('--:--', key='_left_s_', justification='c', size=(7, 1))]],
                colors['BGR_1'],
                expand_x=True
            )
        ],
        [
            sg.Column(
                [[Text1('Playlist:'),
                  sg.Push(background_color=colors['BGR_1']),
                  Text1('--:--', key='_elapsed_p_', justification='c', size=(7, 1)),
                  ProgressBar(key='_playlist_progress_'),
                  Text1('--:--', key='_left_p_', justification='c', size=(7, 1))]],
                colors['BGR_1'],
                expand_x=True
            )
        ],
    ]

    layout = sg.Column(layout, colors['BGR_1'], pad=(5, 5))

    return sg.Column([[layout]], colors['BGR_1'], pad=(0, 0))


def header():

    layout = [[
        Text1('asdasd', background_color=colors['BGR_1']),
        sg.Push(background_color=colors['BGR_1']),
        Button(
            image_source='icons\\close.png',
            button_color=(colors['BGR_1'], colors['BGR_1']),
            image_subsample=23,
            mouseover_colors='#EB2628',
            key='_cancel_'
        )
    ]]

    return sg.Column(layout, colors['BGR_1'], pad=(0, 0), expand_x=True)


# # # Windows used in apps # # #

def main_window():
    """
    Main window with app menu, table of today's playlists and music progressbar
    :return: Window element
    """

    col_1 = Frame(
        'OPTION MENU',
        [
            [Button('Enable Autoplay', key='_autoplay_enabler_')],
            [Button('Music Database', key='_music_db_')],
            [Button('Playlists Editor', key='_editor_')],
            [Button('Settings', key='_settings_')]
        ]
    )

    col_2 = Frame(
        '',
        [
            [Text2('Today\'s Playlists:')],
            [Table(
                data,
                ['Nr', 'Start Time', 'Break\'s length', 'Playlist Length'],
                key='_today_plalist_',
                col_widths=[4, 19, 19, 20],
                justification='c',
                num_rows=10,
                selected_row=None,
                hide_vertical_scroll=True
            )],
            [Text2('Selected Playlist:')],
            [Table(
                data2,
                ['Nr', 'Title', 'Length'],
                key='_selected_playlist_',
                col_widths=[4, 50, 8],
                justification='c',
                num_rows=8,
                hide_vertical_scroll=True
            )]
        ],
    )

    layout = [[col_1, sg.Push(background_color=colors['SNOW']), col_2]]

    return WindowPlaybar('School Radio Player', layout=layout)


def settings_window():
    """
    Creates settings window, to choose language, and music directories
    :return:
    """

