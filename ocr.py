#
#Main OCR block
#
import pytesseract

def extract_text(img):
    text = pytesseract.image_to_string(img,lang='eng',config='--psm 6')
    return text