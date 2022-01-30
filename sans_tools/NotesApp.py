from typing import List, Dict, Any
import sqlite3
import logging
import os
import re

class SansNotesApp(object):
    APP_FILES = 'SansNotesAppFiles'
    APP_DATABASE_FILES = os.path.join(APP_FILES,'NotesAppDbFiles')
    CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS {table_name_field}
            (
                subject VARCHAR(50),
                topic VARCHAR(50),
                book  VARCHAR(3),
                page  VARCHAR(3),
                notes VARCHAR(1000)
            )
        """
    DROP_TABLE = """
        DROP TABLE {table_name_field};
    """

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
        db_path = os.path.join(SansNotesApp.APP_DATABASE_FILES,'{}.db'.format(SansNotesApp.check_char_string(db_name_fmt)))
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

    def check_db_file(self) -> bool:
        return os.path.exists(self.__db_name)

    def create_new_database(self) -> bool:
        if self.check_db_file():
            print(f'{os.path.basename(self.__db_name)} already exists.')
            return False
        self.db_connect()
        print(f'Created {os.path.basename(self.__db_name)}')
        return True
    
    def show_all_tables(self):
        self.get_cursor()
        self.__cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(self.__cur.fetchall())
    
    def committ_and_close(self) -> bool:
        self.__con.commit()
        self.__con.close()
        return True
    
    def drop_table(self):
        pass 

    def create_table(self, table_name) -> bool:
        self.get_cursor()
        self.__cur.execute(
            SansNotesApp.CREATE_TABLE.format(table_name_field=SansNotesApp.check_char_string(table_name))
            )
        return True

    def insert_data(self,in_data):
        pass 

    def drop_table(self):

        pass

    def delete_data(self,del_data):
        pass

    def search_data(self,s_data):
        pass

    @staticmethod
    def check_char_string(alpha_string) -> str:
        return ''.join(re.findall('[\w+\-0-9]',alpha_string))
   

if __name__ == "__main__":
    notes = SansNotesApp()
    notes.database_name = 'test'
    notes.db_connect()
    notes.create_table('my_test_table')
    notes.show_all_tables()
    notes.committ_and_close()