from .__main__ import Blocks

class Style:
    height:int = 0
    width:int = 0

    def __init__(self,**kwargs):
        for key,val in kwargs.items():
            self.__dict__[key] = val

class Parent:
    height = 0
    width = 0

class Widget:
    stateful = False
    pre_text = ''
    post_text = ''
    name = ''
    padding = 0

    # Cached
    _height = 0
    _width = 0

    def __init__(self,
            parent:Parent,
            style:Style,
            state=False
        ):
        self.parent = parent
        self.style = style
        self.state = state
        self.stateful = bool(state)
        self.parent.add(self)

    def set_padding(self,pre_text,post_text):
        self.pre_text = pre_text
        self.post_text = post_text
        self.padding = len(pre_text) + len(post_text)
    
    def cache_geometry(self,):
        pass

    def cache_render(self,):
        pass

    def render(self,)->str:
        pass

class WidgetBordered:
    stateful = False
    pre_text = ''
    post_text = ''
    name = ''
    padding = 0

    # Cached
    _height = 0
    _width = 0

    def __init__(self,
            parent:Parent,
            style:Style,
            state=False
        ):
        self.parent = parent
        self.style = style
        self.state = state
        self.stateful = bool(state)
        self.parent.add(self)

    def set_padding(self,pre_text,post_text):
        self.pre_text = pre_text
        self.post_text = post_text
        self.padding = len(pre_text) + len(post_text)
    
    def cache_geometry(self,):
        pass

    def cache_render(self,):
        pass

    def render(self,)->str:
        pass

class Line(Widget):
    
    def blank(self,):
        return self._width * Blocks.whitespace + '\n'

    def hcenter_text(self,text):
        whitespace = self._width - len(self.state)
        left = whitespace // 2
        right = whitespace - left
        return left*Blocks.whitespace + text + right*Blocks.whitespace + '\n' 

    def vcenter_text(self,text:str,blank:str):
        whitespace = self._height - len(text.split("\n"))
        top = whitespace // 2
        bottom = whitespace - top
        return blank*top + text + bottom*blank + '\n'

class LineBordered(WidgetBordered):
    
    def blank(self,):
        return (
            Blocks.medium_right + 
            ((self._width-2) * Blocks.whitespace) + 
            Blocks.medium_left + 
            '\n'
        )

    def hcenter_text(self,text):
        whitespace = self._width - len(self.state) - 2
        left = whitespace // 2
        right = whitespace - left
        return (
            Blocks.medium_right +
            left*Blocks.whitespace + 
            text + 
            right*Blocks.whitespace + 
            Blocks.medium_left +
            '\n'
        ) 

    def vcenter_text(self,text:str,blank:str):
        whitespace = self._height - len(text.split("\n")) - 2
        top = whitespace // 2
        bottom = whitespace - top
        return blank*top + text + bottom*blank + '\n'

    def border_top(self,):
        return (
            Blocks.top_left +
            Blocks.medium_center +
            self.name +
            (self._width - len(self.name) - 3) * Blocks.medium_center +
            Blocks.top_right + 
            '\n'
        )
    
    def border_bottom(self,):
        return (
            Blocks.bottom_left +
            (self._width - 2) * Blocks.medium_center +
            Blocks.bottom_right 
        )

class Text(Widget):
    def cache_geometry(self,):
        self._height = int(self.parent._height * self.style.height)
        self._width = int(self.parent._width * self.style.width) - self.padding

    def cache_render(self,):
        self._content = Line.hcenter_text(self,self.state)
        self._content = Line.vcenter_text(self,self._content,Line.blank(self))

    def render(self,executer):
        return self._content

class TextBordered(WidgetBordered):
    def cache_geometry(self,):
        self._height = int(self.parent._height * self.style.height)
        self._width = int(self.parent._width * self.style.width) - self.padding

    def cache_render(self,):
        self._content = LineBordered.hcenter_text(self,self.state)
        self._content = Line.vcenter_text(self,self._content,LineBordered.blank(self))
        self._content = (
            LineBordered.border_top(self) +
            self._content[:-1] + # Skip newline character
            LineBordered.border_bottom(self) +
            '\n'
        )

    def render(self,executer):
        return self._content