import cv2
def main():
    image_path = 'download.jpg'
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: unable to lead image at {image_path}")
        return
    print("Original image loaded successfully")

    sizes = {
        'small': (200, 200),
        'medium': (400, 400),
        'large': (600, 600),
    }

    for size_name, dimensions in sizes.items():
            resized = cv2.resize(image, dimensions)
            cv2.imshow(f"{size_name.capitalize()} Image", resized)
            cv2.imwrite(f"Input_image_{size_name}.jpg", resized)
            print(f"Image resized to {dimensions[0]}x{dimensions[1]} pixels ({size_name}) and saved.")

    print("Displaying resized images. press any key in the image windows to exit. ")
    cv2. waitKey(0)
    cv2.destroyAllWindows()
    print("All windows closed. project completed successfully.")

if __name__ == "__main__":
    main()

        
