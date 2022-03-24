import cv2
from cv2 import circle
from cv2 import boxFilter
import numpy as np
import math

def find_contours(img, color):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_mask = cv2.inRange(img_hsv, color[0], color[1])
    contours, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

img = cv2.imread("pool_two_bins.jpg")
drawing = img.copy()

color = (
            (30, 80, 0),
            (70, 200, 255)
        )

contours = find_contours(img, color)

for cnt in contours:
    contour_area = cv2.contourArea(cnt)
    if contour_area > 100:
        print("Площадь контура:", contour_area)
        cv2.drawContours(drawing, [cnt], 0, (255, 255, 255), 2)
        
        (bounding_x, bounding_y, bounding_w, bounding_h) = cv2.boundingRect(cnt)
        bounding_pos1 = (bounding_x, bounding_y)
        bounding_pos2 = (bounding_x + bounding_w, bounding_y + bounding_h)
        cv2.rectangle(drawing, bounding_pos1, bounding_pos2, (255, 0, 255), 2)
        print("Площадь прямоугольника:", bounding_h * bounding_w)
        
        rectangle = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rectangle)
        box = np.int0(box)
        cv2.drawContours(drawing, [box], 0, (0, 150, 255), 2)
        rectangle_area = cv2.contourArea(box)
        print("Площадь прямоугольник2:", rectangle_area)
        print()
        
cv2.imshow("window", drawing)
cv2.waitKey(0)