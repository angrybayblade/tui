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
    pre_text = ''
    post_text = ''
    def __init__(self,parent:Container,value:str,name:str="Text",geometry:dict={}):
        self.value = value
        self.name = name
        self.geometry = Geometry(**geometry)
        self.parent = parent
        self.parent.add(self)

    @property
    def height(self,):
        return int(
            (self.geometry.height * self.parent.height) -
            self.parent.padding
        )

    @property
    def width(self,):
        return int(
            (self.geometry.width * self.parent.width) -
            self.parent.padding
        )

    @property
    def line_hollow(self,):
        return (
            self.pre_text + 
            ((self.width)*' ') +
            self.post_text +
            '\n'
        )

    @property
    def line_center(self,):
        whitespace = self.width - len(self.value)
        left = whitespace // 2
        right = whitespace - left
        return (
            self.pre_text +
            ( ' '*left ) +
            ( self.value ) +
            ( ' '*right) +
            self.post_text +
            '\n'
        )

    def render(self,):
        hollow = self.line_hollow
        whitespace = self.height 
        left = whitespace // 2
        right = whitespace - left
        return (
            (hollow*left)+
            self.line_center +
            (hollow*right)
        )

class TextBordered(Widget):
    stateful = False
    pre_text = ''
    post_text = ''
    
    def __init__(self,parent:Container,value:str,name:str="Text",geometry:dict={}):
        self.value = value
        self.name = name
        self.geometry = Geometry(**geometry)
        self.parent = parent
        self.padding = 2
        self.parent.add(self)

    @property
    def height(self,):
        return int(
            (self.geometry.height * self.parent.height) -
            self.parent.padding
        )

    @property
    def width(self,):
        return int(
            (self.geometry.width * self.parent.width) -
            self.parent.padding + len(self.pre_text) + len(self.post_text)
        )

    @property
    def border_top(self,):
        return (
            self.pre_text +
            Blocks.top_left +
            ( (self.width - 2) * Blocks.medium_center) +
            Blocks.top_right +
            self.post_text +
            '\n'
        )

    @property
    def border_bottom(self,):
        return (
            self.pre_text +
            Blocks.bottom_left +
            ( (self.width - 2) * Blocks.medium_center) +
            Blocks.bottom_right +
            self.post_text 
        )

    @property
    def line_center(self,):
        whitespace = self.width - len(self.value) - 2
        left = whitespace // 2
        right = whitespace - left
        return (
            self.pre_text +
            Blocks.medium_right +
            ( ' '*left )+ 
            self.value +
            ( ' '*right )+
            Blocks.medium_left +
            self.post_text +
            '\n'
        )

    @property
    def line_hollow(self,):
        return (
            self.pre_text +
            Blocks.medium_right +
            (' '*(self.width-2)) +
            Blocks.medium_left +
            self.post_text +
            '\n'
        )

    def render(self,)->str:
        whitespace = self.height - 2
        top = whitespace // 2
        bottom = whitespace - top
        hollow = self.line_hollow
        return (
            self.border_top +
            (hollow*top) +
            self.line_center +
            (hollow*bottom) +
            self.border_bottom
        )