from .__main__ import Terminal,Blocks
from concurrent.futures import ThreadPoolExecutor

from .widgets import Widget,Style,LineBordered,Line

class Box(object):
    stateful = False
    pre_text = ''
    post_text = ''
    padding = 0
    children = []

    ## Cache
    _height = 0
    _width = 0
    _executer = None
    _content = ''

    def __init__(self,
        parent,
        style=Style(
            height=1.0,
            width=1.0
        ),
        children:list=[],
        name:str='HBox'
    ):
        self.children = children
        self.parent = parent
        self.name = name
        self.style = style
        self.parent.add(self)

    def add(self,child:Widget):
        child.cache_geometry()
        child.cache_render()
        self.children.append(child)

    def _render(self,obj,):
        return obj.render(self._executer)

class Hbox(Box):
    def cache_geometry(self,):
        self._height = int(self.parent._height * self.style.height)
        self._width = int(self.parent._width * self.style.width) - self.padding

    def cache_render(self,):
        pass

    def render(self,executer):
        return f"{self._height},{self._width}"
