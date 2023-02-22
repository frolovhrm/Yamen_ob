import datetime
import sqlite3 as sq
import os
import pytesseract
import cv2
from creat_db_ob import createNewBase
from readTextToFields import readTextToFields
from readTextToFields2 import readTextToFields2
from tqdm import tqdm
from analitic import checkduble

screenshot_path = 'C:\\Python projects\\Screenshort\\'
base_name = 'yamen_ob.db'
tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

createNewBase()


class Screen:
    def __int__(self):
        self.screen_id = ''
        self.name = ''

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
        print(f'... найдено и добавленно в базу новых файлов - {count} \n')

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
        self.time = 'null'  # 2
        self.activ = 0  # 4
        self.rait = 0  # 5
        self.grate = 0  # 6
        self.all_profit = 0.0  # 7
        self.cash_profit = 0.0  # 8
        self.cart_profit = 0.0  # 9
        self.orders = 0  # 10
        self.commission = 0.0  # 12
        self.mileage = 0  # 13
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
        # print(type(date_time_str))
        # date_time_obj = datetime.strptime(date_time_str, '%Y %m %d %H %M %S')
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')
        # print(type(date_time_obj))
        # print(f'дата: {date_time_obj.date()}')
        # print(f'время: {date_time_obj.time()}')
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
        fields.mileage = 0
        fields.balance = 0.0

    def getNewFile(self):
        with sq.connect(base_name) as con:  # Расшифровываем и раскладываем по полям базы
            cursor = con.cursor()
            # try:
            cursor.execute(
                "SELECT id, name FROM Screen WHERE readed = '0' AND usable = '1' LIMIT 1")  # Получаем первую запись из базы
            getfilename = cursor.fetchone()
            fields.name = getfilename[1]
            screen.screen_id = getfilename[0]
            # print(f'2) Начало распознавания')
            string = Fields.readImagetoText(fields)
            # print(f'3) Распознали')
            # print(fields.name)
            # print(screen.screen_id)
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
                fields.date = str(Fields.nameToDate(fields.name))  # выделяем дату из имени
                # print(f"5) Дата = {fields.date}")
                if fields.date < '2022-04-04':
                    # print(f'5.1) old way')
                    readTextToFields(fields, string_split)  # Расшифровываем и раскладываем по полям базы
                    # print(string_split)
                else:
                    # print(f'5.2) new way')
                    readTextToFields2(fields, string_split)  # Расшифровываем и раскладываем по полям базы
                    # print(string_split)
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

                    list_filds = [fields.date, fields.time, fields.activ, fields.rait, fields.grate, fields.all_profit,
                                  fields.cash_profit, fields.cart_profit,
                                  fields.orders, fields.commission, fields.mileage, fields.balance,
                                  str(fields.name), fields.verified]
                    # print(list_filds)
                    cursor.execute("INSERT INTO Fields VALUES(null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                   list_filds)
                    fields.name = fields.name.replace("'", "")
                    cursor.execute('UPDATE Screen SET readed = ? WHERE name = ?', (True, fields.name))

print(f'Готово! \n ')
#
Screen.notReadedFilesInBase(screen)

question = input('Проверить базу на наличие задвоенных данных и сформировать окончательную таблицу (д\y - да) - ')
if question == 'y' or question == 'д':
    checkduble()

#
# print(f'Нераспарсеных файлов за сессию {len(listNotParsFile)}')
# for i in listNotParsFile:
#     print(i)
