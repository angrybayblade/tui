from .__main__ import Geometry,Terminal,Blocks

terminal = Terminal()

class HBox(object):
    stateful = False
    def __init__(self,parent,geometry:dict={'height':1.,'width':1.},widgets:list=[],name:str='HBox'):
        self.widgets = widgets
        self.geometry = Geometry(**geometry)
        self.parent = parent
        self.name = name
        self.parent.add(self)

    def add(self,widget):
        self.widgets.append(widget)

    @property
    def height(self,)->int:
        return int(self.parent.height * self.geometry.height) - 1

    @property
    def width(self,)->int:
        return int(self.parent.width * self.geometry.width)

    @property
    def border_top(self,)->str:
        return (
            f"{Blocks.top_left}{Blocks.medium_center}"
            f" {self.name} "
            f"{Blocks.medium_center*(self.width - len(self.name) - 3)}"
            f"{Blocks.top_right}"
        )

    @property
    def border_bottom(self,)->str:
        return (
            f"{Blocks.bottom_left}"
            f"{Blocks.medium_center*(self.width)}"
            f"{Blocks.bottom_right}"
        )

    def center_line(self,line:str)->str:
        line = f" ".join(line)
        whitespace = self.width - len(line)
        left = whitespace // 2
        right = whitespace - left
        return (
            Blocks.medium_right +
            " " * left +
            line +
            " " * right +
            Blocks.medium_right 
        )

    def hollow_line(self,):
        return (
            f"{Blocks.medium_left}"
            f"{ ' ' * self.width}"
            f"{Blocks.medium_right}"
        )

    def render(self,):
        rows = [widget.render().split("\n") for widget in self.widgets]
        rows = "\n".join([self.center_line(row) for row in zip(*rows)])

        return (
            f"{self.border_top}\n" 
            f"{rows}\n"
            f"{self.border_bottom}"
        )

class VBox(object):
    stateful = False
    def __init__(self,parent,geometry:dict={'height':1.,'width':1.},widgets:list=[]):
        self.widgets = widgets
        self.geometry = Geometry(**geometry)
        parent.add(self)

    def add(self,widget):
        self.widgets.append(widget)

    def render(self,):
        return "\n".join([widget.render() for widget in self.widgets])
        
class Grid(object):
    def __init__(self):
        pass

class FlexBox(object):
    def __init__(self,):
        pass