from NotesApp import SansNotesApp
import pandas as pd
import os 


class AppFileHandler(SansNotesApp):
    def __init__(self):
        super().__init__()
        

if __name__ == '__main__':
    app = AppFileHandler()