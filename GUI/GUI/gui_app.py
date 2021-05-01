from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk

import cnc_pcb_v1_1
import datetime

now = datetime.datetime.now()

number_of_holes=0
board_count=0
file_name=''
cost_per_board=0
total_cost=0
i_c=0
i_s=0
j=0
ret_val=-1
pt = '--Port--'

ports_list = []
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
for i in  ports:
    ports_list.append(i.name)

# print(ports_list)
'''

import os, sys
import traceback
import time,cv2

try:
    import cnc_pcb_v1_1

except ImportError:
    print('\n[ERROR] cnc_pcb_v1_1.py file is not present in the current directory.')
    print('Your current directory is: ', os.getcwd())
    print('Make sure cnc_pcb_v1_1.py is present in this current directory.\n')

except Exception as e:
    print('Your cnc_pcb_v1_1.py throwed an Exception. Kindly debug your code!\n')
    traceback.print_exc(file=sys.stdout)
'''

window = Tk()
window.iconbitmap('images/icon2.ico')
window.geometry("750x250")
window.resizable(width=False, height=False)
window.title("SOLDER")

fl = StringVar()
cn = StringVar()
var = StringVar()

def exit1():
    window.destroy()

def select_port():
    global myCompo
    def submit_selp():
        global pt
        pt = str(myCompo.get())
        if (pt == "--Port--"):
            messagebox.showinfo(title="Warning", message="Please select the port!")
        else:
            # print(str(pt))
            t = cnc_pcb_v1_1.select_com_port(pt)
            if(t==1):
                if(messagebox.showinfo(title="Port",message= pt+" is selected.")):
                    selp_window.destroy()
                    port_label = Label(window, text=pt, font=('arial', '12', 'bold'))
                    port_label.place(x=45, y=201)

    def reset_selp():
        myCompo.current(0)

    global i_s,ports_list
    if(i_s==1):
        selp_window = Toplevel()
        if (selp_window.winfo_exists()==1):
            selp_window.destroy()
    else:
        i_s=1
        selp_window = Toplevel()
        selp_window.title("Select Port")
        selp_window.iconbitmap('images/icon2.ico')
        selp_window.resizable(width=False, height=False)
        selp_window.geometry("500x300")
        f_line = Label(selp_window, text="Select the bluetooth port named \"CNC_PCB\" (incoming port)",font=('16'))
        f_line.place(x=50,y=50)
        ports_list.insert(0,"--Port--")
        myCompo = ttk.Combobox(selp_window, value=ports_list)
        myCompo.current(0)
        myCompo.place(x=150, y=80)
        proceed = Button(selp_window, text="Submit", width=12, bg="green", fg="white", command=submit_selp)

        proceed.place(x=120, y=140)

        rest = Button(selp_window, text="Reset", width=12, bg="blue", fg="white", command=reset_selp)
        rest.place(x=220, y=140)
    
def enter_data(file_name,number_of_holes,board_count):
    time = now.strftime("%H:%M:%S")
    today = now.strftime("%d_%m_%Y")
    name = str(today)+'.txt'
    f=open(name,"a")
    info =  "\n\nTime: "+str(time) \
           + "\nFile name: " + str(file_name) \
           + "\nNumber of holes: " + str(number_of_holes) \
           + "\nNumber of boards: " + str(board_count) \
           + "\nCost per board: " + str(number_of_holes * 2.00) \
           + "\nTotal Cost (INR): " + str(board_count * number_of_holes * 2.00)
    f.write(info)
    f.close()

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
    global number_of_holes,board_count,file_name
    if (entry_1.get() == '' or myCombo.get() == "--Count--"):
        messagebox.showinfo(title="Warning", message="Please fill all the entrys!")
    else:
        proceed['state'] = DISABLED
        brd=0
        file_path=entry_1.get()
        brd_count = int(myCombo.get())
        print("File Path:",file_path)
        print("Total Number of Boards:",brd_count)
        points = cnc_pcb_v1_1.locate_coordinates(file_path)
        print("Coordinates found")
        #####################
        file_name=file_path
        board_count=brd_count
        number_of_holes=len(points)
        #####################
        info = "Bill:"+"\nNumber of holes:"+str(number_of_holes)\
               +"\nNumber of boards:"+str(board_count)\
               +"\nCost per board:"+str(number_of_holes*2.00)\
               +"\nTotal Cost (INR): "+str(board_count*number_of_holes*2.00)\
               +"\n\nWant to continue?"
        if (messagebox.askokcancel("Bill Confirmation", info)):
            enter_data(file_name,number_of_holes,board_count)
            print('value appended')
            cnc_pcb_v1_1.send_data("4" + "," + str(brd_count) + "," + str(len(points)))
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
            # val=1
            if val==1:
                messagebox.showinfo(title="Done", message="Soldering is done!")
                reset()
        else:
            proceed['state'] = NORMAL

def reset():
    global i
    i=0
    myCombo.current(0)
    entry_1.delete(0,END)
    # if(myCombo.get() != "--Count--"):
    #     num_brd.destroy()
    proceed['state'] = NORMAL

def abt():
    messagebox.showinfo(title="About",message="This is a GUI Application done for the pcb soldering machine.\n Icon Credit:https://free-icon-rainbow.com/soldering-iron-icon-3/")


def callibrate_win():
    global i_c
    if(i_c==1):
        clb_window = Toplevel()
        if (clb_window.winfo_exists()==1):
            clb_window.destroy()
    else:
        i_c=1
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
subm2.add_command(label="Select Port",command=select_port)
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
print(pt)

port_label = Label(window, text="Port : ",font=('arial','12','bold'))
port_label.place(x=0,y=200)

proceed = Button(window,text="Proceed",width=12,bg="green",fg="white",command = proced)
proceed.place(x=50,y=140)

rest = Button(window,text="Reset",width=12,bg="blue",fg="white",command = reset)
rest.place(x=150,y=140)

quit = Button(window,text="Exit",width=12,bg="red",fg="white",command = exit1)
quit.place(x=250,y=140)

window.mainloop()
