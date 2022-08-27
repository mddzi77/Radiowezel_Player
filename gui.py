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
            'Boston Blue': '#448CC9',
            'Black Squeeze': '#EFF9F9',
            'Glacier': '#85AEC5',
            'Cornflower': '#99D0EE',
            'White': '#FFFFFF',
            'Snow': '#FFFAFA',
            'Grey': '#7197AD',
            'More Grey': '#7B8FA2'
        }

    def __init__(self):
        pass

    ''' Widgets used in app '''
    class Button(sg.Button):

        def __init__(self, *args):
            super().__init__(
                *args,
                border_width=0,
                font=Gui.fonts
            )

    class Playbar(sg.Column):
        pass

    ''' Windows used in app '''
    class MainWindow(sg.Window):
        """
        Main window of the app
        """
        def __init__(self):

            layout = [
                [col_1, col_2],
                [Gui.Playbar]
            ]
