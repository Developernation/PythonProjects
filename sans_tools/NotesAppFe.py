from tkinter.filedialog import askopenfile
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
def build_frame(label_text_info,box_width,master_frame):
    frame1 = tk.Frame(master=master_frame,relief=border_effects['flat'],width=100, height=10)
    text_box1 = tk.Entry(master=frame1, width=box_width, borderwidth=4)
    label1 = tk.Label(master=frame1, text=label_text_info,width=10)
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




##############################################################################

window.mainloop()

notes_db.committ_and_close()