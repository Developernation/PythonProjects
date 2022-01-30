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
            );
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

    SHOW_TABLE_DATA = """
        SELECT 
            * 
        FROM {table_name_field}
    """

    DELETE_DATA = """
        DELETE FROM {table_name_field} 
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

    def insert_values(
        self,
        table_name,
        subject, 
        topic,
        book, 
        page, 
        notes = ''
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
        values_list = values_str.split(',')
        fmt_func = SansNotesApp.__format_values_string
        insert_value_query_string = SansNotesApp.INSERT.format(
            table_name_field=table_name,
            subject_=fmt_func(values_list[0]),
            topic_=fmt_func(values_list[1]), 
            book_=fmt_func(values_list[2]),
            page_=fmt_func(values_list[3]),
            notes_=fmt_func(values_list[4])
        
        )
        logging.debug(insert_value_query_string)
        self.__cur.execute(
            insert_value_query_string
        )
        return True
    
    def show_table_data(self,table_name):
        clean_table_name = SansNotesApp.check_char_string(table_name)
        show_table_query_string = SansNotesApp.SHOW_TABLE_DATA.format(table_name_field = clean_table_name)
        logging.debug(show_table_query_string)
        table_data = [*self.__cur.execute(
              show_table_query_string
        )]
        logging.debug(f'table_data: {[[tuple[0] for tuple in self.__cur.description]]+table_data}')
        return True

    def delete_data(self,del_data):
        pass

    def search_data(self,
        table_name,
        subject = None, 
        topic = None, 
        book = None, 
        page = None, 
        notes = None,
        strict_search = True
        ):
        search_query_string = SansNotesApp.SHOW_TABLE_DATA.format(table_name_field=SansNotesApp.check_char_string(table_name)) \
            if not any({subject,topic,book,page,notes}) \
            else SansNotesApp.SHOW_TABLE_DATA.format(table_name_field=SansNotesApp.check_char_string(table_name)) + SansNotesApp.format_where_clause(
                subject, 
                topic, 
                book, 
                page,  
                notes,
                strict_search   
            )
        logging.debug(f'search_query_string: {search_query_string}')
        search_table_data = [*self.__cur.execute(
            search_query_string
        )]
        logging.debug(f'search_table_data: {[[tuple[0] for tuple in self.__cur.description]]+search_table_data}')
        return True
        

    @staticmethod
    def check_char_string(alphanum_string,strict=True) -> str:
        if strict:
            return ''.join(re.findall('[\w+\-0-9]+',alphanum_string))
        else:
            return ''.join(re.findall('[\w\-0-9\._+,\s]+',alphanum_string))
    
    @staticmethod
    def __format_values_string(val:str,strict_format=True) -> str:
        val = str(val)
        return f'\'{val}\'' if strict_format else f'\'%{val}%\''
    
    @classmethod
    def format_where_clause(cls,
        subject = None, 
        topic = None, 
        book = None, 
        page = None, 
        notes = None,
        strict_search = True,
        ):
        sep = ' = ' if strict_search else 'LIKE' 
        field_data =' WHERE' + ' AND '.join(
            [
            f' {k} {sep} {cls.__format_values_string(cls.check_char_string(v,strict=False),strict_format=strict_search)}' for k,v in {
            'subject':subject,
            'topic':topic,
            'book':book,
            'page':page,
            'notes':notes
            }.items() 
            if v != None
            ]
            )
        logging.debug('format_where_clause: '+field_data)
        return field_data


if __name__ == "__main__":
    notes = SansNotesApp()
    notes.database_name = 'test'
    notes.db_connect_and_cursor()
    #notes.create_table('my_test_table')
    notes.show_all_tables()
    notes.show_table_data('my_test_table')
    notes.search_data('my_test_table','drink','wine',strict_search=False)
    #notes.insert_values('my_test_table','drink','wine','red wine','80-91','glub glub')
    # notes.format_where_clause(
    #     'my_test_table',
    #     'food',
    #     'cheese',
    #     strict_search=False  
    # )
    notes.committ_and_close()