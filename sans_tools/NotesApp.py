from typing import List, Dict, Any
import sqlite3
import logging
import os

class SansNotesApp(object):
    APP_FILES = 'SansNotesAppFiles'
    APP_DATABASE_FILES = os.path.join(APP_FILES,'NotesAppDbFiles')

    def __init__(self):  
        if not os.path.exists(SansNotesApp.APP_FILES):
             os.mkdir(SansNotesApp.APP_FILES)

        logging.basicConfig(
            filename=os.path.join(SansNotesApp.APP_FILES,'NotesAppDb.log'), 
            level=logging.DEBUG,
            filemode='w'
            )
        
        logging.debug(SansNotesApp.APP_FILES)
        if not os.path.exists(SansNotesApp.APP_DATABASE_FILES):
            os.mkdir(SansNotesApp.APP_DATABASE_FILES)
            logging.debug(os.listdir(SansNotesApp.APP_FILES))

    def __format_db_name(self,db_name_fmt:str):
        db_path = os.path.join(SansNotesApp.APP_DATABASE_FILES,'{}.db'.format(db_name_fmt))
        logging.debug(db_path)
        return db_path

    @property
    def database_name(self) -> str:
        return self.__db_name

    @database_name.setter
    def database_name(self,db_name:str) -> str:
        """
        Enter a string with no spaces or special characters
        as the database name
        """
        self.__db_name = self.__format_db_name(db_name)
        logging.debug(self.__db_name)
    
    def db_connect(self):
        self.__con = sqlite3.connect(self.__db_name)
        logging.debug(self.__con)
        return self.__con
    
    def get_cursor(self):
        self.__cur = self.__con.cursor()
        logging.debug(self.__cur)
        return self.__cur 

    def create_new_database(self):
        pass
    
    def delete_database(self):
        pass 

    def insert_data(self,in_data):
        pass 

    def delete_data(self,del_data):
        pass

    def search_data(self,s_data):
        pass

    def show_all_databases(self):
        pass

if __name__ == "__main__":
    notes = SansNotesApp()
    notes.database_name = 'test'