
#======================================================
#                 CNC SOLDERING MACHINE
#======================================================

#======== LIBRARIES IMPORTED =========
import serial
import xlrd

#========= GLOBAL VARIABLES ==========
try:
    ser=serial.Serial('com5',115200)
except:
    pass
mm_per_step_x=0.13
mm_per_step_y=0.13
points=[]

#===== Locating the co-ordinates =====
wb = xlrd.open_workbook("test_board.xls")
sheet = wb.sheet_by_index(0)

for i in range(len(sheet.col_values(2))):
    if sheet.cell_value(i,2) == 1:
        co_ord = sheet.cell_value(i,10)
        co_ord=(co_ord[1:len(co_ord)-1]).split(')(')
        for co_str in co_ord:
            co_str=co_str.replace(' ',',')
            co = co_str.split(',')
            points.append([float(co[0]),float(co[1])])

print("Total points to solder:",len(points))
print("Points of PTH : ",points)


#========= nearest points =========
ref_pt = [0,0]
sorted_points = []
for j in range(0,len(points)):
    min_dis = 0.00
    for i in range(0,len(points)):
        x = points[i][0]
        y = points[i][1]
        dis1 = pow(((x-ref_pt[0])**2+(y-ref_pt[1])**2),0.5)
        if (dis1>min_dis and min_dis==0) or dis1<min_dis:
            min_dis = dis1
            t = i
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
    error.append([diff_x,diff_y])
error.insert(0,sorted_points[0])
print("Difference:")
print(error)

#===== Calculating steps needed to move =====
def errorCorrection(error, rawSteps):
    if rawSteps<0:
        rawSteps=-rawSteps
        integralSteps=int(rawSteps)
        integralSteps=-integralSteps
    else:
        integralSteps = int(rawSteps)

    error += rawSteps - integralSteps
    #print(error)
    if(error >= 1):
        error=error-1
        return error, integralSteps + 1
    elif(error <= -1):
        error=error+1
        return error, integralSteps - 1
    else:
        return error,integralSteps


steps=[]
problemInX = problemInY = 0                         #THESE variables keep a tab on extra steps to be added or subtracted
for i in range(len(error)):
    problemInX, steps_x = errorCorrection(problemInX, (error[i][0]/mm_per_step_x))
    problemInY, steps_y = errorCorrection(problemInY, (error[i][1]/mm_per_step_y))
    steps.append([steps_x,steps_y])
print("Steps needed:")
print(steps)

#===== Sending data to Microcontroller ======
try:
    index=0
    while True:
        if str(ser.readline())=="b\'NEXT\\r\\n\'":
            value = str(steps[index][0])+","+str(steps[index][1])+"\n"
            ser.write(value.encode('utf-8'))
            index+=1
        if index==len(steps):
            break
except:
    pass
