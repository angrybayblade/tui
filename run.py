import time
import sys
import os
import random

import numpy as np

from tui.utils import Blocks

from concurrent.futures import ThreadPoolExecutor
from threading import Thread

i = 0

class Terminal:
    _height = 0
    _width = 0
    def __init__(self,):
        self._get = os.get_terminal_size
        self._width,self._height = self._get()

    def update(self,):
        self._width,self._height = self._get()

    @property
    def width(self,)->float:
        return self._width

    @property
    def height(self,)->float:
        return self._height

class Style(object):
    def __init__(self,
        height:float=1.0,
        width:float=1.0 ):

        self.height = height
        self.width = width
        
_default_style = Style(
    height=1.0,
    width=1.0
)

class Text(object):
    state:str = 'TextBox'

    # cached
    _height = 0
    _width = 0
    _screen = np.array([])
    
    def __init__(
            self,
            parent,
            state:str='TextBox',
            style:Style=_default_style):

        self.state = state
        self.style = style
        self.parent = parent

        self.parent.add(self)
        self.generate_cache()
    
    @property
    def height(self,):
        return self._height
    
    @property
    def width(self,):
        return self._width

    def generate_cache(self,):
        self._height = int(self.style.height * self.parent.height)
        self._width = int(self.style.width * self.parent.width)

        self._screen[:,[0,-1]] = Blocks.thin.vr
        self._screen[[0,-1],:] = Blocks.thin.hr

        self._screen[0,0] = Blocks.thin.top_left
        self._screen[0,-1] = Blocks.thin.top_right
        self._screen[-1,0] = Blocks.thin.bottom_left
        self._screen[-1,-1] = Blocks.thin.bottom_right

        content = np.array(list(self.state))
    
        t = (self._height // 2)
        l = (self._width // 2) - len(content) // 2 

        self._screen[t:t+1,l:l+len(content)] = content

    def update_state(self,):
        pass

    def render(self,):
        pass

class Screen(object):
    children = []

    # cached
    _terminal = Terminal()
    _height = 0
    _width = 0

    def __init__(self,
            style:Style = _default_style
        ):
        
        self.style = style
        self.generate_cache()

        os.system("cls||clear")

    def generate_cache(self,):
        self._height = int(self.style.height * self._terminal.height)
        self._width = int(self.style.width * self._terminal.width)

        self._screen = np.zeros((self._height,self._width),dtype=str)
        self._screen[:,:] = ' '

    @property
    def height(self,):
        return self._height
    
    @property
    def width(self,):
        return self._width

    def add(self,child):
        child._screen = self._screen
        self.children.append(child)

    def __str__(self,):
        pass

    def __repr__(self,):
        pass

    def render(self,):
        while True:
            sys.stdout.write(u"\u001b[{}D".format(self._width)) 
            sys.stdout.write(u"\u001b[{}A".format(self._height))         
            sys.stdout.write('\n'.join(np.apply_along_axis(lambda x:''.join(x),0,self._screen.T)))
            sys.stdout.flush()
            time.sleep(1)

def main():
    screen = Screen(style=Style(height=1.,width=1.))

    t1 = Text(screen,state='Count',style=Style(height=1.,width=1.))

    screen.render()

if __name__ == "__main__":
    main()

# os.system('cls||clear')
# while True:
#     col,row = os.get_terminal_size()
#     count = row
#     text = f'hello world {i}'
    
#     w = col - len(text) - 2
#     l = w // 2
#     r = w - l

#     h = Blocks.thin.vr + (' '*(col-2)) + Blocks.thin.vr
    
#     w = row - 3
#     t = w // 2
#     b = w - t

#     screen = [
#         Blocks.thin.top_left + Blocks.thin.hr*(col-2) + Blocks.thin.top_right,
#         *([h]*t),
#         Blocks.thin.vr +' '*l + text + ' '*r + Blocks.thin.vr,
#         *([h]*b),
#         Blocks.thin.bottom_left + Blocks.thin.hr*(col-2) + Blocks.thin.bottom_right
#     ]

#     sys.stdout.write(u"\u001b[{col}D".format(col=col)) 
#     sys.stdout.write(u"\u001b[{row}A".format(row=row))         
#     sys.stdout.write('\n'.join(screen))
#     sys.stdout.flush()

#     i += 1
#     time.sleep(0.1)