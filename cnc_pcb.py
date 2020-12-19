import cv2
import serial
ser=serial.Serial('com10',115200)
mm_per_step_x=0.15
mm_per_step_y=0.15
#--------------------PCB dimensions(in mm)---------
pcb_width=60
pcb_height=80
#--------------------------------------------------
points=[]
area_list=[]
img=cv2.imread("test#1.jpg")
img=cv2.resize(img,(600,600))
cv2.imshow("Initial",img)

#Removing black area
img_p = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
contours, _ = cv2.findContours(img_p, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    area = cv2.contourArea(cnt)
    area_list.append(area)
green_contour=contours[area_list.index(max(area_list))]
x1=green_contour[0][0][0]
x2=green_contour[2][0][0]
y1=green_contour[0][0][1]
y2=green_contour[2][0][1]
img=img[y1:y2,x1:x2]
width=img.shape[1]
height=img.shape[0]
print("Cropped Image dimensions(px):")
print("Width=",width,"\nHeight=",height)


#Locating soldering co-ordinates
img_f = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
contoursf, _ = cv2.findContours(img_f, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(len(contoursf))
for cnt in contoursf:
    area = cv2.contourArea(cnt)
    if area<50:
        cv2.drawContours(img,cnt,-1,(255,255,255),2)
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        #cv2.putText(img,str(cX),(cX,cY),cv2.FONT_HERSHEY_TRIPLEX,1,(255,0,0),1)
        cx=(pcb_width*cX)/width
        cx=round(cx,4)
        cy=(pcb_height*cY)/height
        cy = round(cy,4)
        points.append([cx,cy])
cv2.imshow("Final",img)
cv2.waitKey(0)
print("Total points to solder:",len(points))

#to be edited by giri
#nearest points
ref_pt = [0,0]
sorted_points = []
img1 = cv2.imread('test#1.jpg')
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


#Printing difference b/w 2 points
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

#Calculating steps needed to move
steps=[]
for i in range(len(error)):
    steps_x=int(error[i][0]/mm_per_step_x)
    steps_y=int(error[i][1]/mm_per_step_y)
    steps.append([steps_x,steps_y])
print("Steps needed:")
print(steps)

#Sending data to Arduino
index=0
while True:
    if str(ser.readline())=="b\'NEXT\\r\\n\'":
        value = str(steps[index][0])+","+str(steps[index][1])+"\n"
        ser.write(value.encode('utf-8'))
        index+=1
    if index==len(steps):
        break

cv2.waitKey(0)