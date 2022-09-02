import base64
import json
import base64
import PySimpleGUI as sg
import pandas as pd

from playerdatabase import PlayerDatabase
from screeninfo import get_monitors
from random import randrange

data = [[randrange(0, 100) for i in range(4)] for j in range(100)]
data2 = [[1, 'GenYoutube.net_Mike-Posner-I-Took-A-Pill-In-Ibiza-Original_41GZVVcxQps', '22:22'],
         [2, '01 Macklemore  Ryan Lewis - Can_t Hold Us _ft Ray Dalton__', '33:33']]

''' Global default values for widgets and windows'''
# settings
with open('settings.json', encoding='UTF-8') as f:
    settings = json.load(f)['options']

# app icon
app_icon = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAIfUlEQVR4nN1bCawV1Rn+5hYpokabmiaicYlWpRYXgjPaqFGcQdSosa1a' \
           b'E22lJEaCG8xYi4YYNSrGGYlb2lSf4pa2KqZKKoQZSIxFMmPrCuKKuNtWxYUYRWHMP/4X7533n7nnzL33weNLbl7enDPnX85/ln8ZK89z' \
           b'dAMveqoB5JMA/BrALwDsCWAUgE8ArALwOIBFAJ6MffsbHVJelI0AcBiAEwAcDWAsgB0BfAVgDYDlAObDwsJ4pr2xG/67UoAXZRMB3ATg' \
           b'5xrdSSEJgIUAFsS+/f/SWDsDOAnA8fQvgJ00xiQFXxT7dlxXhloK8KLMAnAVgMtpjBp01wO4E8Bl/P+1AH4PYGSNsUiA6/OGdVky41Bj' \
           b'YUbUIEiIAMyo+S5Y0PMAHMf/79XFWDQBf7Q25tsBuND4ZVML8KLsLAD3mhIaIkyJfXueCSkjBXhR9iMArwL4sdBMG9w/ACzl9U6b4bEA' \
           b'jgDww5ry01J5AsAS3vx24jFPUVjvWgD7xL79sS4B0yUwTSH86wB+Gfv286Xn13lRtj0zTZvbiQB260DjHQD/5M1ySezb60rtf/Ki7EAA' \
           b'DwPYu9RGEzQdwNW6AplawEsA9is9Jq2Pj317jcb7P2DmZim6XIccs+PA3qAxFlnYM8Jp8Vrs2z/t9H4THRXgRdlPAJzKs3ia0GVW7Ntz' \
           b'dAm60VOWhXyVoMiX8zwfmwSO9ox4UUanyDVC03w+ch+Offt/VWM0Kgbfw4uyuwC8DeDPCuEJD+kyTEj84qhaITStMBGe8aDi+a9oqRDv' \
           b'XpTNY2sRMWgP8KKM/pxPZyuA0Z04yIE3DJkmSLc34xvdRgurG9Uqo+P2dzR5XpRdCuDW2LfbOrRZgBeltEYHANyiIzyKGe28XvuFJTO1' \
           b'aY9mme50byxkHKyA72beup1vZFsrpli5dTtbebsCAFxAHSoE/2IYKaWK1ymtN8ZCAV6U7cVrXsJ/AdDtb2q/ue4hpjLPHyiGnMMyb7IA' \
           b'cmy2FTo+B+CQ2LfvB7BZ1jqZa/NngA3M83iWoYxtWWY0vCjbBcBvhE7vA5gc+/b7vRDEsqxNP5O+SeBs+pmCeZ/MspRxBsne4ECGdCWe' \
           b'Efu2yoREZiUhdYXW6VtFRwWWQfJct6H7AilgotC4GnlDdcnoiTBDCSsvLkyrBZLHkgIOFBoWxMGErkJNpkgC5/R+jb04KMJmC4SmcaSA' \
           b'MULDC/1iRkISOD03FcH6JJl2HcEBzDI+F56JAU03zLZJAvvruow2hXfD9GD2Eieyy92UgLzNW62GdUU80267+HphOlJxEy54bSqBHT5J' \
           b'plEqZ0ga90NF158pxuiIFuHPBkDnHC2DnUtxRvLxZ+cb898KTI5V0GgLuLIiRF2ZBERWsMNSVho5GzMNxmlb7zzzA7wrV4EixXcLtMsg' \
           b'Hlfq8qJ0h8uIfXstz1IZ090wPVx3HAGzNIQntHmdTHO60C9LAmetLnFtBTAGhGfkci50w/R0N0zrbGbSMVwGhdrmNp8RLQ6ZSWF0iUcl' \
           b'lEuA1o0QLboHwB8AlENOlLX5O4Ar3TB9hJlblgSOTiZIijHO5ewPeBN8PAmcYqN1w/RFqNf+q7AKHrWhVAAJX1ZCEjjr3TCdypFf6d39' \
           b'+UfBh0/dMG1mghYlgfOugpRkNcuTwNl0ESPLcsP0FI46q0DKnpr4znoTBXRcAuXzNAmcJzip0emitCOHpu6g0JQbps+6YTrHDdOjTBhk' \
           b'DHQQnniZxrwZofIUaFpBGUngDLhh+hkztoMGQRrkoCRwDjZl0A3TTnHCdcXMB84DpmMTOlpAUwmCJZCJjuO139FV7sNtbwPTHtdJ+KrI' \
           b'd93cYIEkcN4kV9oN093Z3CmdfWQ5E9QqvHtDOhJW4aePUdzOqkDr+18AHqOIcBI4b3XDP0FLAaql0AQzQjv3XDdMt+ejjTJBk5PAKSIv' \
           b'bpiO5mzwdM3UdxNvcX1BkSlKAsdUaZXoygIkJIFDa/JR/hVww5SSK4tpH6gx5B51giG6ML0IGWNimDY4U1NH+FqRIBP0XQEN4EzOEG8W' \
           b'dEr9dVwCPYjqnLOlCk/ouwUAmDAENAZBN+s9FArQuSiV0VUIvix8lRUPhQLeG6J3RLQIL8raUIS66lRrqbDUsD+V1zzdC8KlmZcSP9+Q' \
           b'Aj4SGvYUBqiLmw1T37eR19ktUYF3qTTnQ1LAy0KDTpBCC0ngPF2UvujhWa4Z7AeOEcZ8hRSwTGg42ouy/boto23BbC5lqbIEcmWPSwKn' \
           b'6yx0efbdMN2fS27LWEaBBiqZSIXGxcityXFwaN6rDI8bpuM5NU0Wtgu7sv8GMC/P8dcllzg9T8Z4YUpFJIs4qFqGTQqgZ//hTGoZIYBL' \
           b'qKxkS0lzmYBluwFAILxGMk9ocM3MFYpx6cX7uEByWMENU/I471MIX8hcTCytc869P8Q+vQQ6Kf7ynYdnrQTyz/vtpOigdY/iEp8dgPwA' \
           b'ACcDOFcRcCXMj32bsuLf1wnyLKdCxHdrA5X6Opzn+P52xA8mlRMQWxmomnVSU/g2BbAS1vBXH8bR1WEAkunwcknvoPsxVVTksOjScLHi' \
           b'ljjcQJXjF+cWjpEqXiprhb0oI0/ubK4hOkwzh7cl4Gvez/5G2azYt5VxRO1qcS/KRnNKaoyipsAEVLNTTqgub83/1cSX7H2uin1b60bZ' \
           b'9VdjdeBF2QNC8fWDsW/3rUxGhcp4wHC8/ZmiUgGbwzqGGkMREdpiIFl0z/cA/p5n3w7fE9bZBInRV4TvkgahtTiqLPSgeGHzgaIgwghe' \
           b'lN3Y5feEOpgb+7ZYk6SzZ1UqQNVJBzzzUmFyP3CQZAlVCpAKPgjiHmBSi9uCbr7+NIURraoJ1aoQ0VTIco7w9BvrWuqH2visA+NTQFWx' \
           b'zZ+n0ed1FGTtx/lJY9LYpxItk6pxZR8A3wI9H8V+ReXPYgAAAABJRU5ErkJggg=='

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

