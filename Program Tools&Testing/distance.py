
points=[[31.6107, 67.8057], [28.9933, 67.8057], [31.2081, 51.7253], [28.5906, 51.7253], [53.3557, 42.7471], [48.9262, 42.2111]]
ref_pt = [0,0]
sorted_points = []
# img1 = cv2.imread('test#1.jpg')
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

print(sorted_points)