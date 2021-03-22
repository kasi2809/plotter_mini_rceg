from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import os, sys
import traceback
import time,cv2
import sqlite3

i=0
j=0


try:
    import cnc_pcb_v1_1

except ImportError:
    print('\n[ERROR] cnc_pcb_v1_1.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure cnc_pcb_v1_1.py is present in this current directory.\n')

except Exception as e:
    print('Your cnc_pcb_v1_1.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)


window = Tk()
window.iconbitmap('images/icon2.ico')
window.geometry("750x250")
window.resizable(width=False, height=False)
window.title("SOLDER")

fl = StringVar()
cn = StringVar()
var = StringVar()

def exit1():
    exit()

def solder():
    print('solder')
    cnc_pcb_v1_1.send_data("3")

def up():
    print('up')
    cnc_pcb_v1_1.send_data("5")

def down():
    print('down')
    cnc_pcb_v1_1.send_data("6")

def right():
    print('right')
    cnc_pcb_v1_1.send_data("7")

def left():
    print('left')
    cnc_pcb_v1_1.send_data("8")

def z_up():
    print('z_up')
    cnc_pcb_v1_1.send_data("1")

def z_down():
    print('z_down')
    cnc_pcb_v1_1.send_data("2")


def proced():
    if (entry_1.get() == '' or myCombo.get() == "--Count--"):
        messagebox.showinfo(title="Warning", message="Please fill all the entrys!")
    else:
        if(messagebox.askokcancel("Confirmation", "Want to continue?")):
            proceed['state'] = DISABLED
            brd=0
            file_path=entry_1.get()
            brd_count = int(myCombo.get())
            print("File Path:",file_path)
            print("Total Number of Boards:",brd_count)
            points = cnc_pcb_v1_1.locate_coordinates(file_path)
            print("Coordinates found")
            cnc_pcb_v1_1.send_data("4"+","+str(brd_count)+","+str(len(points)))
            sorted_points = cnc_pcb_v1_1.find_near_pts(points)
            print("Coordinates sorted")
            error = cnc_pcb_v1_1.calculate_error(sorted_points)
            print("error calc")
            steps = cnc_pcb_v1_1.calulating_steps(error)
            print("calc steps")
            while(brd<brd_count):
                val = cnc_pcb_v1_1.send_data(steps)
                brd+=1
                print("No. of boards completed:",brd)
            val=1
            if val==1:
                messagebox.showinfo(title="Done", message="Soldering is done!")
                reset()

def reset():
    global i
    i=0
    myCombo.current(0)
    entry_1.delete(0,'end')
    if(myCombo.get() != "--Count--"):
        num_brd.destroy()
    proceed['state'] = NORMAL

def abt():
    messagebox.showinfo(title="About",message="This is a GUI Application done for the pcb soldering machine.\n Icon Credit:https://free-icon-rainbow.com/soldering-iron-icon-3/")

def callibrate_win():
    global i
    if(i==1):
        clb_window = Toplevel()
        if (clb_window.winfo_exists()==1):
            clb_window.destroy()
    else:
        i=1
        clb_window = Toplevel()
        clb_window.title("Calibrate")
        clb_window.iconbitmap('images/icon2.ico')
        clb_window.resizable(width=False, height=False)
        clb_window.geometry("500x300")
        clb_window.config(bg="white")
        #Up Button
        up_bn = PhotoImage(file='images/buttons/up.png')
        up_btn = Button(clb_window,text="x",font=("arial",12,"bold"),image=up_bn,compound="center",relief="groove",command=up)
        up_btn.place(x=100,y=30)
        #Left Button
        left_bn = PhotoImage(file='images/buttons/left.png')
        left_btn = Button(clb_window, text="-y", font=("arial", 12, "bold"), image=left_bn, compound="center", relief="groove",command=left)
        left_btn.place(x=30, y=100)
        #Down Button
        down_bn = PhotoImage(file='images/buttons/down.png')
        down_btn = Button(clb_window, text="-x", font=("arial", 12, "bold"), image=down_bn, compound="center", relief="groove",command=down)
        down_btn.place(x=100, y=170)
        #Right Button
        right_bn = PhotoImage(file='images/buttons/right.png')
        right_btn = Button(clb_window, text="y", font=("arial", 12, "bold"), image=right_bn, compound="center", relief="groove",command=right)
        right_btn.place(x=170, y=100)
        #Z Up Button
        z_up_bn = PhotoImage(file='images/buttons/z_up.png')
        z_up_btn = Button(clb_window, text="z", font=("arial", 12, "bold"),fg="white", image=z_up_bn, compound="center",relief="groove",command=z_up)
        z_up_btn.place(x=320, y=30)
        #Z Down Button
        z_down_bn = PhotoImage(file='images/buttons/z_down.png')
        z_down_btn = Button(clb_window, text="-z",fg="white", font=("arial", 12, "bold"), image=z_down_bn, compound="center",relief="groove",command=z_down)
        z_down_btn.place(x=320, y=170)
        #start
        solder_bn = PhotoImage(file='images/buttons/solder.png')
        solder_btn = Button(clb_window,image=solder_bn, compound="center",relief="groove",command=solder)
        solder_btn.place(x=320,y=100)

        clb_window.mainloop()


title = Label(window,text="Welcome to PCB Soldering",font=("georgia",16,"bold")).pack()

img = Image.open('images/CEG_main_logo.png')
photo = ImageTk.PhotoImage(img)
logo = Label(image = photo)
logo.place(x=525,y=10)

menu = Menu(window)
window.config(menu= menu)

subm1 = Menu(menu)
menu.add_cascade(label="File",menu=subm1)
subm1.add_command(label="Exit",command=exit1)

subm2 = Menu(menu)
menu.add_cascade(label="Tools",menu=subm2)
subm2.add_command(label="Callibrate",command=callibrate_win)

subm3 = Menu(menu)
menu.add_cascade(label="Options",menu=subm3)
subm3.add_command(label="About",command=abt)

file_loca = Label(window,text="Enter file location : ",font=("arial",12,"bold"))
file_loca.place(x=10,y=40)

entry_1 = Entry(window,textvar=fl,width='50')
entry_1.insert(0,"")
entry_1.place(x=160,y=44)

num_brd = Label(window,text="Enter number of boards : ",font=("arial",12,"bold"))
num_brd.place(x=10,y=80)
i=1
list_cnt=["--Count--"]
while(i<=50):
    list_cnt.append(i)
    i+=1;

myCombo = ttk.Combobox(window,value=list_cnt)
myCombo.current(0)
myCombo.place(x=210,y=84)

# database


proceed = Button(window,text="Proceed",width=12,bg="green",fg="white",command = proced)
proceed.place(x=50,y=140)

rest = Button(window,text="Reset",width=12,bg="blue",fg="white",command = reset)
rest.place(x=150,y=140)

quit = Button(window,text="Exit",width=12,bg="red",fg="white",command = exit1)
quit.place(x=250,y=140)

window.mainloop()
