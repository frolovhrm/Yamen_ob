def decor(func):
    def wrapper(a):
        print(a)
        func(a)

    return wrapper


@decor
def fun(a):
    b = a ** 2
    print(b)


fun(2)

# cur.execute("""CREATE TABLE IF NOT EXISTS Truedate (
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# date TEXT,
# day INTEGER,
# month INTEGER,
# year INTEGER,
# activ INTEGER,
# rait REAL,
# grate INTEGER,
# all_profit REAL,
# cash_profit REAL,
# card_profit REAL,
# orders INTEGER,
# commission INTEGER,
# balance REAL,
# tips REAL
#
# )""")

# "SELECT date(date), COUNT(*)  FROM Fields WHERE verified = 0  GROUP BY date(date) HAVING COUNT(*) > 1")

# base_name = 'yamen_ob.db'
#
# squares = [1, 4, 9, 16, 25]
#
# fig, ax = plt.subplots()
# ax.plot(squares)
#
# plt.show()


# n_date = '2021-08-07'
#
# id_list = [1377, 1378, 1379]
# with sq.connect(base_name) as con:
#     for i in id_list:
#         with sq.connect(base_name) as con:
#             cursor = con.cursor()
#             ver = f"UPDATE Screen SET usable = 1, readed = 0 WHERE id = {i}"
#             cursor.execute(ver)

#     cursor = con.cursor()
#     ver = f"ALTER TABLE Fields ADD COLUMN tips"
#     cursor.execute(ver)


#     # cursor = con.cursor()
#     # cursor.execute("SELECT id, date "
#     #                "FROM Fields WHERE verified = 0 and date(date) = ?", ('2021-08-07',))
#     # list_count = cursor.fetchall()
#     # for item in list_count:
#     #     print(item)
#
#     cursor = con.cursor()
#     ver = f"UPDATE Fields SET verified = 0 "
#     cursor.execute(ver)
# # #
#     cursor = con.cursor()
#     ver = f"DELETE FROM Truedate "
#     cursor.execute(ver)

# id_list = [21, 22, 23, 24, 25, 26]
#
# for i in id_list:
#     with sq.connect(base_name) as con:
#         cursor = con.cursor()
#         ver = f"UPDATE Fields SET verified = 0 WHERE id = {i}  "
#         cursor.execute(ver)
