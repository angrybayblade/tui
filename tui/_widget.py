from typing import Union

class Widget:
    name = 'Widget'
    pre_text = ''
    post_text = ''
    
    # Cached 
    _height = 0
    _width = 0
    _content = 0

    def __init__(
        self,
        parent:Union[int,str],
        style
        ):
        self.style = style
        self.parent = parent
        self.parent.add(parent)

class WidgetBordered:
    pass