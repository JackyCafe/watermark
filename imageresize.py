import cv2
img = cv2.imread('1.jpg')
img = cv2.resize(img,(63,63))
print(img)

cv2.imwrite('2.png',img)