from doctest import master
import tkinter as tk
from tkinter import Label, ttk
from NotesApp import SansNotesApp as snp

#database connection
# notes_db = snp()
# notes_db.database_name = 'sans'
# notes_db.db_connect_and_cursor()
# db_list = notes_db.show_databases()
# notes_db.create_table("test_table")#('default_sans_table')
# db_tables = notes_db.show_tables()


class SansNotesGui(tk.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.master.title('SANS Notes Aoo')
        self.pack()
        self.tab1 = ttk.Notebook(master)
        self.tab2 = ttk.Notebook(master)
        self.make_label()
    
    def make_label(self):
        self.label = Label(master,text="test",width=10)
        self.label.pack()
    



root = tk.Tk()
test_app = SansNotesGui(root)
test_app.mainloop()

# window = tk.Tk()








# window.mainloop()

# notes_db.committ_and_close()