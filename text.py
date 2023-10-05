#install easyocr
#install matplotlib
#install opencv-python-headless

import cv2
import easyocr
import matplotlib.pyplot as plt
import time
#read images
image_path = "jamun.jpg"
img = cv2.imread(image_path)

#instant text detection
reader = easyocr.Reader(["en"], gpu=False)

#detect text
text_ = reader.readtext(img)
for t in text_:
    print(t)

#Creating a box
    bbx, text, score = t
    cv2.rectangle(img, bbx[0], bbx[2], (0, 255, 0), 5)


plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()
#time.sleep(3)
plt.gcf().clear()