# database
pdb = PlayerDatabase()

# # # Widgets created used class inheritance # # #

class Button(sg.Button):
    def __init__(self, *args, border_width=0, font='Comic', button_color=(colors['TEXT_1'], colors['COLOR_1']),
                 mouseover_colors=(colors['TEXT_1'], colors['COLOR_2']), **kwargs):

        super().__init__(*args, border_width=border_width, font=font, button_color=button_color,
                         mouseover_colors=mouseover_colors, **kwargs)

class FolderBrowse(sg.Button):
    def __init__(self, *args, border_width=0, font='Comic', button_color=(colors['TEXT_1'], colors['COLOR_1']),
                 mouseover_colors=(colors['TEXT_1'], colors['COLOR_2']), target=(555666777, -1), **kwargs):

        super().__init__(*args, border_width=border_width, font=font, button_color=button_color,
                         mouseover_colors=mouseover_colors, target=target,
                         button_type=sg.BUTTON_TYPE_BROWSE_FOLDER, **kwargs)


class Combo(sg.Combo):
    def __init__(self, *args, background_color=colors['BGR_3'], text_color=colors['TEXT_1'], font='Comic',
                 button_background_color=colors['COLOR_1'], button_arrow_color=colors['COLOR_3'],
                 auto_size_text=False, **kwargs):

        super().__init__(*args, background_color=background_color, text_color=text_color, font=font,
                         button_background_color=button_background_color, button_arrow_color=button_arrow_color,
                         auto_size_text=auto_size_text, **kwargs)


