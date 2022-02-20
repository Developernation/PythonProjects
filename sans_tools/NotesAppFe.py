from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from NotesApp import SansNotesApp as snp
from datetime import datetime
from tkinter import ttk
import tkinter as tk
import pandas as pd
import os
pd.set_option('display.max_rows', None)

#database connection
notes_db = snp()
notes_db.database_name = 'sans'
notes_db.db_connect_and_cursor()
db_list = notes_db.show_databases()
notes_db.create_table('default_sans_table')
db_tables = notes_db.show_tables()

#first frame
def build_frame(label_text_info,box_width,master_frame,label_width=10):
    frame1 = tk.Frame(master=master_frame,relief=border_effects['flat'],width=100, height=10)
    text_box1 = tk.Entry(master=frame1, width=box_width, borderwidth=4)
    label1 = tk.Label(master=frame1, text=label_text_info,width=label_width)
    label1.pack(side='left')
    text_box1.pack(side='left')
    frame1.pack(fill=tk.X)
    return text_box1


#-------------------------------------------------------------------------
border_effects = {
    "flat": tk.FLAT,
    "sunken": tk.SUNKEN,
    "raised": tk.RAISED,
    "groove": tk.GROOVE,
    "ridge": tk.RIDGE,
}

min_width, min_height = 300,400

label_text = ['Subject:','Topic:','Book:','Page:','Notes:']


window = tk.Tk()

tabControl = ttk.Notebook(window)

window.minsize(min_width, min_height)
window.title('SANS NOTES APP')

#setting defaults for table list
clickedA = tk.StringVar()
clickedA.set(db_tables[0])

clickedB = tk.StringVar()
clickedB.set(db_tables[0])

clickedC = tk.StringVar()
clickedC.set(db_tables[0])

########################################################
#################### Add Data ##########################
########################################################

super_frame_tab1 = ttk.Frame(master=window,relief=border_effects['flat'])


drop_down_frameA = tk.Frame(master=super_frame_tab1,relief=border_effects['flat'],width=50, height=10)
drop_down_labelA = tk.Label( drop_down_frameA , text = "Select Table:" )
drop_down_labelA.pack(side='left')
# Create Dropdown menu
dropA = tk.OptionMenu(drop_down_frameA , clickedA, *db_tables)
dropA.pack(side='left')
drop_down_frameA.pack(fill=tk.X)
    

frm0 = build_frame(label_text[0],10,super_frame_tab1)
frm1 = build_frame(label_text[1],40,super_frame_tab1)
frm2 = build_frame(label_text[2],5,super_frame_tab1)
frm3 = build_frame(label_text[3],5,super_frame_tab1)


frame3 = tk.Frame(master=super_frame_tab1,relief=border_effects['flat'],width=50, height=10)
inputtxt = tk.Text(master= frame3, height = 5, width = 52,borderwidth=4,relief=border_effects['sunken'])
label2 = tk.Label(master=frame3, text=label_text[4],width=10)
label2.pack(side='left')
inputtxt.pack(side='left')
frame3.pack(fill=tk.X)

def write_dataA():
    input_vals = {
    'table': clickedA.get().strip(),
    'subject':frm0.get().strip(),
    'topic':frm1.get().strip(),
    'book':frm2.get().strip(),
    'page':frm3.get().strip(),
    'notes':inputtxt.get("1.0","end-1c").strip(),
    }

    notes_db.insert_values(
        input_vals['table'],
        input_vals['subject'],
        input_vals['topic'],
        input_vals['book'],
        input_vals['page'],
        input_vals['notes']
    )
    return input_vals

def add_opt():  
    dropA['menu'].add_command(label=frm0_tb3.get(), command=tk._setit(clickedA, frm0_tb3.get()))
    dropB['menu'].add_command(label=frm0_tb3.get(), command=tk._setit(clickedB, frm0_tb3.get()))
    dropC['menu'].add_command(label=frm0_tb3.get(), command=tk._setit(clickedC, frm0_tb3.get()))
    global db_tables
    db_tables.append(frm0_tb3.get())

def create_table():
    notes_db.create_table(frm0_tb3.get().strip())
    add_opt()
    return True

