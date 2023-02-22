import sqlite3 as sq
import datetime
#
base_name = 'yamen_ob.db'

#
# with sq.connect(base_name) as con:
#     cursor = con.cursor()
#     cursor.execute('UPDATE Fields SET verified = 0')

    # cursor.execute("""CREATE TABLE IF NOT EXISTS Truedate (
    # id INTEGER PRIMARY KEY AUTOINCREMENT,
    # date TEXT,
    # activ INTEGER,
    # rait REAL,
    # grate INTEGER,
    # all_profit REAL,
    # cash_profit REAL,
    # cart_profit REAL,
    # orders INTEGER,
    # commission INTEGER,
    # mileage INTEGER,
    # balance REAL
    #
    # )""")
#
# print('Р' == 'Р')
#
#
# print('‚' == ',') '%Y %m %d %H %M %S'

# yyyy = 2024
#
#
# hh = '03'
# mm = '00'
# ss = '00'
#
# datetime_low = str(f'{yyyy} 01 02 {hh} {mm} {ss}')
#
# print(datetime_low)
#
# print(datetime.datetime.strptime(datetime_low, '%Y %m %d %H %M %S'))

with sq.connect(base_name) as con:
    cursor = con.cursor()
    cursor.execute(
        "SELECT id, date FROM Fields WHERE verified = 0")
    getdatelist = cursor.fetchall()

# print(getdatelist)

for date in getdatelist:
    date_str = date[1]

    date_time_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')   #'%Y %m %d %H %M %S'
    # print(date_time_obj.date(), date_time_obj)
    date_now = date_time_obj.date()
    time_now = date_time_obj.time()
    print(date_now, time_now)
    # list_dates = []




