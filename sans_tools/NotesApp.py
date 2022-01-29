from typing import List, Dict, Any
import sqlite3
import logging
import os


class SansNotesApp(object):

    def __init__(self):
        self.__log_path = 'SansNotesAppFiles'
        self.__folder = os.path.join(self.__log_path,'NotesAppDbFiles')
        
        
        if not os.path.exists(self.__log_path):
             os.mkdir(self.__log_path)

        logging.basicConfig(
            filename=os.path.join(self.__log_path,'NotesAppDb.log'), 
            level=logging.DEBUG,
            filemode='w'
            )
        
        logging.debug(self.__log_path)
        if not os.path.exists(self.__folder):
            os.mkdir(self.__folder)
            logging.debug(os.listdir(self.__log_path))

    def __format_db_name(self,db_name_fmt:str):
        db_path = os.path.join(self.__folder,'{}.db'.format(db_name_fmt))
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
    print(notes.database_name)