def remove_item():
    r_index1=dropB['menu'].index(frm0_tb3.get())
    dropB['menu'].delete(r_index1)
    clickedB.set(dropB['menu'].entrycget(0,"label")) # select the first one 

    r_index2=dropA['menu'].index(frm0_tb3.get())
    dropA['menu'].delete(r_index2)
    clickedA.set(dropB['menu'].entrycget(0,"label")) # select the first one 
    
    r_index3=dropC['menu'].index(frm0_tb3.get())
    dropC['menu'].delete(r_index3)
    clickedC.set(dropC['menu'].entrycget(0,"label")) # select the first one 
    return True 

def delete_table():
    notes_db.drop_table(frm0_tb3.get().strip())
    remove_item()
    return True


frame5 = tk.Frame(master=super_frame_tab1,relief=border_effects['flat'],width=100, height=10)
label_opt = tk.Label(master=frame5, text='Options',width=10)

Add_Button = tk.Button(master=frame5, 
                 height = 1,
                 width = 10,
                 text ="Add Data",
                 relief=tk.RAISED,
                 fg = "blue",
                 command = lambda:write_dataA()
                 )



frame5.pack(fill=tk.X)
label_opt.pack(side='left')
Add_Button.pack(side='left')
tabControl.add(super_frame_tab1,text='Add Data')

#############################################################
######################## SEARCH DATA TAB ####################
#############################################################
def show_search_data():
    Output.delete('1.0', tk.END)
    global show_vals
    show_vals = {
    'table': clickedB.get(),
    'subject':frm0_tb2.get(),
    'topic':frm1_tb2.get(),
    'book':frm2_tb2.get(),
    'page':frm3_tb2.get(),
    }
    
    global search_data
    search_data = notes_db.search_data( 
        show_vals['table'],
        show_vals['subject'],
        show_vals['topic'],
        show_vals['book'],
        show_vals['page'],
        strict_search = False
    )
    
    Output.insert(tk.END,search_data)

def show_all_table_data():
    Output.delete('1.0', tk.END)
    global search_data
    search_data = notes_db.show_table_data(clickedB.get())
    Output.insert(tk.END,search_data)

def show_all_ingest_columns():
    Output_tb4.delete('1.0', tk.END)
    col_data = None
    if filename.endswith('xlsx'):
        col_data = list(pd.read_excel(filename).columns)
    else:
        col_data = list(pd.read_csv(filename).columns)
    Output_tb4.insert(tk.END,"""
                      *********Directions****** 
    1) Map the columns in your file to their respective column in the 
    table schema by entering them in the spaces above.

    2) If you do not want to map a specific column from you file you can 
    leave the entry blank.

                  Below are the columns in your file:\n
    ******************** Ingest Data Column Names *******************
    \n\t{}
    *****************************************************************
    """.format('\n\t'.join(col_data)))

def delete_data():
    notes_db.delete_data(
        table_name=clickedB.get().strip(),
        subject=frm0_tb2.get().strip(),
        topic=frm1_tb2.get().strip(),
        book=frm2_tb2.get().strip(),
        page=frm3_tb2.get().strip(),
    )
    show_search_data()

def save_to_excel():
    search_data.sort_values(by='topic').reset_index(drop=True).to_excel(
        f"{os.path.join(os.path.expanduser('~'),'Downloads','search_data' + datetime.today().strftime('%y%m%d_%H%M%S'))}.xlsx"
        )

super_frame_tab2 = ttk.Frame(master=window,relief=border_effects['flat'])

drop_down_frameB = tk.Frame(master=super_frame_tab2,relief=border_effects['flat'],width=50, height=10)
drop_down_labelB = tk.Label( drop_down_frameB , text = "Select Table:" )
drop_down_labelB.pack(side='left')

# Create Dropdown menu
dropB = tk.OptionMenu(drop_down_frameB , clickedB, *db_tables)
dropB.pack(side='left')
drop_down_frameB.pack(fill=tk.X)


frm0_tb2 = build_frame(label_text[0],10,super_frame_tab2)
frm1_tb2 = build_frame(label_text[1],40,super_frame_tab2)
frm2_tb2 = build_frame(label_text[2],5,super_frame_tab2)
frm3_tb2 = build_frame(label_text[3],5,super_frame_tab2)


