from numpy import void
from NotesApp import SansNotesApp
import pandas as pd
import os 


class AppFileHandler(SansNotesApp):
    def __init__(self):
        super().__init__()

    @property
    def set_ingest_file(self) -> str:
        #getter
        return self.ingest_file
        
    @set_ingest_file.setter
    def set_ingest_file(self,file_name: str) -> void:
        #setter
        self.ingest_file = file_name
    
    def noralize_columns(self,**kwargs):
        column_mappings = kwargs
        

        
        

if __name__ == '__main__':
    app = AppFileHandler()