class Slider(sg.Slider):
    def __init__(self, *args, relief=sg.RELIEF_FLAT, font='Comic', text_color=colors['TEXT_1'],
                 trough_color=colors['BGR_3'], background_color=colors['COLOR_1'], **kwargs):

        super().__init__(*args, relief=relief, font=font, text_color=text_color,
                         trough_color=trough_color, background_color=background_color, **kwargs)


class ProgressBar(sg.ProgressBar):
    def __init__(self, *args,  max_value=100, size=(80, 10), orientation='horizontal',
                 bar_color=(colors['COLOR_1'], colors['SNOW']), **kwargs):

        super().__init__(*args,  max_value=max_value, size=size, orientation=orientation,
                         bar_color=bar_color, **kwargs)


class Input(sg.Input):
    def __init__(self, *args, background_color=colors['BGR_3'], text_color=colors['TEXT_1'], enable_events=True,
                 font='Comic', **kwargs):

        super().__init__(*args, background_color=background_color, text_color=text_color, enable_events=enable_events,
                         font=font,**kwargs)


class Text1(sg.Text):
    def __init__(self, *args, font='Comic', text_color=colors['TEXT_1'], background_color=colors['BGR_1'], **kwargs):

        super().__init__(*args, font=font, text_color=text_color, background_color=background_color, **kwargs)


class Text2(sg.Text):
    def __init__(self, *args, font='Comic', text_color=colors['TEXT_2'], background_color=colors['SNOW'], **kwargs):

        super().__init__(*args, font=font, text_color=text_color, background_color=background_color, **kwargs)


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


class Listbox(sg.Listbox):
    def __init__(self,
                 *args,
                 text_color=colors['TEXT_1'],
                 background_color=colors['BGR_3'],
                 highlight_text_color=colors['GREY'],
                 highlight_background_color=colors['COLOR_3'],
                 font='Comic',
                 sbar_relief=sg.RELIEF_FLAT,
                 sbar_trough_color=colors['BGR_3'],
                 sbar_background_color=colors['COLOR_1'],
                 sbar_arrow_color=colors['COLOR_3'],
                 enable_events=True,
                 **kwargs):

        super().__init__(*args,
                         text_color=text_color,
                         background_color=background_color,
                         highlight_text_color=highlight_text_color,
                         highlight_background_color=highlight_background_color,
                         font=font,
                         sbar_relief=sbar_relief,
                         sbar_trough_color=sbar_trough_color,
                         sbar_background_color=sbar_background_color,
                         sbar_arrow_color=sbar_arrow_color,
                         enable_events=enable_events,
                         **kwargs)


class Tab(sg.Tab):
    def __init__(self,
                 *args,
                 title_color=colors['TEXT_1'],
                 background_color=colors['BGR_1'],
                 font='Comic',
                 border_width=0,
                 element_justification='c',
                 **kwargs):
        super().__init__(*args,
                         title_color=title_color,
                         background_color=background_color,
                         font=font,
                         border_width=border_width,
                         element_justification=element_justification,
                         **kwargs)


