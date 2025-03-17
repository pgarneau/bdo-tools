import pytesseract
import cv2 as cv

class Ocr:
    config = r"--oem 3 --psm 6"
    def __init__(self):
        pass

    def get_text(self, img):
        # cv.imshow('Matches', img)
        # return pytesseract.image_to_string(img, config='digits')
        return pytesseract.image_to_string(img, config=self.config)
