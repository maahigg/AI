import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('download.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image_rgb)
plt.title('original image')
plt.show()

grayimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.imshow(grayimage, cmap = 'gray')
plt.title('grayscale image')
plt.show()

cropped_image = image[100:400, 200:300]
cropped_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
plt.imshow(cropped_rgb)
plt.title('cropped area')
plt.show()

(h, w) = image.shape[:2]
center = (w //2, h //2)
M = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(image, M, (w, h))
rotated_rgb = cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB)
plt.imshow(rotated_rgb)
plt.title('rotated image')
plt.show()

brightness_matrix = np.ones(image.shape, dtype = "uint8") * 50
brighter = cv2.add(image, brightness_matrix)
brighter_rgb = cv2.cvtColor(brighter, cv2.COLOR_BGR2RGB)
plt.imshow(brighter_rgb)
plt.title('brighter image')
plt.show()

cv2.imwrite('gray_image.jpg', grayimage)
cv2.imwrite('cropped_image.jpg', cropped_image)
cv2.imwrite('rotated.jpg', rotated)
cv2.imwrite('brighter.jpg', brighter)