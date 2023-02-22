import sqlite3 as sq

# "SELECT date(date), COUNT(*)  FROM Fields WHERE verified = 0  GROUP BY date(date) HAVING COUNT(*) > 1")

base_name = 'yamen_ob.db'

n_date = '2021-08-07'

with sq.connect(base_name) as con:
    cursor = con.cursor()
    cursor.execute("SELECT id, date "
                   "FROM Fields WHERE verified = 0 and date(date) = ?", ('2021-08-07',))
    list_count = cursor.fetchall()
    for item in list_count:
        print(item)
