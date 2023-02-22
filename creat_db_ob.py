import sqlite3 as sq


def createNewBase():
    with sq.connect('yamen_ob.db') as con:
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS Screen (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL,
        usable INTEGER NOT NULL DEFAULT 1,
        readed INTEGER NOT NULL DEFAULT 0,
        error_log TEXT,
        strline TEXT
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS Fields (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        time TEXT,
        activ INTEGER,
        rait REAL,
        grate INTEGER,
        all_profit REAL,
        cash_profit REAL,
        cart_profit REAL,
        orders INTEGER,
        commission INTEGER,
        mileage INTEGER,
        balance REAL,
        name TEXT NOT NULL,
        verified INTEGER NOT NULL DEFAULT 0     
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS Truedate (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        activ INTEGER,
        rait REAL,
        grate INTEGER,
        all_profit REAL,
        cash_profit REAL,
        cart_profit REAL,
        orders INTEGER,
        commission INTEGER,
        mileage INTEGER,
        balance REAL

        )""")

    # print('Новая база созданна')
