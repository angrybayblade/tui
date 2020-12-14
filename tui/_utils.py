from ._imports import os

class Blocks:
    whitespace = ''
    tabspace = '\t'
    newline = '\n'

    class thin:
        top_left = '┌'
        top_right = '┐'
        bottom_left = '└'
        bottom_right = '┘'
        hr = '─'
        vr = '│'

    class thick:
        top_left = '┏'
        top_right = '┓'
        bottom_left = '┗'
        bottom_right = '┛'
        hr = '━'
        vr = '┃'

    class outlined:
        top_left = '╔'
        top_right = '╗'
        bottom_left = '╚'
        bottom_right = '╝'
        hr = '═'
        vr = '║'

    class rounded:
        top_left = '╭'
        top_right = '╮'	
        bottom_right = '╯'
        bottom_left = '╰'
        hr = '─'
        vr = '│'
