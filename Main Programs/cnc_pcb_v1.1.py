
#======================================================
#                 CNC SOLDERING MACHINE
#======================================================

#======== LIBRARIES IMPORTED =========
import serial
import xlrd
import math
#========= GLOBAL VARIABLES ==========
check_pts = {}
mm_per_step_x=0.13
mm_per_step_y=0.13
points=[]
redius = []

#===== Locating the co-ordinates =====

def locate_coordinates(file_path):
    wb = xlrd.open_workbook(file_path)
    sheet = wb.sheet_by_index(0)

    for i in range(len(sheet.col_values(2))):
        coordinates = []
        if sheet.cell_value(i,2) == 1:
            rad = sheet.cell_value(i, 7)
            redius.append(rad)
            co_ord = sheet.cell_value(i,10)
            co_ord=(co_ord[1:len(co_ord)-1]).split(')(')
            for co_str in co_ord:
                co_str=co_str.replace(' ',',')
                co = co_str.split(',')
                coordinates.append([float(co[0]),float(co[1])])
                check_pts[rad] = coordinates


    print("Radius and points:",check_pts)

    for r in redius:
        for c in check_pts[r]:
            c.append(r)
            points.append(c)
    print("Total points to solder:",len(points))
    print("Points of PTH : ",points)

#========= nearest points =========
def find_near_pts(pooints):
    ref_pt = [0,0]
    sorted_points = []
    for j in range(0,len(pooints)):
        min_dis = 0.00
        for k in range(0,len(pooints)):
            x = pooints[k][0]
            y = pooints[k][1]
            dis1 = pow(((x-ref_pt[0])**2+(y-ref_pt[1])**2),0.5)
            if (dis1>min_dis and min_dis==0) or dis1<min_dis:
                min_dis = dis1
                t = k
        ref_pt = pooints[t]
        pooints.remove(ref_pt)
        sorted_points.append(ref_pt)
    print("Final solder point co-ordinates:")
    print(sorted_points)
    return sorted_points

#===== Printing difference b/w 2 points =====
def calculate_error(sort_points):
    error=[]
    for i in range(len(sort_points)-1):
        p1x=sort_points[i][0]
        p1y=sort_points[i][1]
        p2x=sort_points[i+1][0]
        p2y=sort_points[i+1][1]
        diff_x=p2x-p1x
        diff_x= round(diff_x, 2)
        diff_y=p2y-p1y
        diff_y = round(diff_y, 2)
        error.append([diff_x,diff_y,sort_points[i][2]])
    error.insert(0,sort_points[0])
    print("Difference:")
    print(error)
    return error
#===== Calculating steps needed to move =====
def calulating_steps(err):
    stps=[]
    for s in range(len(err)):
        steps_x=int(err[s][0]/mm_per_step_x)
        steps_y=int(err[s][1]/mm_per_step_y)
        stps.append([steps_x,steps_y,int(err[s][2])+1])
        stps.append([steps_x, steps_y, math.ceil(err[s][2])])

    print("Steps needed:")
    print(stps)
    return stps

#===== Sending data to Microcontroller ======
def send_data(tot_brd,stps):
    board_count = 0
    tot_brd = 0
    try:
        ser=serial.Serial('com5',115200)
    except:
        print("[ERROR]Connection Not Established.")
    try:
        while(board_count<tot_brd):
            index=0
            while True:
                if str(ser.readline())=="b\'NEXT\\r\\n\'":
                    value = str(stps[index][0])+","+str(stps[index][1])+str(stps[index][2])+","+"\n"
                    ser.write(value.encode('utf-8'))
                    index+=1
                if index==len(stps):
                    break
            board_count += 1
            print("Number of boards completed:", board_count)
        return 1
    except:
        print("[ERROR]Sending data to microcontroller.Please restart machine.")