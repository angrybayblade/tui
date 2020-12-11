import os
import sys
import time
import keyboard

from concurrent.futures import ThreadPoolExecutor

from tui import Terminal
from tui.widgets import Text,Style,Widget,TextBordered
from tui.box import Hbox

terminal = Terminal()

class Screen:
    widget = []
    stateful_widgets = []
    padding = 0
    def __init__(self,style:Style):
        self.style = style

    def add(self,widget:Widget):
        widget.cache_geometry()
        widget.cache_render()
        self.widget.append(widget) 

    def _render(self,obj):
        return obj.render(self._executer)

    @property
    def _height(self,):
        return int(terminal.rows() * self.style.height)

    @property
    def _width(self,):
        return int(terminal.cols() * self.style.width)

    def render(self,):
        start = time.time()
        with ThreadPoolExecutor(max_workers=128) as executer:
            self._executer = executer
            output = executer.map(self._render,self.widget)
            output = '\r'.join(output)[:-1]
            os.system("clear||cls")
            sys.stdout.write(output)
            t = time.time() - start
            sys.stdout.write(f"\n{t:.6f} Sec | {(1//t)} FPS")
            sys.stdout.flush()

class EventHandler:
    callback  = None
    screen  = None
    def __init__(self,):
        pass
    def add_listner(self,callback):
        keyboard.on_release(callback)

event_handler = EventHandler()
screen = Screen(
    style=Style(
        height=.975,
        width=1.0
    )
)

b1 = Hbox(
    parent=screen,
)


t1 = TextBordered(
    parent=b1,
    style=Style(
        height=1.0/2,
        width=1.0
    ),
    state='Hello'
)

# t2 = TextBordered(
#     parent=b1,
#     style=Style(
#         height=1.0/2,
#         width=1.0
#     ),
#     state='World'
# )

def callback(key:keyboard.KeyboardEvent):
    if key.name == "q":
        os.system("cls||clear")
        exit(0)
    screen.render()

def main():
    screen.render()
    event_handler.add_listner(callback)
    while True:
        time.sleep(1)
    
if __name__ == "__main__":
    main()