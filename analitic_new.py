import sqlite3 as sq
import datetime
from tqdm import tqdm

base_name = 'yamen_ob.db'
one_date = '2021-07-21'
shift_time = '03:00:00'
null_time = '00:00:00'

list_all_date = []


def checkduble():
    activ = 0
    rait = 0.0
    grate = 0
    all_profit = 0.0
    cart_profit = 0.0
    cash_profit = 0.0
    orders = 0
    commission = 0.0
    balance = 0.0

    with sq.connect(base_name) as con:
        cursor = con.cursor()
        cursor.execute("SELECT DISTINCT date, date_time FROM Fields WHERE verified = 0")
        list_date = cursor.fetchall()

    if len(list_date) > 0:
        for i in list_date:
            date_old = i[0]
            date_time = datetime.datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S')
            # print(date_old, date_time)
            null_date_time = datetime.datetime.strptime(f'{date_old} {null_time}', '%Y-%m-%d %H:%M:%S')
            shift_date_time = datetime.datetime.strptime(f'{date_old} {shift_time}', '%Y-%m-%d %H:%M:%S')
            if null_date_time < date_time < shift_date_time:
                date_new = date_time - datetime.timedelta(days=1)
                date = str(date_new.date())
            else:
                date = i[0]
            # print(date_old, date)
            list_all_date.append(date)
    # print(f'список всех дат {list_all_date}')

    len_list_all_date = len(list_all_date)

    if len_list_all_date > 0:
        for num in tqdm(range(len_list_all_date)):

            min_date_time = datetime.datetime.strptime(f'{list_all_date[num]} {shift_time}', '%Y-%m-%d %H:%M:%S')
            max_date_time = min_date_time + datetime.timedelta(days=1)

            with sq.connect(base_name) as con:
                cursor = con.cursor()
                cursor.execute(
                    "SELECT id, date_time FROM Fields WHERE verified = 0 AND (date_time > ? AND date_time < ?)",
                    (min_date_time, max_date_time,))
                list_one_date = cursor.fetchall()
                # print(f'{i} - {list_one_date}')
            if len(list_one_date) == 0:
                continue

            # print(f'list_one_date - {list_one_date} - {i}')
            for d in list_one_date:
                with sq.connect(base_name) as con:
                    cursor = con.cursor()
                    list_fields = f"SELECT activ, rait, grate, all_profit, cash_profit, cart_profit, orders, commission," \
                                  f" balance FROM Fields WHERE id = {d[0]}"
                    cursor.execute(list_fields)
                    fields = cursor.fetchone()
                # print(f' id - {d[0]} - {d[1]} - fields2 - {fields}')

                if activ < int(fields[0]):
                    activ = fields[0]
                if rait < fields[1]:
                    rait = fields[1]
                if grate < fields[2]:
                    grate = fields[2]
                if all_profit < fields[3]:
                    all_profit = fields[3]
                if cash_profit < fields[4]:
                    cash_profit = fields[4]
                if cart_profit < fields[5]:
                    cart_profit = fields[5]
                if orders < int(fields[6]):
                    orders = fields[6]
                if commission < fields[7]:
                    commission = fields[7]
                if balance < fields[8]:
                    balance = fields[8]

                with sq.connect(base_name) as con:  # помечаем запись как проверенную
                    cursor = con.cursor()
                    ver = f"UPDATE Fields SET verified = 1 WHERE id = {d[0]}"
                    cursor.execute(ver)

            if activ + rait + grate > 0:  # Пишем данные в базу новой строкой
                s = f"INSERT INTO Truedate VALUES(null, '{list_all_date[num]}', {activ}, {rait}, {grate}, {all_profit}," \
                    f" {cash_profit}, {cart_profit}, {orders}, {commission}, {balance}) "
                # print(s)
                with sq.connect(base_name) as con:  # помечаем запись как проверенную
                    cursor = con.cursor()
                    cursor.execute(s)
            activ = 0
            rait = 0.0
            grate = 0
            all_profit = 0.0
            cart_profit = 0.0
            cash_profit = 0.0
            orders = 0
            commission = 0.0
            balance = 0.0
    print('Финальные данные сохранены в базе, таблица сформирована.')


if __name__ == '__main__':
    checkduble()

