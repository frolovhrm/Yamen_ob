import datetime
import json
import sqlite3 as sq
import os
import pytesseract
import cv2
from creat_db_ob import createNewBase
from readTextToFields import readTextToFields
from readTextToFields2 import readTextToFields2
from tqdm import tqdm
from analitic_new import checkduble

screenshot_path = 'C:\\Python projects\\Screenshort\\'
base_name = 'yamen_ob.db'
tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

createNewBase()


class Screen:
    def __int__(self):
        self.screen_id = ''
        self.name = ''
        self.error_log = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        """ Разряды лога 0 - версия парсера
                        1 - activ
                        2 - rait
                        3 - grate
                        4 - all_profit
                        5 - cash_profit
                        6 - cart_profit
                        7 - orders
                        8 - commission
                        9 - balance
                        10 - ошибка getFloat """

    def findNewFiles(self):  # Отбираем подходящие файлы для сканирования и складываем их имена в базу
        count = 0
        for adress, dirs, files in os.walk(
                screenshot_path):
            print(f'В указанной папаке найдено файлов - {len(files)} \nПроверяем файлы и добавляем новые в базу ...')
            for file in tqdm(files):
                screen.name = ("'" + file + "'")
                with sq.connect(base_name) as con:
                    cursor = con.cursor()
                    cursor.execute(f"SELECT name FROM Screen WHERE  name = {screen.name}")
                    if cursor.fetchone() is None:
                        if 'yandex.taximeter' in screen.name:
                            cursor = con.cursor()
                            cursor.execute(
                                f"INSERT INTO Screen VALUES(null, {screen.name}, 1, False, null, null)")
                            count += 1
        print(f'... найдено подходящих для дальнейшей работы и добавленно в базу - {count} файлов \n')

    def notReadedFilesInBase(self):
        with sq.connect(base_name) as con:  # Проверяем количество доступных для расшифровки файлов
            cursor = con.cursor()
            cursor.execute("SELECT COUNT (readed) FROM Screen WHERE readed = '0' AND usable = '1'")
            count = cursor.fetchone()
            notReadedFilesInBase = count[0]
            print(f'Всего файлов пригодных для расшифровки в базе - {notReadedFilesInBase}')
            return notReadedFilesInBase


class Fields(Screen):

    def __init__(self):
        super().__int__()
        self.id = 0  # 1
        self.date = 'null'  # 2
        self.time = 'null'  # 3
        self.date_time = 'null' # 4
        self.activ = 0  # 5
        self.rait = 0  # 6
        self.grate = 0  # 7
        self.all_profit = 0.0  # 8
        self.cash_profit = 0.0  # 9
        self.cart_profit = 0.0  # 10
        self.orders = 0  # 11
        self.commission = 0.0  # 12
        self.balance = 0.0  # 14
        self.name = ""  # 15
        self.verified = False  # 16

    def readImagetoText(self):
        """ Переводит картинку в строку текста"""
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        fileneme = fields.name.replace("'", '')
        screenshotname = screenshot_path + fileneme
        # print(f'2.1) есть файл - {screenshotname}')
        image = cv2.imread(screenshotname)
        # print('2.2) файл подготовлен')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # print('2.3) файл серый, отдали читать')
        config = r'--oem 3 --psm 6'
        string = pytesseract.image_to_string(gray, lang='rus', config=config)
        return string

    def nameToDate(self):
        """ Из имени файла достаем дату """
        datetime_str = fields.name.split('_')
        datetimeplus = datetime_str[1]
        datetime_split = datetimeplus.split('-')
        datetime_split.pop(-1)
        date_time_str = ' '.join(datetime_split)
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')
        return date_time_obj

    def makeNullFields(self):
        fields.activ = 0.0
        fields.rait = 0.0
        fields.grate = 0
        fields.all_profit = 0.0
        fields.cash_profit = 0.0
        fields.cart_profit = 0.0
        fields.orders = 0
        fields.commission = 0
        fields.balance = 0.0

    def getNewFile(self):
        with sq.connect(base_name) as con:  # Расшифровываем и раскладываем по полям базы
            cursor = con.cursor()
            # try:
            cursor.execute(
                "SELECT id, name FROM Screen WHERE readed = '0' AND usable = '1' LIMIT 1")  # Получаем первую запись из базы
            fields.error_log = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            getfilename = cursor.fetchone()
            fields.name = getfilename[1]
            screen.screen_id = getfilename[0]
            # print(f'2) Начало распознавания')
            string = Fields.readImagetoText(fields)
            # print(f'3) Распознали')
            # print(fields.name)
            # print(screen.screen_id)
            # print(f'тест -{fields.error_log}')
            stringforbase = string.replace('?', ' ')  # Готовим специальную строку для записи в базу
            stringforbase = stringforbase.replace("'", ' ')
            stringforbase = "'" + stringforbase + "'"
            # print(f'3.1) Начитаем писать подготовленную строку в базу')
            cursor.execute(f"UPDATE Screen SET strline = {stringforbase}  WHERE id = {screen.screen_id}")
            # print(f'4) Записали в базу строку {screen.screen_id} - {stringforbase}')
            string_split = string.split()
            # print(string_split)
            return string_split
            # except:
            #     print('Файлы в базе не обнаружены')

    # def writeFieldsToBase(self):
    #
    #


