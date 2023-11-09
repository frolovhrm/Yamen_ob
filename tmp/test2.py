import cv2
import os
import pytesseract

tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

filenameList = ["Screenshot_2021-07-28-10-15-47-884_ru.yandex.taximeter.x", "Screenshot_2021-07-28-10-15-53-685_ru.yandex.taximeter.x", "Screenshot_2021-07-28-19-14-13-892_ru.yandex.taximeter.x", "Screenshot_2021-07-28-19-14-19-096_ru.yandex.taximeter.x"]
filenameList = ["Screenshot_2021-07-28-10-15-47-884_ru.yandex.taximeter.x"]
screenshot_path = 'C:\\Python projects\\ScreenExp\\'
screenshot_path_new = 'C:\\Python projects\\ScreenExp\\1\\'

# for n in filenameList:
#     for i in range(160, 250, 10):
#         filenemeLine = n.replace("'", '') + ".jpg"
#         screenshotName = screenshot_path + filenemeLine
#         image = cv2.imread(screenshotName)
#         # gray = cv2.cvtColor(image, cv2.IMREAD_GRAYSCALE)
#         thresh = i
#         # filenemeLine +=
#         # print(filenemeLine)
#         img_binary = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
#         cv2.imwrite(screenshot_path_new + n.replace("'", '') + str(thresh) + ".jpg", img_binary)


pytesseract.pytesseract.tesseract_cmd = tesseract_path
fileneme = 'C:\Python projects\ScreenExp\Screenshot_2021-08-24-21-25-39-778_ru.yandex.taximeter.jpg'

print(fileneme)
image = cv2.imread(fileneme)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.threshold(image, 180, 255, cv2.THRESH_BINARY)[1]
config = r'--oem 3 --psm 6'
string = pytesseract.image_to_string(gray, lang='rus', config=config)
# string = pytesseract.image_to_string(image, lang='rus', config=config)
print(string)