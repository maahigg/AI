import cv2
import numpy as np
import platform

def apply_color_filter(image, filter_type):
    filtered_image = image.copy()
    if filter_type == "red_tint":
        filtered_image[:, :, 1] = 0  # remove green
        filtered_image[:, :, 0] = 0  # remove blue
    elif filter_type == "blue_tint":
        filtered_image[:, :, 1] = 0  # remove green
        filtered_image[:, :, 2] = 0  # remove red
    elif filter_type == "green_tint":
        filtered_image[:, :, 0] = 0  # remove blue
        filtered_image[:, :, 2] = 0  # remove red
    elif filter_type == "increase_red":
        filtered_image[:, :, 2] = np.clip(filtered_image[:, :, 2] + 50, 0, 255)
    elif filter_type == "decrease_blue":
        filtered_image[:, :, 0] = np.clip(filtered_image[:, :, 0] - 50, 0, 255)
    # 'original' or unknown filter just returns unchanged
    return filtered_image

# Load the image
image_path = 'download.jpg'
image = cv2.imread(image_path)

if image is None:
    print("Error! Image not found")
else:
    filter_type = "original"

    cv2.namedWindow("filtered image", cv2.WINDOW_NORMAL)

    print("Press the following keys to apply filters:")
    print("r - red tint")
    print("b - blue tint")
    print("g - green tint")
    print("i - increase red intensity")
    print("d - decrease blue intensity")
    print("q - quit")

    while True:
        filtered_image = apply_color_filter(image, filter_type)
        cv2.imshow("filtered image", filtered_image)

        # Use waitKey(1) for better compatibility
        key = cv2.waitKey(1) & 0xFF

        if key != 255:  # ignore invalid key (255 means no key pressed)
            print("Key pressed:", chr(key))

        if key == ord('r'):
            filter_type = "red_tint"
        elif key == ord('b'):
            filter_type = "blue_tint"
        elif key == ord('g'):
            filter_type = "green_tint"
        elif key == ord('i'):
            filter_type = "increase_red"
        elif key == ord('d'):
            filter_type = "decrease_blue"
        elif key == ord('q'):
            print("Exiting...")
            break

    cv2.destroyAllWindows()
