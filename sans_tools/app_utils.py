from numpy import void
import pandas as pd
from typing import List
from pprint import pprint 

class AppFileHandler():
    INSERT_FILE = """
        INSERT INTO {table_name_field} 
            (
            {col_names}
            )
        VALUES 
            {values_insertion}
        """
    
    def __init__(self):
        self.ingest_file_df = None
        self.mappings = None
        self.insert_query = None

    def set_ingest_file(
        self,
        file_name: str,
        sheetname = 0,
        use_cols: List[str] = None,
        na_values: str = None,
        na_filter: bool = True,
        delimiter: str = ','        
        ) -> void:
        
        if file_name.endswith('xlsx'):
            self.ingest_file_df = pd.read_excel(
                file_name,
                sheet_name = sheetname,
                usecols = use_cols,
                na_values= na_values,
                na_filter = na_filter,
                )
            

        elif file_name.endswith('csv'):
            self.ingest_file_df = pd.read_csv(
                file_name,
                usecols = use_cols,
                sep = delimiter,
                na_values= na_values,
                na_filter = na_filter,

                )
        else:
            raise ValueError('Unable to process file. Please provide an excel or csv file')
         
    def set_colum_mappings(
        self,
        topic_column:str = None,
        book_column:str = None,
        page_column:str = None,
        subject_column:str = None,
        notes_column:str = None
        ) -> void:
        """
            input column mappings from dataframe to table column names
        """
        self.mappings = dict(filter(lambda x: x[1] is not None , {
            'subject':subject_column,
            'topic':topic_column,
            'book':book_column,
            'page':page_column,
            'notes':notes_column,
        }.items()))
    
    def rename_df_columns(self) -> void:

        self.ingest_file_df = self.ingest_file_df.rename(
            columns={v:k for k,v in self.mappings.items()}
        )
        print(self.ingest_file_df.columns)
        
    
    def build_insert_query(self,table_name: str) -> str:
        
        formatted_values_tup = [
            (
                k,self.ingest_file_df[k].tolist()
                ) 
                for k in self.ingest_file_df[list(self.mappings.keys())]
            ]

        cols = []
        formatted_values_lst = []
        for data in formatted_values_tup:
            cols.append(data[0])
            formatted_values_lst.append(data[1])

        formatted_values_final = list(zip(*formatted_values_lst))
        cols_insertion = '{}'.format(','.join(cols))

        formatted_values = ','.join(
            '({})'.format(
                ','.join(
                    '\'{}\''.format(x) for x in vals_tup
                    )
                ) 
                for vals_tup in  formatted_values_final
            )

        self.insert_query = AppFileHandler.INSERT_FILE.format(
            table_name_field = table_name,
            col_names = cols_insertion,
            values_insertion = formatted_values,
            )
        
        return self.insert_query
        

if __name__ == '__main__':
    app = AppFileHandler()
    test_file = 'sans_study_notes_test.xlsx'
    app.set_ingest_file(test_file,use_cols=['Type', 'Topic', 'Page', 'Note'])
    app.set_colum_mappings(topic_column='Type',subject_column='Topic',page_column='Page')
    app.rename_df_columns()
    pprint(app.build_insert_query('default_sans_table'))
    