import os

class Blocks:
    upper_block = '▀'
    lower_block = '▄'
    full_block = '█'

    upper_one_eighth = '▔'
    lower_one_eighth = '▁'
    left_one_eighth  = '▏'
    right_one_eighth  = '▕'

    medium_center = '━'
    medium_left = '┃'
    medium_right = '┃'
    medium_low = '━'
    top_left = '┏'
    top_right = '┓'
    bottom_left = '┗'
    bottom_right = '┛'
    whitespace = ' '
    tabspace = '\t'

class Terminal:
    def __init__(self,):
        pass
    
    def cols(self=None,)->int:
        return os.get_terminal_size()[0]

    def rows(self=None,)->int:
        return os.get_terminal_size()[1]

    def cols_padded(self=None,padding=0)->int:
        return os.get_terminal_size()[0] - padding

    def rows_padded(self=None,padding=0)->int:
        return os.get_terminal_size()[1] - padding



