import cv2
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.265
font_color = (255, 255, 255)
font_thickness = 1

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

scale_factor = 0.2
window_width = 1200

frame_width = int(vc.get(cv2. CAP_PROP_FRAME_WIDTH))
frame_height = int(vc.get(cv2. CAP_PROP_FRAME_HEIGHT))

image_width = int(frame_width * scale_factor)
image_height = int(frame_height * scale_factor)

pixels_per_pixel = window_width / image_width;
half_pixels_per_pixel = pixels_per_pixel * 0.5

aspect_ratio = image_height / image_width
frametime = int(1000 / vc.get(cv2. CAP_PROP_FPS))

density = ('Ñ','@','#','W','$','0','?','!','a','b','c',';',':','+','=','-',',','.','_',' ')
density_length = len(density)

blank_frame = np.zeros((int(window_width * aspect_ratio), window_width), dtype=np.uint8)

while True:
    ascii_frame = blank_frame.copy()

    rval, frame = vc.read()

    if rval:
        frame = cv2.resize(frame, (image_width, image_height))
        
        for x in range(image_width):
            for y in range(image_height):
                pixel = frame[y][x]
                greyscale = np.add(np.add(np.multiply(pixel[0], 0.33), np.multiply(pixel[1], 0.33)), np.multiply(pixel[2], 0.33))
                char_index = int(np.floor(np.multiply(np.divide(density_length - 1, 255), np.subtract(255, greyscale))))
                org = (window_width - int(x * pixels_per_pixel + pixels_per_pixel), int(y * pixels_per_pixel + half_pixels_per_pixel))
                ascii_frame = cv2.putText(ascii_frame, density[char_index], org, font, font_scale, font_color, font_thickness, cv2.LINE_AA)

        cv2.imshow("preview", ascii_frame)
    else:
        break

    key = cv2.waitKey(frametime)
    if key == 27:
        break

vc.release()
cv2.destroyWindow("preview")
