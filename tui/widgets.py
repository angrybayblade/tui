from .__main__ import Geometry,Terminal,Blocks

terminal = Terminal()

class Widget:
    stateful = False
    def __init__(self,parent,name:str="Widget"):
        pass

    def render(self,):
        pass

class Container:
    def __init__(self,):
        pass

    def add(self,):
        pass

class Text(Widget):
    stateful = False
    def __init__(self,parent:Container,value:str,name:str="Text",geometry:dict={}):
        self.value = value
        self.name = name
        self.geometry = Geometry(**geometry)
        self.parent = parent
        self.parent.add(self)

    @property
    def height(self,):
        return int(self.geometry.height * self.parent.height) - 2

    @property
    def width(self,):
        return int(self.geometry.width * self.parent.width) - 2

    @property
    def upper_border(self, ):
        return (
            f"{Blocks.top_left}{Blocks.medium_center}"
            f" {self.name} "
            f"{Blocks.medium_center*(self.width - len(self.name) - 3)}"
            f"{Blocks.top_right}"
        )

    @property
    def lower_border(self,):
        return (
            f"{Blocks.bottom_left}"
            f"{Blocks.medium_center*self.width}"
            f"{Blocks.bottom_right}"
        )

    def add_update_handler(self,func):
        pass

    def update_handler(self,*args,**kwargs):
        pass

    def hollow_line(self,):
        return (
            f"{Blocks.medium_left}"
            f"{' ' * (self.width)}"
            f"{Blocks.medium_right}\n"
        )

    def center_line(self,line):
        whitespace = self.width - len(line)
        left = whitespace // 2
        right = whitespace - left

        return (
            f"{Blocks.medium_right}"
            f"{' '*left}"
            f"{self.value}"
            f"{' '*right}"
            f"{Blocks.medium_right}"
        )

    def render(self,):
        whitespace = self.height - 1
        top = whitespace // 2
        bottom = whitespace - top
        hollow = self.hollow_line()

        return (
            f"{self.upper_border}\n"
            f"{hollow*top}"
            f"{self.center_line(self.value)}\n"
            f"{hollow*bottom}"
            f"{self.lower_border}\n"
        )

class List:
    value = []
    update_handler = None
    stateful = False
    
    def __init__(self,geometry:dict,parent=None,name='List'):
        self.geometry = Geometry(**geometry)
        self.parent = parent
        self.parent.add(self)
        self.name = name

    @property
    def upper_block(self,):
        return (
            f"{Blocks.top_left}"
            f"{Blocks.medium_center*2}"
            f" {self.name} "
            f"{Blocks.medium_center*Terminal.cols_padded(padding=(6+len(self.name)))}"
            f"{Blocks.top_right}"
        ) 

    @property
    def lower_block(self,)->str:
        return (
            f"{Blocks.bottom_left}"
            f"{Blocks.medium_low*Terminal.cols_padded(padding=2)}"
            f"{Blocks.bottom_right}"
        )

    @property
    def hollow_line(self)->str:
        return f"{Blocks.medium_left}{' '*Terminal.cols_padded(padding=2)}{Blocks.medium_right}"

    def center_line(self,line:str)->str:
        white_space = terminal.cols_padded(2) - len(line)
        left = white_space // 2
        right = white_space - left
        return f"{Blocks.medium_left}{' '*left}{line}{' '*right}{Blocks.medium_right}"

    def left_line(self,line:str)->str:
        white_space = terminal.cols_padded(2) - len(line)
        left = white_space // 2
        right = white_space - left
        return f"{Blocks.medium_left}{' '*left}{line}{' '*right}{Blocks.medium_right}"

    def right_line(self,line:str)->str:
        white_space = terminal.cols_padded(2) - len(line)
        left = white_space // 2
        right = white_space - left
        return f"{Blocks.medium_left}{' '*left}{line}{' '*right}{Blocks.medium_right}"

    def render(self,):
        height = int( 
            self.parent.geometry.height * 
            self.geometry.height * 
            Terminal.rows_padded(padding=4) 
        )
        content_height = len(self.value)

        white_space = height - content_height
        up = white_space // 2
        down = white_space - up

        return (
            f"{self.upper_block}"+
            '\n'.join([self.hollow_line]*up) +
            '\n'.join([f"{self.center_line(value)}" for value in self._value]) +
            '\n'.join([self.hollow_line]*down) +
            f"{self.lower_block}"
        ) 