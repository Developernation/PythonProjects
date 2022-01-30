from typing import List, Dict, Any
from itertools import chain
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

    INSERT = """
        INSERT INTO {table_name_field} 
            (
                subject, 
                topic, 
                book, 
                page, 
                notes
            )
        VALUES 
            (
                {subject_},
                {topic_}, 
                {book_},
                {page_},
                {notes_}
            );
    """

    SEARCH = """
        SELECT 
            *
        FROM 
            {table_name_field}
        WHERE
            {col_name}   

    
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
    
    def db_connect_and_cursor(self):
        """
        This function will create a database if it doesn't exist.
        """
        self.__con = sqlite3.connect(self.__db_name)
        logging.debug(self.__con)
        self.__cur = self.__con.cursor()
        logging.debug(self.__cur)
        return self.__con

    def check_db_file(self) -> bool:
        return os.path.exists(self.__db_name)
    
    def show_all_tables(self):
        self.__cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables_normalized = list(chain.from_iterable(self.__cur.fetchall()))
        print(tables_normalized)
        return tables_normalized
    
    def committ_and_close(self) -> bool:
        self.__con.commit()
        self.__con.close()
        return True
    
    def drop_table(self, table_to_drop) -> bool:
        clean_drp_tbl_nm = SansNotesApp.check_char_string(table_to_drop)
        self.__cur.execute(
            SansNotesApp.DROP_TABLE.format(table_name_field=clean_drp_tbl_nm)
        )
        success = clean_drp_tbl_nm not in self.show_all_tables()
        logging.debug(f'{SansNotesApp.check_char_string(clean_drp_tbl_nm)} dropped:{success}')
        return success
         
    def create_table(self, table_name) -> bool:
        clean_crt_tbl_nm = SansNotesApp.check_char_string(table_name)
        self.__cur.execute(
            SansNotesApp.CREATE_TABLE.format(table_name_field=clean_crt_tbl_nm)
            )
        success = clean_crt_tbl_nm in self.show_all_tables()
        logging.debug(f'{SansNotesApp.check_char_string(clean_crt_tbl_nm)} created:{success}')
        return success

    def insert_data(
        self,
        subject, 
        topic, 
        book, 
        page, 
        notes
        ):
        values_ = ','.join(
            map(
                lambda x: str(x),
                    [
                        subject, 
                        topic, 
                        book, 
                        page, 
                        notes
                    ]
            )
        )
        values_str = SansNotesApp.check_char_string(values_,strict=False)
        self.__cur.execute(
            SansNotesApp.INSERT.format(table_name_field=values_str)
            )
        return True

    def delete_data(self,del_data):
        pass

    def search_data(self,s_data,strict=True):
        pass

    @staticmethod
    def check_char_string(alphanum_string,strict=True) -> str:
        if strict:
            return ''.join(re.findall('[\w+\-0-9]',alphanum_string))
        else:
            return ''.join(re.findall('[\w+\-0-9\._+,]',alphanum_string))
   

if __name__ == "__main__":
    notes = SansNotesApp()
    notes.database_name = 'test'
    notes.db_connect_and_cursor()
    notes.create_table('my_test_table')
    notes.show_all_tables()
    notes.drop_table('my_test_table')
    notes.committ_and_close()