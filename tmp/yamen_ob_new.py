import json
import os
import sqlite3 as sq

from creat_db_ob import createNewBase
from screen_reader import ScreenRead
from fields_reader import Fields, fields

from readTextToFields import readTextToFields
from readTextToFields2 import readTextToFields2
from readTextToFields3 import readTextToFields3
from analitic_new import checkduble

from tqdm import tqdm

base_name = 'yamen_ob.db'
tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
screenshot_path = 'C:\\Python projects\\Screenshort\\'


def find_new_files():  # Отбирает подходящие файлы для сканирования и кладет их имена в базу
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
                            f"INSERT INTO Screen VALUES(null, {screen.name}, "
                            f"1, 0, null, null)")
                        count += 1
    print(f'... найдено подходящих для дальнейшей работы и добавленно в базу - {count} файлов \n')


def get_notreaded_files():  # Считает кол-во необработаных скринов в базе
    with sq.connect(base_name) as con:  # Проверяем количество доступных для расшифровки файлов
        cursor = con.cursor()
        cursor.execute("SELECT COUNT (readed) FROM Screen WHERE readed = '0' AND usable = '1'")
        count = cursor.fetchone()
        count_files = count[0]
        return count_files


def save_results(): # записывает в базу прочитанные данные по полям помечает обработаные файлы
    with sq.connect(base_name) as con:
        cursor = con.cursor()
        print(f"Ошибка с файлом - {fields.name}, {error_log_dump}")
        cursor.execute(f"UPDATE Screen SET errors_log = {error_log_dump}  WHERE name = {fields.name}")
        fields.name = ("'" + fields.name + "'")
        if fields.all_profit + fields.cash_profit + fields.card_profit + fields.activ + fields.orders < 1:
            cursor.execute(
                f"UPDATE Screen SET usable = 0  WHERE name = {fields.name}")  # Если данных нет ставим пригодность - 0
        else:
            list_filds = [fields.date, fields.time, fields.date_time, fields.activ, fields.rait, fields.grate,
                          fields.all_profit, fields.cash_profit, fields.card_profit,
                          fields.orders, fields.commission, fields.balance, fields.tips,
                          str(fields.name), fields.verified]
            cursor.execute("INSERT INTO Fields VALUES(null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           list_filds)
            fields.name = fields.name.replace("'", "")
            cursor.execute('UPDATE Screen SET readed = ? WHERE name = ?', (True, fields.name))


createNewBase()
screen = ScreenRead()
find_new_files()

notReaded_count = get_notreaded_files()

question = 0
if notReaded_count > 0:
    try:
        print(f'Всего файлов пригодных для расшифровки в базе - {notReaded_count}')
        question = int(input('Сколько файлов расшифровать? - '))
    except ValueError:
        print('... ввод не корректен,\nКонец ')
        quit()

    if question == 0:
        quit()

    if question <= notReaded_count:

        # tqdm
        for i in tqdm(range(question)):
            Fields.make_null_fields(fields)  # Сбрасываем значение полей на ноль
            string_split = Fields.getNewFile(fields)  # Выбираем файл для расшифровки, и переводим его в сплит строку

            datetime_obj = Fields.name_to_date(fields.name)  # выделяем дату и время из имени
            fields.date_time = datetime_obj
            fields.date = str(datetime_obj.date())
            fields.time = str(datetime_obj.time())

            if fields.date < '2022-04-04':  # выбераем версию парсера и раскладываем данные по полям
                readTextToFields(fields, string_split)
            if fields.date >= '2023-04-08':
                readTextToFields3(fields, string_split)
            else:
                readTextToFields2(fields, string_split)
            error_log_dump = json.dumps(fields.error_log)
            error_log_dump = "'" + error_log_dump + "'"

            save_results()

    print(f'Готово! \n ')

# get_notreaded_files()

question2 = input('Проверить базу на наличие задвоенных данных и сформировать окончательную таблицу (д\y - да) - ')
if question2 == 'y' or question2 == 'д':
    checkduble()