class TabGroup(sg.TabGroup):
    def __init__(self,
                 *args,
                 title_color=colors['TEXT_1'],
                 background_color=colors['SNOW'],
                 font='Comic',
                 border_width=0,
                 tab_background_color=colors['COLOR_1'],
                 selected_title_color=colors['TEXT_1'],
                 selected_background_color=colors['COLOR_2'],
                 **kwargs):
        super().__init__(*args,
                         title_color=title_color,
                         background_color=background_color,
                         font=font,
                         border_width=border_width,
                         tab_background_color=tab_background_color,
                         selected_title_color=selected_title_color,
                         selected_background_color=selected_background_color,
                         **kwargs)


class DefWindow(sg.Window):
    """
        Default look of app window
    """

    def __init__(self, *args, layout: list, finalize=True, background_color=colors['BGR_1'], margins=(0, 0),
                 use_custom_titlebar=True, titlebar_background_color=colors['BGR_1'], titlebar_font='Comic',
                 titlebar_text_color=colors['TEXT_1'], titlebar_icon='icons\\app_icon.png', **kwargs):
        layout = sg.Column(
            [[sg.Column(layout, background_color=colors['SNOW'], pad=(8, 5), expand_x=True, expand_y=True)]],
            background_color=colors['SNOW'],
            pad=((4, 4), (0, 4)),
            expand_x=True,
            expand_y=True)

        super().__init__(*args, layout=[[layout]], finalize=finalize, background_color=background_color,
                         margins=margins, use_custom_titlebar=use_custom_titlebar,
                         titlebar_font=titlebar_font, titlebar_text_color=titlebar_text_color,
                         titlebar_background_color=titlebar_background_color, titlebar_icon=titlebar_icon, **kwargs)


class WindowPlaybar(sg.Window):
    """
    Default window with addition of Playbar
    """
    def __init__(self, *args, configuration: str = 'both', layout: list, finalize=True,
                 background_color=colors['BGR_1'], margins=(0, 0), use_custom_titlebar=True,
                 titlebar_background_color=colors['BGR_1'], titlebar_font='Comic', titlebar_text_color=colors['TEXT_1'],
                 titlebar_icon='icons\\app_icon.png', **kwargs):

        layout = sg.Column(
            [[sg.Column(layout, background_color=colors['SNOW'], pad=(8, 5), expand_x=True, expand_y=True)]],
            background_color=colors['SNOW'],
            pad=(4, 0),
            expand_x=True,
            expand_y=True)

        layout = [[layout]] + [[playbar(configuration)]]

        super().__init__(*args, layout=layout, finalize=finalize, background_color=background_color,
                         margins=margins, use_custom_titlebar=use_custom_titlebar,
                         titlebar_font=titlebar_font, titlebar_text_color=titlebar_text_color,
                         titlebar_background_color=titlebar_background_color, titlebar_icon=titlebar_icon, **kwargs)


# # # Ready to implement layouts # # #

