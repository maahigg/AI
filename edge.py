import cv2
import numpy as np
import matplotlib.pyplot as plt

def display_image(title, image):
    plt.figure(figsize=(8, 8))
    if len(image.shape) == 2:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(image, cv2.COLOR_BGR2RGB)
    plt.title(title)
    plt.axis('off')
    plt.show()

def interactive_edge_detection(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: image not found!")
        return
    
    gray_image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    display_image("original grayscale image", gray_image)

    print("Select an option:")
    print("1. sobel edge detection")
    print("2. canny edge detection")
    print("3. laplacian edge detection")
    print("4. gaussian smoothing")
    print("5. median filtering")
    print("6. exit")

    while True:
        choice = int(input("enter your choice between 1 to 6"))

        if choice == 1:
            sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize = 3)
            sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
            combined_sobel = cv2.bitwise_or(sobelx.astype(np.uint8), sobely.astype(np.uint8))
            display_image("sobel edge detection", combined_sobel)

        elif choice==2:
            print("adjust thresholds for canny (default: 100 and 200)")
            lower_thresh = int(input("enter lower threshold : "))
            upper_thresh = int(input("enter upper threshold: "))
            edges = cv2.Canny(gray_image, lower_thresh, upper_thresh)
            display_image("canny edge detection", edges)

        elif choice==3:
            laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
            display_image("laplacian edge detecton", np.abs(laplacian).astype(np.uint8))
        
        elif choice==4:
            print("adjust kernel size for gaussian blur (must be odd, default 5)")
            kernel_size = int(input("enter kernel size (odd number): "))
            blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
            display_image("gaussian smoothed image", blurred)

        elif choice == 5:
            print("adjust kernel size for median filtering (must be odd, default 5)")
            kernel_size = int(input("enter kernel size (odd number): "))
            median_filtered = cv2.medianBlur(image, kernel_size)
            display_image("median filtered image", median_filtered)

        elif choice == 6:
            print("exiting..")
            break

        else:
            print("invalid choice, please select a number between 1 and 6")

interactive_edge_detection('download.jpg')