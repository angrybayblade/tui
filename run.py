import os
import sys
import time
import keyboard

from concurrent.futures import ThreadPoolExecutor

from tui._utils import Blocks

class EventHandler:
    callback  = None
    screen  = None
    def __init__(self,):
        pass
    def add_listner(self,callback):
        keyboard.on_release(callback)

event_handler = EventHandler()

def main():
    pass
    
if __name__ == "__main__":
    print (Blocks.Medium.line)