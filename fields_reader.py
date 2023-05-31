import datetime
import sqlite3 as sq
import pytesseract

from screen_reader import ScreenRead
# from yamen_ob_new import fields


from cv2 import cv2

base_name = 'yamen_ob.db'
tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
screenshot_path = 'C:\\Python projects\\Screenshort\\'


class Fields(ScreenRead):
    def __init__(self):
        super().__int__()
        self.id = 0  # 1
        self.date = 'null'  # 2
        self.time = 'null'  # 3
        self.date_time = 'null'  # 4
        self.activ = 0  # 5
        self.rait = 0  # 6
        self.grate = 0  # 7
        self.all_profit = 0.0  # 8
        self.cash_profit = 0.0  # 9
        self.card_profit = 0.0  # 10
        self.orders = 0  # 11
        self.commission = 0.0  # 12
        self.balance = 0.0  # 13
        self.tips = 0.0  # 14
        self.name = ""  # 15
        self.verified = False  # 16

    def readImagetoText(self):
        """ Переводит картинку в строку текста"""
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        fileneme = fields.name.replace("'", '')
        screenshotname = screenshot_path + fileneme
        image = cv2.imread(screenshotname)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        config = r'--oem 3 --psm 6'
        string = pytesseract.image_to_string(gray, lang='rus', config=config)
        return string

    def name_to_date(self):
        """ Из имени файла достаем дату """
        datetime_str = fields.name.split('_')
        datetimeplus = datetime_str[1]
        datetime_split = datetimeplus.split('-')
        datetime_split.pop(-1)
        date_time_str = ' '.join(datetime_split)
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')
        return date_time_obj

    def make_null_fields(self):
        fields.activ = 0.0
        fields.rait = 0.0
        fields.grate = 0
        fields.all_profit = 0.0
        fields.cash_profit = 0.0
        fields.card_profit = 0.0
        fields.orders = 0
        fields.commission = 0
        fields.balance = 0.0
        fields.tips = 0.0

    def getNewFile(self):
        with sq.connect(base_name) as con:  # Расшифровываем и раскладываем по полям базы
            cursor = con.cursor()
            cursor.execute(
                "SELECT id, name FROM Screen WHERE readed = '0' AND usable = '1' LIMIT 1")  # Получаем первую запись из базы
            fields.error_log = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            getfilename = cursor.fetchone()
            fields.name = getfilename[1]
            fields.screen_id = getfilename[0]
            string = Fields.readImagetoText(fields)
            stringforbase = string.replace('?', ' ')  # Готовим специальную строку для записи в базу
            stringforbase = stringforbase.replace("'", ' ')
            stringforbase = "'" + stringforbase + "'"
            cursor.execute(f"UPDATE Screen SET strline = {stringforbase}  WHERE id = {fields.screen_id}")
            string_split = string.split()
            # print(string_split)
            return string_split


fields = Fields()
