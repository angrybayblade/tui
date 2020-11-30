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

class Geometry:
    height = None
    width = None
    border = False
    def __init__(self,**kwargs):
        for key,value in kwargs.items():
            self.__dict__[key] = value

    def __setitem__(self,key,value):
        self.__dict__[key] = value

    def __getitem__(self,key):
        return self.__dict__[key]

    def __str__(self,):
        prop = '\n'.join([ f'   {key}:{value}' for key,value in self.__dict__.items() ])
        return f"""Geometry(\n{prop}\n)"""

    def __repr__(self):
        return str(self)


