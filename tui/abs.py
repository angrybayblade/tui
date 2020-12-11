from .__main__ import Terminal,Blocks

class Style:
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
        return f"""Style(\n{prop}\n)"""

    def __repr__(self):
        return str(self)

