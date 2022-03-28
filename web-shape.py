import cv2
import numpy as np
import math

def find_contours(img, color):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_mask = cv2.inRange(img_hsv, color[0], color[1])
    contours, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

# связываем видеопоток камеры с переменной capImg
capImg = cv2.VideoCapture(0)
# запускаем бесконечный цикл, чтобы следить
# в реальном времени
while(True):
# получаем кадр из видеопотока,
# кадры по очереди считываются в переменную frame
    ret, frame = capImg.read()

    drawing = frame.copy()

    color = (
                (56, 190, 90),
                (74, 255, 255)
            )

    contours = find_contours(frame, color)

    for cnt in contours:
        contour_area = cv2.contourArea(cnt)
        if contour_area > 100:
            print("Площадь контура:", contour_area)
            cv2.drawContours(drawing, [cnt], 0, (255, 255, 255), 2)
            
            (circle_x, circle_y), circle_radius = cv2.minEnclosingCircle(cnt)
            circle_area = math.pi * circle_radius**2
            print("Площадь куруга:", circle_area)
            
            rectangle = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rectangle)
            box = np.int0(box)
            rectangle_area = cv2.contourArea(box)
            print("Площадь прямоугольника:", rectangle_area)
            rect_w, rect_h = rectangle[1][0], rectangle[1][1]
            aspect_ratio = max(rect_w, rect_h) / min(rect_w, rect_h)
            
            try:
                triangle = cv2.minEnclosingTriangle(cnt)[1]
                triangle = np.int0(triangle)
                triangle_area = cv2.contourArea(triangle)
            except:
                triangle_area = 0

            print("Площадь треугольника:", triangle_area)        
            print()

            shapes_areas = {
                'circle': circle_area,
                'triangle': triangle_area,
                'rectangle' if aspect_ratio > 1.25 else 'square': rectangle_area
            }

            diffs = {
                name: abs(contour_area - shapes_areas[name]) for name in shapes_areas
            }

            shape_name = min(diffs, key=diffs.get)
            
            if shape_name == 'circle':
                cv2.circle(drawing, (int(circle_x), int(circle_y)), int(circle_radius), (255, 255, 0), 2, cv2.LINE_AA)
            elif shape_name == 'triangle':
                cv2.drawContours(drawing, [triangle], 0, (100, 255, 155), 2, cv2.LINE_AA)
            else:
                cv2.drawContours(drawing, [box], 0, (0, 150, 255), 2, cv2.LINE_AA)
            
            print()

            moments = cv2.moments(cnt)
            try:
                x = int(moments['m10'] / moments['m00'])
                y = int(moments['m01'] / moments['m00'])
                cv2.circle(drawing, (x, y), 4, (0, 100, 255), -1, cv2.LINE_AA)

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(drawing, shape_name, (x - 40, y + 30), font, 1, (0,0,0), 4, cv2.LINE_AA)
                cv2.putText(drawing, shape_name, (x - 41, y + 31), font, 1, (255,255,255), 2, cv2.LINE_AA)
            except:
                pass

# показываем кадр в окне ’Video’
    cv2.imshow('Video', drawing)
# организуем выход из цикла по нажатию клавиши,
# ждем 10 миллисекунд нажатие, записываем код
# нажатой клавиши
    key_press = cv2.waitKey(10)
# если код нажатой клавиши совпадает с кодом
# «q»(quit - выход),
    if key_press == ord('q'):
# то прервать цикл while
        break
# освобождаем память от переменной capImg
capImg.release()
# закрываем все окна opencv
cv2.destroyAllWindows()