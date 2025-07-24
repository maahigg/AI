import cv2
import matplotlib.pyplot as plt

image = cv2.imread('download.jpg')

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

height, width, _ = image.shape

arrow_start_left = (20, height, 50)
arrow_end_right = (width - 20, height- 50)

cv2.arrowedLine(image_rgb, arrow_start_left, arrow_end_right, (255, 0, 0), 3, tipLength=0.05)
cv2.arrowedLine(image_rgb, arrow_end_right, arrow_start_left, (255, 0, 0), 3, tipLength = 0.05)

width_label_position = (width //2 -100, height - 80)
cv2.putText(image_rgb, f"width: {width}px", width_label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

cv2.imwrite('annotated_width.jpg')

plt.imshow(cv2.cvtColor(image_rgb, cv2.COLOR_BGR2RGB))
plt.title('annotated image w bi directional width arrows')
plt.axis('off')
plt.show()