screen = Screen()
Screen.findNewFiles(screen)

notReadedFilesInBase = Screen.notReadedFilesInBase(screen)

listNotParsFile = []

fields = Fields()

question = 0

if notReadedFilesInBase > 0:
    try:
        question = int(input('Сколько файлов расшифровать? - '))
    except ValueError:
        print('... ввод не корректен,\nКонец ')
        quit()

    if question == 0:
        quit()

    if question <= notReadedFilesInBase:

        # tqdm
        for i in tqdm(range(question)):
            # print(f'\n1) файл {i} ')

            Fields.makeNullFields(fields)  # Сбрасываем значение полей на ноль
            string_split = Fields.getNewFile(fields)  # Выбираем файл для расшифровки, и переводим его в сплит строку
            # print(f'Начальное имя экземпляра - {fields.name}')

            with sq.connect(base_name) as con:
                cursor = con.cursor()
                # try:
                # fields.date = str(Fields.nameToDate(fields.name))  # выделяем дату из имени
                datetime_obj = (Fields.nameToDate(fields.name))  # выделяем дату из имени
                # print(screen.screen_id)
                fields.date = str(datetime_obj.date())
                fields.time = str(datetime_obj.time())
                fields.date_time = datetime_obj

                # print((datetime_obj.date()))
                # print(f'дата: {date_time_obj.date()}')
                # print(f'время: {date_time_obj.time()}')
                # print(fields.date, type(fields.date))
                # print(fields.time, type(fields.time))


                # print(f"5) Дата = {fields.date}")
                if fields.date < '2022-04-04':
                    # print(f'5.1) old way')
                    readTextToFields(fields, string_split)  # Расшифровываем и раскладываем по полям базы
                    # print(string_split)
                else:
                    # print(f'5.2) new way')
                    readTextToFields2(fields, string_split)  # Расшифровываем и раскладываем по полям базы
                    # print(string_split)
                error_log_dump = json.dumps(fields.error_log)
                error_log_dump = "'" + error_log_dump + "'"
                # print(type(error_log_dump))
                # print(error_log_dump)
                # print(f'тест 2 -{fields.error_log}')
                cursor.execute(f"UPDATE Screen SET errors_log = {error_log_dump}  WHERE id = {screen.screen_id}")

                # except:
                #     print(f'Нужные данные из файла - {fields.name} не получены')
                #     listNotParsFile.append(fields.name)
                #     cursor.execute(
                #         f"UPDATE Screen SET required = 2  WHERE id = {screen.screen_id}")  # Поля не прочитались - статус 2
                # continue
                fields.name = ("'" + fields.name + "'")
                if fields.all_profit + fields.cart_profit + fields.cart_profit < 1:
                    # print(f'6) Понулям!')
                    cursor.execute(
                        f"UPDATE Screen SET usable = 0  WHERE name = {fields.name}")  # Поля равны нулю - статус 0
                else:

                    list_filds = [fields.date, fields.time, fields.date_time, fields.activ, fields.rait, fields.grate, fields.all_profit,
                                  fields.cash_profit, fields.cart_profit,
                                  fields.orders, fields.commission, fields.balance,
                                  str(fields.name), fields.verified]
                    # print(list_filds)
                    cursor.execute("INSERT INTO Fields VALUES(null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                   list_filds)
                    fields.name = fields.name.replace("'", "")
                    cursor.execute('UPDATE Screen SET readed = ? WHERE name = ?', (True, fields.name))

print(f'Готово! \n ')

Screen.notReadedFilesInBase(screen)

question = input('Проверить базу на наличие задвоенных данных и сформировать окончательную таблицу (д\y - да) - ')
if question == 'y' or question == 'д':
    checkduble()
