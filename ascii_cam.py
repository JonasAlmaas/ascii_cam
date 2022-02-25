import cv2
import numpy as np


font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.265
font_color = (255, 255, 255)
font_thickness = 1

FLIP_IMAGE = False

cv2.namedWindow("ascii_window")

vc = cv2.VideoCapture(0)

frame_width = int(vc.get(cv2. CAP_PROP_FRAME_WIDTH))
frame_height = int(vc.get(cv2. CAP_PROP_FRAME_HEIGHT))

aspect_ratio = frame_width / frame_height

window_height = 1280
window_width = int(window_height * aspect_ratio)

image_height = 128
image_width = int(image_height * aspect_ratio)

pixels_per_char = window_height / image_height;
half_pixels_per_char = pixels_per_char * 0.5


density = ('Ñ','@','#','W','$','0','?','!','a','b','c',';',':','+','=','-',',','.','_',' ')
density_length = len(density)

blank_frame = np.zeros((window_width, window_height), dtype=np.uint8)
blank_frame = cv2.resize(blank_frame, (window_width, window_height))

while True:
    ascii_frame = blank_frame.copy()

    rval, pre = vc.read()

    if rval:
        bnw = cv2.resize(pre, (image_width, image_height))
        bnw = cv2.cvtColor(bnw, cv2.COLOR_BGR2GRAY)
        
        for x in range(image_width):
            for y in range(image_height):
                value = bnw[y][x]
                char_index = round(np.multiply(np.subtract(1, np.divide(value, 255)), density_length-1))
                org_x = round(np.add(np.multiply(x, pixels_per_char), pixels_per_char))
                if FLIP_IMAGE:
                    org_x = np.subtract(window_width, org_x)
                org_y = round(np.add(np.multiply(y, pixels_per_char), half_pixels_per_char))
                ascii_frame = cv2.putText(ascii_frame, density[char_index], (org_x, org_y), font, font_scale, font_color, font_thickness, cv2.LINE_AA)

        cv2.imshow("ascii_window", ascii_frame)
    else:
        break

    key = cv2.waitKey(1)
    if key == 27:
        break

vc.release()

cv2.destroyWindow("ascii_window")
