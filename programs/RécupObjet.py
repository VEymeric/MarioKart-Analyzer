from PIL import Image
import cv2
new_im = Image.new('RGB', (60,65))
new_im.save("Test/MonImage.png", "PNG")
im1 = cv2.imread('Test/MonImage.png')
im2 = cv2.imread('Images/imageCourse2.png')
for i in range(45,110):
   for j in range(60,120):
        im1[i-45][j-60][0]=im2[i][j][0]
        im1[i - 45][j - 60][1] = im2[i][j][1]
        im1[i - 45][j - 60][2] = im2[i][j][2]
cv2.imwrite('Images/CarapaceVerte2.png',im1)