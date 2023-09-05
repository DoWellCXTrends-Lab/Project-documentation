'''from pytesseract import pytesseract
import os
import requests
from PIL import Image
from io import BytesIO

class OCR:
    def __init__(self):
        self.path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    def extract(self, image_path):
        try:
            pytesseract.tesseract_cmd = self.path

            # Load the image using PIL
            image = Image.open(image_path)

            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(e)
            return "Error"

# URL of the image
image_url = "https://homechef.imgix.net/https%3A%2F%2Fs3.us-west-2.amazonaws.com%2Fasset.homechef.com%2Flanding_pages%2Ftry-oven-ready%2Fno-prep.png?ixlib=rails-1.1.0&auto=format&fm=png&s=ac70bbeead59702a9b309135dc04c494"

# Download the image
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))

ocr = OCR()
text = ocr.extract(image)
print(text)
'''

!pip install easyocr --no-deps # Colab already has all dependencies

!pip install python-bidi

! wget --output-document=ta_poster.jpg https://th.bing.com/th/id/OIP.XMvdsvQZKdtYlus-Y6dDxQHaHa?pid=ImgDet&rs=1

show an image
import PIL
from PIL import ImageDraw
im = PIL.Image.open("ta_poster.jpg")
im

Create a reader to do OCR.
If you change to GPU instance, it will be faster. But CPU is enough.
(by MENU > Runtime > Change runtime type > GPU, then redo from beginning )
import easyocr
reader = easyocr.Reader(['ta','en'])

Doing OCR. Get bounding boxes.
bounds = reader.readtext('ta_poster.jpg')
bounds

Draw bounding boxes
def draw_boxes(image, bounds, color='blue', width=2):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
        draw.line([p0,p1, p2,p3, *p0], fill=color, width=width)
    return image
draw_boxes(im, bounds)