def playbar(configuration: str = 'both'):
    """
    Container for all information and controls to music playback
    :param configuration: Decides which progressbar will be shown 'both' | 'song' | 'playlist'
    :return: Ready to implement layout
    """
    buttons = [[
        sg.Push(colors['BGR_1']),
        Button('', key='_play_pause_', image_source='icons\\play.png',
               button_color=(colors['BGR_1'], colors['BGR_1']), image_size=(30, 30)),
        Button('', key='_stop_', image_source='icons\\stop.png',
               button_color=(colors['BGR_1'], colors['BGR_1']), image_size=(30, 30)),
        Button('', key='_mute_unmute_', image_source='icons\\volume.png',
               button_color=(colors['BGR_1'], colors['BGR_1']), image_size=(30, 30)),
        sg.Push(colors['BGR_1'])
    ]]
    song = [[
        sg.Column(
            [[Text1('Song:'),
              sg.Push(colors['BGR_1']),
              Text1('--:--', key='_elapsed_s_', justification='c', size=(7, 1)),
              ProgressBar(key='_song_progress_'),
              Text1('--:--', key='_left_s_', justification='c', size=(7, 1))]],
            colors['BGR_1'],
            expand_x=True)
    ]]
    playlist = [[
        sg.Column(
            [[Text1('Playlist:'),
              sg.Push(colors['BGR_1']),
              Text1('--:--', key='_elapsed_p_', justification='c', size=(7, 1)),
              ProgressBar(key='_playlist_progress_'),
              Text1('--:--', key='_left_p_', justification='c', size=(7, 1))]],
            colors['BGR_1'],
            expand_x=True)
    ]]

    if configuration == 'both':
        layout = buttons + song + playlist
    elif configuration == 'song':
        layout = buttons + song
    elif configuration == 'playlist':
        layout = buttons + playlist

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
    :return: WindowPlaybar element
    """

    col_1 = Frame(
        '',
        [
            [Text2('OPTION MENU:', text_color=colors['COLOR_1'], expand_x=True, justification='c')],
            [sg.VPush(colors['SNOW'])],
            [Button('Enable Autoplay', key='_autoplay_enabler_', size=(25, 1))],
            [Text2('', font='Comic 1')],
            [Button('Music Database', key='_music_db_', size=(25, 1))],
            [Text2('', font='Comic 1')],
            [Button('Playlists Editor', key='_editor_', size=(25, 1))],
            [Text2('', font='Comic 1')],
            [Button('Settings', key='_settings_', size=(25, 1))],
            [sg.VPush(colors['SNOW'])]
        ],
        background_color=colors['SNOW'],
        element_justification='c',
        size=(335, 200),
        expand_y=True
    )

    col_2 = Frame(
        '',
        [
            [Text2('Today\'s Playlists:')],
            [Table(
                data,
                ['Nr', 'Start Time', 'Break\'s length', 'Playlist Length'],
                key='_today_plalist_',
                col_widths=[4, 21, 21, 21],
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
                col_widths=[4, 55, 8],
                justification='c',
                num_rows=8,
                hide_vertical_scroll=True
            )]
        ],
        background_color=colors['SNOW']
    )

    layout = [[col_1, sg.Push(colors['SNOW']), col_2]]

    return WindowPlaybar('School Radio Player', layout=layout, icon=app_icon)


def settings_window():
    """
    Creates settings window, to choose language, and music directories
    :return: DefWindow element
    """
    layout = [
        [Text2('Language')],
        [Combo(['English', 'Polish'], size=(20, 1), key='_lang_')],
        [Text2('Music directories')],
        [sg.Input(key='_add_dir_', enable_events=True, visible=False),
         FolderBrowse('Add', target=(3, 0)),
         Button('Remove', key='_remove_dir_')],
        [Listbox([], key='_dir_list_', size=(50, 15))],
        [Button('Save', key='_save_settings_'), Button('Cancel', key='_cancel_')]
    ]

    return DefWindow('Settings', layout=layout)


def music_db_window(db: PlayerDatabase):
    """
    Creates window for managing saved music
    :return: Window with playbar for songs
    """
    tab_all = Tab(
        'All',
        [[Text1('Search:'), Input(key='_all_browse_')],
         [Table(db.get_songs(), key='_all_table_', headings=['Title', 'Duration'], col_widths=[60, 10],
                justification='left', num_rows=30)]],
        key='_tab_all_'
    )
    tab_unused = Tab(
        'Unused',
        [[Text1('Search:'), Input(key='_unused_browse_')],
         [Table(db.get_songs(condition=('used', False)), key='_unused_table_', headings=['Title', 'Duration'],
                col_widths=[60, 10], justification='left', num_rows=30)]],
        key='_tab_unused_'
    )
    tab_used = Tab(
        'Used',
        [[Text1('Search:'), Input(key='_used_browse_')],
         [Table(db.get_songs(condition=('used', True)), key='_used_table_', headings=['Title', 'Duration'],
                col_widths=[60, 10], justification='left', num_rows=30)]],
        key='_tab_used_'
    )

    tabs = TabGroup([[tab_all, tab_unused, tab_used]], key='_tab_group_')

    buttons_col = sg.Frame(
        '',
        [
            [sg.VPush(colors['SNOW'])],
            [Text2('Change to: ')],
            [Button('Unused', key='_to_unused_', size=(25, 1))],
            [Button('Used', key='_to_used_', size=(25, 1))],
            [Text2('', font='Comic 1')],
            [Button('Download song from YT', key='_yt_', size=(25, 1))],
            [sg.VPush(colors['SNOW'])]
        ],
        background_color=colors['SNOW'],
        element_justification='c',
        relief=sg.RELIEF_GROOVE,
        size=(300, 200),
        expand_y=True
    )
    buttons_col = sg.Column(
        [
            [Text2('')],
            [buttons_col]
        ],
        background_color=colors['SNOW'],
        expand_y=True
    )

    layout = [
        [buttons_col, sg.Push(colors['SNOW']), tabs]
    ]

    return WindowPlaybar('Music Database', layout=layout, configuration='song')
