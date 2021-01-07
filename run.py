import time
import sys
import os
import random

import numpy as np

from tui.utils import Blocks
from concurrent.futures import ThreadPoolExecutor

i = 0

class Terminal:
    _height = 0
    _width = 0
    def __init__(self,):
        self._get = os.get_terminal_size
        self._width,self._height = self._get()

    def update(self,):
        self._width,self._height = self._get()
        return self._width,self._height

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
    update_func:callable = lambda *x:None 

    # cached
    _height = 0
    _width = 0
    _xmin = 0
    _ymin = 0
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
        self.parent.update_cursor(self._height,self._width)
    
    @property
    def height(self,):
        return self._height
    
    @property
    def width(self,):
        return self._width

    def generate_cache(self,):
        self._height = int(self.style.height * self.parent.height) 
        self._width = int(self.style.width * self.parent.width) 

        self._xmax = self._xmin + self._width 
        self._ymax = self._ymin + self._height 

        self._content = np.zeros(shape=(self._height,self._width),dtype=str)
        self._content[:,:] = ' '
        self._content[:,[0,-1]] = Blocks.thin.vr
        self._content[[0,-1],:] = Blocks.thin.hr

        self._content[0,0] = Blocks.thin.top_left
        self._content[0,-1] = Blocks.thin.top_right
        self._content[-1,0] = Blocks.thin.bottom_left
        self._content[-1,-1] = Blocks.thin.bottom_right

        self.render()

    def add_update_callback(self,func):
        self.update_func = func
        self.parent.update_functions.append(self.update)

    def update_callback(self,):
        return self.add_update_callback

    def update(self,):
        self.update_func(self)

    def render(self,):
        whitespace = self._width - len(self.state)
        left = whitespace // 2
        right = whitespace - left

        whitespace  = self._height - 1
        top = whitespace // 2

        self._content[top:top+1,left:left+len(self.state)] = np.array(list(self.state))
        self._content[top:top+1,1:left] = ' '
        self._content[top:top+1,left+len(self.state):-1] = ' '
        
        self._screen[self._ymin:self._ymax,self._xmin:self._xmax] = self._content[:,:]

class HBox(object):
    state:str = 'HorizontalBox'
    update_func:callable = lambda *x:None 

    # cached
    _height = 0
    _width = 0
    _xmin = 0
    _ymin = 0
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
        self.parent.update_cursor(self._height,self._width)
    
    @property
    def height(self,):
        return self._height
    
    @property
    def width(self,):
        return self._width

    def generate_cache(self,):
        self._height = int(self.style.height * self.parent.height) 
        self._width = int(self.style.width * self.parent.width) 

        self._xmax = self._xmin + self._width 
        self._ymax = self._ymin + self._height 

        self._content = np.zeros(shape=(self._height,self._width),dtype=str)
        self._content[:,:] = ' '
        self._content[:,[0,-1]] = Blocks.thin.vr
        self._content[[0,-1],:] = Blocks.thin.hr

        self._content[0,0] = Blocks.thin.top_left
        self._content[0,-1] = Blocks.thin.top_right
        self._content[-1,0] = Blocks.thin.bottom_left
        self._content[-1,-1] = Blocks.thin.bottom_right

        self.render()

    def add_update_callback(self,func):
        self.update_func = func
        self.parent.update_functions.append(self.update)

    def update_callback(self,):
        return self.add_update_callback

    def update(self,):
        self.update_func(self)

    def render(self,):
        whitespace = self._width - len(self.state)
        left = whitespace // 2
        right = whitespace - left

        whitespace  = self._height - 1
        top = whitespace // 2

        self._content[top:top+1,left:left+len(self.state)] = np.array(list(self.state))
        self._content[top:top+1,1:left] = ' '
        self._content[top:top+1,left+len(self.state):-1] = ' '
        
        self._screen[self._ymin:self._ymax,self._xmin:self._xmax] = self._content[:,:]

class Screen(object):
    children = []
    update_functions = []

    # cached
    _terminal = Terminal()
    _height = 0
    _width = 0
    _xmin = 0
    _ymin = 0

    _cursor_x = 0
    _cursor_y = 0

    def __init__(self,
            style:Style = _default_style
        ):
        
        self.style = style
        self.generate_cache()

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

    def add(self,child:Text):
        child._screen = self._screen
        child._xmin = self._cursor_x
        child._ymin = self._cursor_y
        self.children.append(child)

    def update_cursor(self,ch,cw):
        self._cursor_y += ch

    def __str__(self,):
        pass

    def __repr__(self,):
        pass

    def run_update_func(self,func):
        return func()
        
    def render(self,):
        while True:
            sys.stdout.write(u"\u001b[0;0H")         
            sys.stdout.write('\r\n'.join(np.apply_along_axis(lambda x:''.join(x),0,self._screen.T)))
            sys.stdout.flush()

    def loop(self,):
        self.update_functions.append(self.render)
        with ThreadPoolExecutor(max_workers=int(len(self.update_functions)*1.5)) as executer:
            out = list(executer.map(self.run_update_func,self.update_functions))

def update_texts(self:Text,):
    i = np.random.randint(-8,8)
    d = np.random.randint(1,100) / 60
    while True:
        self.state = f'Count {i}'
        self.render()
        time.sleep(d)
        i += 1
    return 1

screen = Screen(style=Style(height=1.,width=1.))

t1 = Text(screen,state='Count will start',style=Style(height=1/3,width=1))
t2 = Text(screen,state='Count will start',style=Style(height=1/3,width=1))
t3 = Text(screen,state='Count will start',style=Style(height=1/3,width=1))

t1.add_update_callback(update_texts)
t2.add_update_callback(update_texts)
t3.add_update_callback(update_texts)


def main():
    os.system("cls||clear")
    screen.loop()
   
if __name__ == "__main__":
    main()

