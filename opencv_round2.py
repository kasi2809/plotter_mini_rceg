import cv2
import numpy as np
global shapes
shapes=[]

def applyPerspectiveTransform(input_img):
    warped_img = None
    imgray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    imblur = cv2.blur(imgray, (3, 3))
    ret, thresh = cv2.threshold(imgray, 245, 255, cv2.THRESH_BINARY)
    thresh = cv2.adaptiveThreshold(thresh, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    epsilon = 0.009 * cv2.arcLength(contours[1], True)
    approx_corners = cv2.approxPolyDP(contours[1], epsilon, True)

    approx_corners = sorted(np.concatenate(approx_corners).tolist())
    approx_corners = [approx_corners[i] for i in [0, 1, 2, 3]]

    corners = np.float32(approx_corners)
    dst = np.float32([[0, 0], [0, 800], [800, 0], [800, 800]])

    # Sorting the corner points
    if corners[0][1] > corners[1][1]:
        temp = dst[0][1]
        dst[0][1] = dst[1][1]
        dst[1][1] = temp
    if corners[2][1] > corners[3][1]:
        temp = dst[2][1]
        dst[2][1] = dst[3][1]
        dst[3][1] = temp

    M = cv2.getPerspectiveTransform(corners, dst)
    warped_img = cv2.warpPerspective(input_img, M, (800,800))
    # cv2.imshow("warped",warped_img)
    # cv2.waitKey(0)
    return warped_img

def splitBoxes(img_b):
    rows = np.split(img_b, 5)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 5)
        for box in cols:
            boxes.append(box)
            # cv2.imshow("box",box)
            # cv2.waitKey(0)
    return boxes
def filter_color(img_1,values):
    shape_data=[]
    # Filtering blue color shapes
    hsv = cv2.cvtColor(img_1, cv2.COLOR_BGR2HSV)
    l_b_blue = np.array([93,153,77])
    u_b_blue = np.array([150, 255, 255])
    mask_blue = cv2.inRange(hsv, l_b_blue, u_b_blue)
    img_blue = cv2.bitwise_and(img_1, img_1, mask=mask_blue)

    # Filtering green colour shapes
    l_b_green = np.array([45,87,77])
    u_b_green = np.array([129,255,255])
    mask_green = cv2.inRange(hsv, l_b_green, u_b_green)
    img_green = cv2.bitwise_and(img_1, img_1, mask=mask_green)

    # Filtering red colour shapes
    l_b_red = np.array([134,116,77])
    u_b_red = np.array([179,255, 255])
    mask_red = cv2.inRange(hsv, l_b_red, u_b_red)
    img_red = cv2.bitwise_and(img_1, img_1, mask=mask_red)
    images = [img_red, img_green, img_blue]
    color = ["red", "green", "blue"]
    for p, im in enumerate(images):

        #im = cv2.blur(im, (3, 3))
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        # Finding contours for each colour
        contours, _ = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(image, contours, -1, (255, 255, 255), 3)

        for cnt in contours:

            # Finding area of contour
            # area = cv2.contourArea(cnt)

            # Finding centroid of contour
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # Finding Shape names
            shape_name = ""
            approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
            if (len(approx) == 3):
                shape_name = "Triangle"

            elif (len(approx) == 5):
                shape_name = "Pentagon"

            elif (len(approx) == 6):
                shape_name = "Hexagon"

            elif (len(approx) == 4):
                shape_name="Quadrilateral"
            elif len(approx)>10:
                shape_name="Circle"
            shape_data = [shape_name,color[p], values+1, cX, cY]

    return shape_data

###########
img = cv2.imread("grid_2.jpg")

warped=applyPerspectiveTransform(img)
cells=splitBoxes(warped)

for val,image in enumerate(cells):

    final_list=filter_color(image,val)

    if final_list!=[]:
        temp_dic={final_list[0]:final_list[1:]}
        shapes.append(temp_dic)
        temp_dic={}

print(shapes)

cv2.imshow("shape",img)
cv2.waitKey(0)


