import cv2
import numpy as np

def apply_filter(image, filter_type):
    filtered_image = image.copy()

    if filter_type == "red_tint":
        filtered_image[:, :, 1] = 0
        filtered_image[:, :, 0] = 0
    elif filter_type == "green_tint":
        filtered_image[:, :, 0] = 0
        filtered_image[:, :, 2] = 0
    elif filter_type == "sobel":
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
        sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
        combined_sobel = cv2.bitwise_or(sobelx.astype('uint8'), sobely.astype('uint8'))
        filtered_image = cv2.cvtColor(combined_sobel, cv2.COLOR_GRAY2BGR)
    elif filter_type=="canny":
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_image, 100, 200)
        filtered_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return filtered_image

image_path = 'download.jpg'
image = cv2.imread(image_path)

if image is None:
    print('error, image not found')
else:
    filter_type="original"

    print('press the following keys to apply filters:')
    print("r - red tint")
    print('g - green tint')
    print("b - blue tint")
    print("s - sobel edge detection")
    print("c - canny edge detection")
    print("q - quit")

    while True:
        filtered_image = apply_filter(image, filter_type)
        cv2.imshow("filtered img", filtered_image)

        key = cv2.waitKey(0) & 0xFF

        if key == ord('r'):
            filter_type = "red_tint"
        if key == ord('g'):
            filter_type = "green_tint"
        if key == ord('b'):
            filter_type = "blue_tint"
        if key == ord('s'):
            filter_type = "sobel"
        if key == ord('c'):
            filter_type = "canny"
        if key == ord('q'):
            print('exiting..')
            break
        else:
            print('invalid key, pls use r, g, b, s, c, or q')

cv2.destroyAllWindows()