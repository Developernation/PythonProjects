import sqlite3
import os

class SansNotesApp(object):
    
    def __init__(self):
        self.folder = 'NotesAppDbFiles'
        if not os.path.exists(self.__folder):
            os.mkdir(self.__folder)

    def __format_db_name(self,db_name_fmt:str):
        return os.path.join(self.__folder,'{}.db'.format(db_name_fmt))

    @property
    def database_name(self):
        return self.__db_name

    @database_name.setter
    def database_name(self,db_name:str):
        """
        Enter a string with no spaces or special characters
        as the database name
        """
        self.__db_name = self.__format_db_name(db_name)
    
    def db_connect(self):
        self.__con = sqlite3.connect(self.__db_name)
        return self.__con
    
    def get_cursor(self):
        self.__cur = self.__con.cursor()
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


if __name__ == '__main__':
    SansNotesApp()