from concurrent.futures import ThreadPoolExecutor
from .__main__ import Geometry,Terminal,Blocks

terminal = Terminal()


def render(obj):
    return getattr(obj,'render')()

class HBox(object):
    stateful = False
    pre_text = ''
    post_text = ''
    padding = 0
    def __init__(self,parent,geometry:dict={'height':1.,'width':1.},widgets:list=[],name:str='HBox'):
        self.widgets = widgets
        self.geometry = Geometry(**geometry)
        self.parent = parent
        self.name = name
        self.parent.add(self)

    def add(self,widget):
        self.widgets.append(widget)

    @property
    def height(self,):
        return int(
            (self.geometry.height * self.parent.height ) -
            self.parent.padding
        )

    @property
    def width(self,):
        return int(
            (self.geometry.width * self.parent.width ) -
            self.parent.padding
        )

    def render(self,):
        with ThreadPoolExecutor(max_workers=(len(self.widgets))) as executer:
            rows = executer.map(render,self.widgets)
            rows = zip(*[ row.split('\n') for row in rows ])
            rows = "\n".join([ " ".join(row) for row in rows ])

        return rows

class HBoxBordered(object):
    stateful = False
    pre_text = ''
    post_text = ''
    padding = 2
    def __init__(self,parent,geometry:dict={'height':1.,'width':1.},widgets:list=[],name:str='HBox'):
        self.widgets = widgets
        self.geometry = Geometry(**geometry)
        self.parent = parent
        self.name = name
        self.parent.add(self)

    def add(self,widget):
        if len(self.widgets) == 0:
            widget.pre_text = Blocks.medium_right
        else:
            self.widgets[-1].post_text = ''

        widget.post_text = Blocks.medium_left
        self.widgets.append(widget)

    @property
    def height(self,):
        return int(
            (self.geometry.height * self.parent.height ) -
            self.parent.padding
        )
    
    @property
    def width(self,):
        return int(
            (self.geometry.width * self.parent.width ) -
            self.parent.padding
        )

    @property
    def border_top(self,):
        return (
            self.pre_text +
            Blocks.top_left  +
            Blocks.medium_center +
            f" {self.name} " +
            ( Blocks.medium_center * (self.width - len(self.name) - 5) ) + 
            Blocks.top_right +
            self.post_text
        )
    
    @property
    def border_bottom(self,):
        return (
            self.pre_text +
            Blocks.bottom_left  +
            ((self.width - 2) * Blocks.medium_center) +
            Blocks.bottom_right +
            self.post_text
        )

    def render(self,):
        with ThreadPoolExecutor(max_workers=(len(self.widgets))) as executer:
            rows = executer.map(render,self.widgets)
            rows = zip(*[ row.split('\n') for row in rows ])
            rows = "\n".join([ " ".join(row) for row in rows ])

        return (
            self.border_top +
            rows +
            self.border_bottom
        )

class VBox(object):
    stateful = False
    pre_text = ''
    post_text = ''
    def __init__(self,parent,geometry:dict={'height':1.,'width':1.},widgets:list=[],name:str='HBox'):
        self.widgets = widgets
        self.geometry = Geometry(**geometry)
        self.parent = parent
        self.name = name
        self.padding = 0
        self.parent.add(self)

    def add(self,widget):
        self.widgets.append(widget)

    @property
    def height(self,):
        return int(
            (self.geometry.height * self.parent.height) -
            self.parent.padding -
            2
        )

    @property
    def width(self,):
        return int(
            (self.geometry.width * self.parent.width) -
            self.parent.padding
        )

    def render(self,)->str:
        with ThreadPoolExecutor(max_workers=(len(self.widgets))) as executer:
            rows = executer.map(render,self.widgets)
            rows = ''.join(rows)

        return rows

class VBoxBordered(object):
    stateful = False
    pre_text = ''
    post_text = ''
    def __init__(self,parent,geometry:dict={'height':1.,'width':1.},widgets:list=[],name:str='HBox'):
        self.widgets = widgets
        self.geometry = Geometry(**geometry)
        self.parent = parent
        self.name = name
        self.padding = 2
        self.parent.add(self)

    def add(self,widget):
        widget.pre_text = Blocks.medium_right
        widget.post_text = Blocks.medium_left
        self.widgets.append(widget)

    
    @property
    def height(self,):
        return (
            int(self.geometry.height * self.parent.height) -
            self.parent.padding
        )
    
    @property
    def width(self,):
        return (
            int(self.geometry.width * self.parent.width) - 
            self.parent.padding
        )

    @property
    def border_top(self,)->str:
        return (
            self.pre_text + 
            Blocks.top_left +
            Blocks.medium_center +
            f" {self.name} " + 
            ((self.width - len(self.name)-5) * Blocks.medium_center) +
            Blocks.top_right +
            self.post_text
        )

    @property
    def border_bottom(self,):
        return (
            self.pre_text +
            Blocks.bottom_left +
            ((self.width-2) * Blocks.medium_center) +
            Blocks.bottom_right +
            self.post_text
        )

    def render(self,)->str:
        with ThreadPoolExecutor(max_workers=(len(self.widgets))) as executer:
            rows = executer.map(render,self.widgets)
            rows = f''.join(rows)

        return (
            self.border_top +
            rows +
            '\n'+
            self.border_bottom
        )

class Grid(object):
    def __init__(self):
        pass

class FlexBox(object):
    def __init__(self,):
        pass