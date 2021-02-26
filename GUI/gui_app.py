from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
import os, sys
import traceback

# try:
#     import cnc_pcb_v1_1
#
# except ImportError:
#     print('\n[ERROR] cnc_pcb_v1_1.py file is not present in the current directory.')
#     print('Your current directory is: ', os.getcwd())
#     print('Make sure cnc_pcb_v1_1.py is present in this current directory.\n')
#
# except Exception as e:
#     print('Your cnc_pcb_v1_1.py throwed an Exception. Kindly debug your code!\n')
#     traceback.print_exc(file=sys.stdout)

window = Tk()
window.iconbitmap(r'C:\Users\sys\Documents\GitHub\plotter_mini_rceg\GUI\icon2.ico')
window.geometry("750x250")
window.title("ELEKTRON")

fl = StringVar()
cn = StringVar()
var = StringVar()

def exit1():
    exit()

def printt():
    global num_brd
    print(entry_1.get())
    if (myCombo.get() != "--Count--"):
        print(myCombo.get())
    num_brd = Label(window, text="OK!Started sodering :-)", font=("arial", 12, "bold"))
    num_brd.place(x=10, y=170)
    proceed['state'] = DISABLED

def reset():
    myCombo.current(0)
    entry_1.delete(0,'end')
    num_brd.destroy()
    proceed['state'] = NORMAL

def abt():
    messagebox.showinfo(title="About",message="This is a GUI Application done for the pcb soldering machine.\n Icon Credit:https://free-icon-rainbow.com/soldering-iron-icon-3/")

def callibrate_win():
    clb_window = Tk()
    clb_window.title("Calibrate")
    clb_window.geometry("300x300")
    up_photo = PhotoImage(file=r"up.png")
    up_size = up_photo.subsample(3,3)
    # up = Button(clb_window, text="x", image=up_size,compound=TOP)
    # up.place(x=50, y=50)
    # Button(clb_window, text='Click Me !', image=up_size,compound=LEFT).pack(side=TOP)


title = Label(window,text="Welcome to PCB Soldering",font=("georgia",16,"bold")).pack()

img = Image.open("CEG_main_logo.png")
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


proceed = Button(window,text="Proceed",width=12,bg="green",fg="white",command = printt)
proceed.place(x=50,y=140)

rest = Button(window,text="Reset",width=12,bg="blue",fg="white",command = reset)
rest.place(x=150,y=140)

quit = Button(window,text="Exit",width=12,bg="red",fg="white",command = exit1)
quit.place(x=250,y=140)

window.mainloop()