frame0a_tb2 = tk.Frame(master=super_frame_tab2,relief=border_effects['flat'],width=100, height=10)
label_opt2 = tk.Label(master=frame0a_tb2, text='Options:',width=10)

Show_Search_Button = tk.Button(master=frame0a_tb2, 
                 height = 1,
                 width = 15,
                 text ="Show Search Data",
                 relief=tk.RIDGE,
                 fg = "blue",
                 command = lambda : show_search_data() )

Search_All_Data = tk.Button(master=frame0a_tb2, 
                 height = 1,
                 width = 15,
                 text ="Show All Data",
                 relief=tk.RIDGE,
                  fg = "blue",
                 command = lambda : show_all_table_data())

To_Excel_Button = tk.Button(master=frame0a_tb2, 
                 height = 1,
                 width = 15,
                 text ="Save Display To Excel",
                 relief=tk.RIDGE,
                  fg = "blue",
                 command = lambda : save_to_excel())

Delete_Data_Button = tk.Button(master=frame0a_tb2, 
                 height = 1,
                 width = 15,
                 text ="Delete Displayed Data",
                 relief=tk.RIDGE,
                  fg = "red",
                 command = lambda : delete_data())

label_opt2.pack(side='left')
Show_Search_Button.pack(side='left')
Search_All_Data.pack(side='left')
To_Excel_Button.pack(side='left')
Delete_Data_Button.pack(side='left')
frame0a_tb2.pack(fill=tk.X)
#------
frame0b_tb2 = tk.Frame(master=super_frame_tab2,relief=border_effects['flat'],width=100, height=10)
###
Output = tk.Text(frame0b_tb2, height = 50,
              width = 99,
              bg = "light cyan")
###
Output.pack(side='left')

frame0b_tb2.pack(fill=tk.X)

super_frame_tab2.pack(fill=tk.X)

tabControl.add(super_frame_tab2,text='Search Data')

tabControl.pack(expand=1, fill="both",side='right')

############################################################################
#################### Create / Delete Table #################################
############################################################################
super_frame_tab3 = ttk.Frame(master=window,relief=border_effects['flat'])

frm0_tb3 = build_frame('Table Nane:\n *Only letters \n & underscores*',20,super_frame_tab3)

#------
frame0_tb3 = tk.Frame(master=super_frame_tab3,relief=border_effects['flat'],width=100, height=10)
label_opt3 = tk.Label(master=frame0_tb3, text='Options:',width=10)
Create_Button = tk.Button(master=frame0_tb3, 
                 height = 1,
                 width = 15,
                 text ="Create Table",
                 relief=tk.RIDGE,
                 padx=5,
                 fg = "blue",
                 command = create_table
                 )

Delete_Table = tk.Button(master=frame0_tb3, 
                 height = 1,
                 width = 10,
                 text ="Delete Table",
                 relief=tk.RIDGE,
                 fg = "red",
                 command = delete_table
                 )
label_opt3.pack(side='left')
Create_Button.pack(side='left')
Delete_Table.pack(side='left')

frame0_tb3.pack(fill=tk.X)

tabControl.add(super_frame_tab3,text='Create Table')

tabControl.pack(expand=1, fill="both",side='right')

#############################################################################
####################### Upload Excel File ###################################
#############################################################################
super_frame_tab4 = ttk.Frame(master=window,relief=border_effects['flat'])

directions_frame = tk.Frame(master=super_frame_tab4,relief=border_effects['flat'],width=70, height=50)
directions_text = """"
              ********** File Upload Directions **********
    1) Select a table to upload data or create one in the Create Table tab.
    2) Select your file by using the Ingest Data button below
    3) Click Show Columns to display the availble columns for mapping to the table schema columns
    4) Enter the columns from your file that you would like to map to table schema columns in section below
    5) Click the Upload Data button
""" 

directions_label = tk.Label(master=directions_frame, text=directions_text ,width=70)
directions_label.pack(side='left')
directions_frame.pack(fill=tk.X) 

drop_down_frameC = tk.Frame(master=super_frame_tab4,relief=border_effects['flat'],width=50, height=10)
drop_down_labelC = tk.Label( drop_down_frameC , text = "Select Table:" )
drop_down_labelC.pack(side='left')
# Create Dropdown menu
dropC = tk.OptionMenu(drop_down_frameC , clickedC, *db_tables)
dropC.pack(side='left')
drop_down_frameC.pack(fill=tk.X)

