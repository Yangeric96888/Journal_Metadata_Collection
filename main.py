from Page import Page
from PIL import Image
import numpy as np
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    for current_file_name in os.listdir("./front_page"):
        if ".jpg" in current_file_name:
            img = np.array(Image.open("./front_page/" + current_file_name))
            text = pytesseract.image_to_string(img)

            current_file = Page(text)

            print(current_file.text)
