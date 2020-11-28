import os
import sys
import time

from pynput import keyboard,mouse

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

terminal = Terminal()

class Blocks:
    upper_block = '▀'
    lower_block = '▄'
    full_block = '█'

    upper_one_eighth = '▔'
    lower_one_eighth = '▁'
    left_one_eighth  = '▏'
    right_one_eighth  = '▕'


class EventHandler:
    callback  = lambda *x:0
    screen  = lambda *x:0
    def __init__(self,):
        pass

    def on_press(self,key):
        try:
            pass
        except AttributeError:
            pass

    def on_release(self,key):
        self.callback(key)
        if key == keyboard.Key.esc:
            return False

    def add_listner(self,callback):
        self.callback = callback
        with keyboard.Listener(on_press=self.on_press,on_release=self.on_release) as listener:
            listener.join()
            try:
                listener.start()
            except RuntimeError:
                self.add_listner(callback)

class Widget:
    geometry = None
    parent = None
    _value = None
    _update_handler = None
    _statefull = None
    def __init__(self):
        pass

class Geometry:
    height = None
    width = None
    def __init__(self,**kwargs):
        for key,value in kwargs.items():
            self.__dict__[key] = value

    def __setitem__(self,key,value):
        self.__dict__[key] = value

    def __getitem__(self,key):
        return self.__dict__[key]

    def __str__(self,):
        prop = '\n'.join([ f'   {key}:{value}' for key,value in self.__dict__.items() ])
        return f"""Geometry(
{prop}
)"""

    def __repr__(self):
        return str(self)

class List:
    _value = []
    _update_handler = lambda *x:x
    _statefull = False
    def __init__(self,geometry:dict,parent=None):
        self.geometry = Geometry(**geometry)
        self.parent = parent
        self.parent.add(self)

    @property
    def _upper_block(self,):
        return f"{Blocks.full_block}{Blocks.upper_block*Terminal.cols_padded(padding=2)}{Blocks.full_block}" 

    @property
    def _lower_block(self,):
        return f"{Blocks.full_block}{Blocks.lower_block*Terminal.cols_padded(padding=2)}{Blocks.full_block}"

    @property
    def _hollow_line(self):
        return f"{Blocks.full_block}{' '*Terminal.cols_padded(padding=2)}{Blocks.full_block}"

    def center_line(self,line):
        white_space = terminal.cols_padded(2) - len(line)
        left = white_space // 2
        right = white_space - left
        return f"{Blocks.full_block}{' '*left}{line}{' '*right}{Blocks.full_block}"

    def add_update_handler(self,func):
        self._update_handler = func

    def update_handler(self,name):
        self._statefull = True
        self.parent._statefull_widgets.append(self)
        return self.add_update_handler

    def update(self,key,*args,**kwargs):
        self._update_handler(self,key)

    def render(self,):
        height = int( self.parent.geometry.height * self.geometry.height * Terminal.rows_padded(padding=2) )
        content_height = len(self._value)

        white_space = height - content_height
        up = white_space // 2
        down = white_space - up

        return (
            f"{self._upper_block}"+
            '\n'.join([self._hollow_line]*up) +
            '\n'.join([f"{self.center_line(value)}" for value in self._value]) +
            '\n'.join([self._hollow_line]*down) +
            f"{self._lower_block}"
        ) 

class Screen:
    _widget = []
    _statefull_widgets = []
    def __init__(self,geometry:dict):
        self.geometry = Geometry(**geometry)

    def add(self,widget:Widget):
        widget.parent = self
        if widget._statefull:
            self._statefull_widgets.append(widget)
        self._widget.append(widget) 

    def render(self,):
        output = '\n'.join([widget.render() for widget in self._widget])
        # sys.stdout.write("\x1b[2J\x1b[H")    
        os.system("clear||cls")
        sys.stdout.write(output)
        sys.stdout.flush()

event_handler = EventHandler()
screen = Screen(geometry={
    'height':1.0,
    'width':1.0
})

box = List(geometry={
    'height':0.4,
    'width':1.0
},parent=screen)

box._value = [
    'This Is An Example',
    f'Press Any Key'
]

@box.update_handler(name='Box_1_event_handler')
def update_box_value(box:List,key:keyboard.Key):
    box._value = [
        'This Is An Example',
        f'You pressed : {key}'
    ]

def callback(key:keyboard.Key):
    for widget in screen._statefull_widgets:
        widget.update(key)
    screen.render()

def main():
    screen.render()
    event_handler.add_listner(
        callback
    )
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()