frm0_tb4 = build_frame(f'{label_text[0][:-1]} Column Mapping',10,super_frame_tab4,label_width=20)
frm1_tb4 = build_frame(f'{label_text[1][:-1]} Column Mapping',10,super_frame_tab4,label_width=20)
frm2_tb4 = build_frame(f'{label_text[2][:-1]} Column Mapping',10,super_frame_tab4,label_width=20)
frm3_tb4 = build_frame(f'{label_text[3][:-1]} Column Mapping',10,super_frame_tab4,label_width=20)
frm6_tb4 = build_frame('Notes Column Mapping',10,super_frame_tab4,label_width=20)

def ingest_file_data():

    #select file
    filetypes = (
        ('CSV files', '*.csv'),
        ('Excel files', '*.xlsx')
    )
    global filename 
    filename = askopenfilename(
        title='Open files',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected Files',
        message=f'You selected:\n {filename}'
    )

def check_len(str_):
    return str_ if len(str_) > 0 else None


def upload_data():
    Output_tb4.delete('1.0', tk.END)
    table = clickedC.get()

    subject = frm0_tb4.get()
    topic = frm1_tb4.get()
    book = frm2_tb4.get()
    page = frm3_tb4.get()
    notes = frm6_tb4.get()
    
    mapping_vals = {
        
        'subject': check_len(subject),
        'topic': check_len(topic),
        'book': check_len(book),
        'page': check_len(page),
        'notes': check_len(notes),
    }

    notes_db.set_ingest_file(
        filename
    )

    notes_db.rename_df_columns(
        topic_column=mapping_vals['topic'],
        subject_column=mapping_vals['subject'],
        page_column=mapping_vals['page'],
        notes_column=mapping_vals['notes'],
        book_column=mapping_vals['book']
    )

    cursor = notes_db.get_cursor()

    res = notes_db.build_insert_query(
        table,
        cursor,
        topic_column=mapping_vals['topic'],
        subject_column=mapping_vals['subject'],
        page_column=mapping_vals['page'],
        notes_column=mapping_vals['notes'],
        book_column=mapping_vals['book']
        )

    if res:
        showinfo(
            title='File Uploaded',
            message=f'{filename} was uploaded to {table}'
        )

    else:
        showinfo(
            title='File Upload Failure',
            message="Please review input colums:\n{}".format(',\n'.join(icols))
        )



    
    
frm4_tb4 = tk.Frame(master=super_frame_tab4,relief=border_effects['flat'],width=100, height=10)
label_opt4a = tk.Label(master=frm4_tb4, text='Options:',width=10)
Ingest_Button = tk.Button(master=frm4_tb4, 
                 height = 1,
                 width = 15,
                 text ="Ingest Data",
                 relief=tk.RIDGE,
                 padx=5,
                 fg = "blue",
                 command = ingest_file_data
                 )

Show_Columns_Button = tk.Button(master=frm4_tb4, 
                 height = 1,
                 width = 15,
                 text ="Show Columns",
                 relief=tk.RIDGE,
                 padx=5,
                 fg = "green",
                 command = show_all_ingest_columns
                 )

Upload_Data_Button = tk.Button(master=frm4_tb4, 
                 height = 1,
                 width = 15,
                 text ="Upload Data",
                 relief=tk.RIDGE,
                 padx=5,
                 fg = "orange",
                 command = upload_data
                 )

frm5_tb4 = tk.Frame(master=super_frame_tab4,relief=border_effects['flat'],width=100, height=10)
###
Output_tb4 = tk.Text(frm5_tb4, height = 40,
              width = 99,
              bg = "light green")

label_opt4a.pack(side='left')
Ingest_Button.pack(side='left')
Show_Columns_Button.pack(side='left')
Upload_Data_Button.pack(side='left')
Output_tb4.pack(side='bottom')
frm4_tb4.pack(fill=tk.X)
frm5_tb4.pack(fill=tk.X)
tabControl.add(super_frame_tab4,text='Upload CSV / Excel')
tabControl.pack(expand=1, fill="both",side='right')
##############################################################################

window.mainloop()

notes_db.committ_and_close()