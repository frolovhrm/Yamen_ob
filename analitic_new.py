import sqlite3 as sq
import datetime
from tqdm import tqdm

base_name = 'yamen_ob.db'
shift_time = '03:00:00'  # максимальное время окончание смены за предидущую дату
null_time = '00:00:00'

list_all_date = []


def checkduble():
    with sq.connect(base_name) as con:
        cursor = con.cursor()
        cursor.execute("SELECT DISTINCT date, date_time FROM Fields WHERE verified = 0")
        list_date = cursor.fetchall()  # Собираем список всех уникальных дат в которые есть записи даннымх

    if len(list_date) > 0:  # Составляем список дат в которые начинались рабочие смены с учетом времени их окончания
        for i in list_date:
            date_old = i[0]
            date_time = datetime.datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S')
            null_date_time = datetime.datetime.strptime(f'{date_old} {null_time}', '%Y-%m-%d %H:%M:%S')
            shift_date_time = datetime.datetime.strptime(f'{date_old} {shift_time}', '%Y-%m-%d %H:%M:%S')
            if null_date_time < date_time < shift_date_time:
                date_new = date_time - datetime.timedelta(days=1)
                date = str(date_new.date())
            else:
                date = i[0]
            list_all_date.append(date)

    len_list_all_date = len(list_all_date)  # range для визуализации

    if len_list_all_date > 0:
        for num in tqdm(range(len_list_all_date)):
            activ = activ1 = activ2 = 0
            rait = rait1 = rait2 = 0.0
            grate = grate1 = grate2 = 0
            all_profit = all_profit1 = all_profit2 = 0.0
            card_profit = card_profit1 = card_profit2 = 0.0
            cash_profit = cash_profit1 = cash_profit2 = 0.0
            orders = orders1 = orders2 = 0
            commission = commission1 = commission2 = 0.0
            balance = balance1 = balance2 = 0.0
            tips = tips1 = tips2 = 0.0

            # вычисляем минимальное время/дата начала смены для  конкретной даты
            min_date_time = datetime.datetime.strptime(f'{list_all_date[num]} {shift_time}', '%Y-%m-%d %H:%M:%S')

            # вычисляем максимальное время/дата начала смены для конкретной даты
            max_date_time = min_date_time + datetime.timedelta(days=1)

            # Собираем список записей подходящих под это диапазон время/дата
            with sq.connect(base_name) as con:
                cursor = con.cursor()
                cursor.execute(
                    "SELECT id, date_time FROM Fields WHERE verified = 0 AND (date_time > ? AND date_time < ?)",
                    (min_date_time, max_date_time,))
                list_one_date = cursor.fetchall()
            if len(list_one_date) == 0:
                continue

            # раскладываем его по полям
            for d in list_one_date:
                with sq.connect(base_name) as con:
                    cursor = con.cursor()
                    list_fields = f"SELECT activ, rait, grate, all_profit, cash_profit, card_profit, orders, commission," \
                                  f" balance, tips FROM Fields WHERE id = {d[0]}"
                    cursor.execute(list_fields)
                    fields = cursor.fetchone()
                file_date_time = datetime.datetime.strptime(f'{d[1]}', '%Y-%m-%d %H:%M:%S')
                file_date = file_date_time.date()

                # учитывем, что для каждой смены могут быть данные из разных дат
                if str(list_all_date[num]) == str(file_date):
                    if activ1 < int(fields[0]):
                        activ1 = fields[0]
                    if rait1 < fields[1]:
                        rait1 = fields[1]
                    if grate1 < fields[2]:
                        grate1 = fields[2]
                    if all_profit1 < fields[3]:
                        all_profit1 = fields[3]
                    if cash_profit1 < fields[4]:
                        cash_profit1 = fields[4]
                    if card_profit1 < fields[5]:
                        card_profit1 = fields[5]
                    if orders1 < int(fields[6]):
                        orders1 = fields[6]
                    if commission1 < fields[7]:
                        commission1 = fields[7]
                    if balance1 < fields[8]:
                        balance1 = fields[8]
                    if tips1 < fields[9]:
                        tips1 = fields[9]
                else:
                    if activ2 < int(fields[0]):
                        activ2 = fields[0]
                    if rait2 < fields[1]:
                        rait2 = fields[1]
                    if grate2 < fields[2]:
                        grate2 = fields[2]
                    if all_profit2 < fields[3]:
                        all_profit2 = fields[3]
                    if cash_profit2 < fields[4]:
                        cash_profit2 = fields[4]
                    if card_profit2 < fields[5]:
                        card_profit2 = fields[5]
                    if orders2 < int(fields[6]):
                        orders2 = fields[6]
                    if commission2 < fields[7]:
                        commission2 = fields[7]
                    if balance2 < fields[8]:
                        balance2 = fields[8]
                    if tips2 < fields[9]:
                        tips2 = fields[9]

                if activ2 > 0:
                    activ = activ2
                else:
                    activ = activ1

                if rait2 > 0:
                    rait = rait2
                else:
                    rait = rait1

                if grate2 > 0:
                    grate = grate2
                else:
                    grate = grate1

                if balance2 > 0:
                    balance = balance2
                else:
                    balance = balance1

                all_profit = round(all_profit1 + all_profit2, 2)
                cash_profit = cash_profit1 + cash_profit2
                card_profit = card_profit1 + card_profit2
                orders = orders1 + orders2
                commission = commission1 + commission2
                tips = tips1 + tips2

                with sq.connect(base_name) as con:  # помечаем запись как проверенную
                    cursor = con.cursor()
                    ver = f"UPDATE Fields SET verified = 1 WHERE id = {d[0]}"
                    cursor.execute(ver)

            if activ + rait + grate >= 0:  # Пишем консолидированые данные в новую таблицу
                s = f"INSERT INTO Truedate VALUES(null, '{list_all_date[num]}', {activ}, {rait}, {grate}, {all_profit}," \
                    f" {cash_profit}, {card_profit}, {orders}, {commission}, {balance}, {tips}) "
                with sq.connect(base_name) as con:  # помечаем запись как проверенную
                    cursor = con.cursor()
                    cursor.execute(s)

    print('Финальные данные сохранены в базе, таблица сформирована.')


if __name__ == '__main__':
    checkduble()
