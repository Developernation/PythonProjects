from doctest import master
import tkinter as tk
from tkinter import ttk
from turtle import color, left
from NotesApp import SansNotesApp as snp

notes_db = snp()

border_effects = {
    "flat": tk.FLAT,
    "sunken": tk.SUNKEN,
    "raised": tk.RAISED,
    "groove": tk.GROOVE,
    "ridge": tk.RIDGE,
}

min_width, min_height = 300,400
#max_width, max_height = 800,800

label_text = ['Subject','Topic','Book','Page','Notes']


window = tk.Tk()

tabControl = ttk.Notebook(window)
#window.geometry('800x1000+50+50')
window.minsize(min_width, min_height)
#window.maxsize(max_width, max_height)
window.title('SANS NOTES APP')


super_frame_tab1 = ttk.Frame(master=window,relief=border_effects['flat'])
#first frame
def build_frame(label_text_info,box_width):
    frame1 = tk.Frame(master=super_frame_tab1,relief=border_effects['flat'],width=100, height=10)
    text_box1 = tk.Entry(master=frame1, width=box_width, borderwidth=4)
    label1 = tk.Label(master=frame1, text=label_text_info,width=10)
    label1.pack(side='left')
    text_box1.pack(side='left')
    return frame1.pack(fill=tk.X)#fill=tk.X,

def Take_input():
    INPUT = inputtxt.get("1.0", "end-1c")
    print(INPUT)
    data = 'test'

    Output.insert(tk.END,data)
    
    

frm0 = build_frame(label_text[0],10)
frm1 = build_frame(label_text[1],40)
frm2 = build_frame(label_text[2],5)
frm3 = build_frame(label_text[3],5)




frame3 = tk.Frame(master=super_frame_tab1,relief=border_effects['flat'],width=50, height=10)
inputtxt = tk.Text(master= frame3, height = 5, width = 52,borderwidth=4,relief=border_effects['sunken'])
label2 = tk.Label(master=frame3, text=label_text[4],width=10)
label2.pack(side='left')
inputtxt.pack(side='left')
inputtxt.insert(tk.END,"test")
frame3.pack(fill=tk.X)


frame5 = tk.Frame(master=super_frame_tab1,relief=border_effects['flat'],width=100, height=10)
label_opt = tk.Label(master=frame5, text='Options',width=10)

Show_Button = tk.Button(master=frame5, 
                 height = 1,
                 width = 10,
                 text ="Show Data",
                 relief=tk.RIDGE,
                 #justify=tk.CENTER,
                 command = lambda:Take_input())
label_opt.pack(side='left')
Show_Button.pack(side='left')

#frame6 = tk.Frame(master=window,relief=border_effects['flat'],width=100, height=10)
Add_Button = tk.Button(master=frame5, 
                 height = 1,
                 width = 10,
                 text ="Add Data",
                 relief=tk.RIDGE,
                 #justify=tk.LEFT,
                #  command = lambda:Take_input()
                 )

Add_Button.pack(side='left')
frame5.pack(fill=tk.X)

frame4 = tk.Frame(master=super_frame_tab1,relief=border_effects['flat'],width=100, height=10)
labeltxt = tk.Label(master=frame4, text='Study Data',width=10)
Output = tk.Text(frame4, height = 50,
              width = 53,
              bg = "light cyan")
labeltxt.pack(side='left')
Output.pack(side='left')
frame4.pack(fill=tk.X)
super_frame_tab1.pack(fill=tk.X)
tabControl.add(super_frame_tab1,text='Tab 1')
#tabControl.pack(expand=1, fill="both",side='left')

#### adding second tab
super_frame_tab2 = ttk.Frame(master=window,relief=border_effects['flat'])
super_frame_tab2.pack(fill=tk.X)
tabControl.add(super_frame_tab2,text='Tab 2')




tabControl.pack(expand=1, fill="both",side='right')

#####

window.mainloop()
