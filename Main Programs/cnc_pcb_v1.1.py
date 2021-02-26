
#======================================================
#                 CNC SOLDERING MACHINE
#======================================================

#======== LIBRARIES IMPORTED =========
import serial
import xlrd
import sys
import math
#========= GLOBAL VARIABLES ==========
# try:
#     ser=serial.Serial('com5',115200)
# except:
#     pass
global entry_1,myCombo
check_pts = {}
mm_per_step_x=0.13
mm_per_step_y=0.13
points=[]
redius = []
board_count = 0
total_board = 0

#===== Locating the co-ordinates =====

# try:
#     file_path = entry_1.get()
#     total_board = myCombo.get()
# except:
#     print("[ERROR]Enter valid details.")
#     sys.exit()
wb = xlrd.open_workbook("test_board.xls")
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
ref_pt = [0,0]
sorted_points = []
for j in range(0,len(points)):
    min_dis = 0.00
    for k in range(0,len(points)):
        x = points[k][0]
        y = points[k][1]
        dis1 = pow(((x-ref_pt[0])**2+(y-ref_pt[1])**2),0.5)
        if (dis1>min_dis and min_dis==0) or dis1<min_dis:
            min_dis = dis1
            t = k
    ref_pt = points[t]
    points.remove(ref_pt)
    sorted_points.append(ref_pt)
print("Final solder point co-ordinates:")
print(sorted_points)

#===== Printing difference b/w 2 points =====
error=[]
for i in range(len(sorted_points)-1):
    p1x=sorted_points[i][0]
    p1y=sorted_points[i][1]
    p2x=sorted_points[i+1][0]
    p2y=sorted_points[i+1][1]
    diff_x=p2x-p1x
    diff_x= round(diff_x, 2)
    diff_y=p2y-p1y
    diff_y = round(diff_y, 2)
    error.append([diff_x,diff_y,sorted_points[i][2]])
error.insert(0,sorted_points[0])
print("Difference:")
print(error)

#===== Calculating steps needed to move =====
steps=[]
for s in range(len(error)):
    steps_x=int(error[s][0]/mm_per_step_x)
    steps_y=int(error[s][1]/mm_per_step_y)
    steps.append([steps_x,steps_y,int(error[s][2])+1])
    steps.append([steps_x, steps_y, math.ceil(error[s][2])])

print("Steps needed:")
print(steps)

#===== Sending data to Microcontroller ======
# try:
#     while(board_count<total_board):
#         index=0
#         while True:
#             if str(ser.readline())=="b\'NEXT\\r\\n\'":
#                 value = str(steps[index][0])+","+str(steps[index][1])+str(steps[index][2])+","+"\n"
#                 ser.write(value.encode('utf-8'))
#                 index+=1
#             if index==len(steps):
#                 break
#         board_count += 1
#         print("Number of boards completed:", board_count)
#     sys.exit()
# except:
#     print("[ERROR]Sending data to microcontroller.Please restart machine.")