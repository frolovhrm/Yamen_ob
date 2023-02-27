import sqlite3 as sq
import datetime

base_name = 'yamen_ob.db'
shift = '03:00:00'


def checkduble():
    activ = 0
    rait = 0.0
    grate = 0
    all_profit = 0.0
    cart_profit = 0.0
    cash_profit = 0.0
    orders = 0
    commission = 0.0
    mileage = 0
    balance = 0.0
    with sq.connect(base_name) as con:
        cursor = con.cursor()
        cursor.execute("SELECT id, date, time FROM Fields WHERE verified = 0")
        listcount = cursor.fetchall()

        for i in listcount:
            id_ = int(i[0])
            new_date = i[1]
            new_time = i[2]
            date_obj = datetime.datetime.strptime(f'{new_date} {new_time}', '%Y-%m-%d %H:%M:%S')
            print(date_obj)
            min_date_time = datetime.datetime.strptime(f'{new_date} {shift}', '%Y-%m-%d %H:%M:%S')
            max_date_time = min_date_time + datetime.timedelta(days=1)
            print(f'min_date - {min_date_time}')
            print(f'max_time - {max_date_time}')
            if date_obj > min_date_time or date_obj < max_date_time:
                list_fields = f"SELECT activ, rait, grate, all_profit, cash_profit, cart_profit, orders, commission," \
                              f" mileage, balance FROM Fields WHERE id = {id_}"
                cursor.execute(list_fields)
                fields = cursor.fetchone()
                print(f'id - {id_}')
                # print(f'date - {date}')
                # print(f'new_date - {new_date}')
                # print(f'new_time - {new_time}')
                print(fields)

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
                if mileage < fields[8]:
                    mileage = fields[8]
                if balance < fields[9]:
                    balance = fields[9]

            print(fields)
            # помечаем запись как проверенную
            # ver = f"UPDATE Fields SET verified = 1 WHERE id = {id_}"
            # cursor.execute(ver)

            if activ + rait + grate > 1:  # Пишем данные в базу новой строкой
                # s = f"INSERT INTO Truedate VALUES(null, '{new_date}', {activ}, {rait}, {grate}, {all_profit}," \
                #     f" {cash_profit}, {cart_profit}, {orders}, {commission}, {mileage}, {balance}) "
                # cursor.execute(s)
                s = "пишем"
            else:
                s = "пустая сторока"
            print(s)


print('Финальные данные сохранены в базе')

if __name__ == '__main__':
    checkduble()
