import sqlite3


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print("База данных подключена!")

    db.execute("CREATE TABLE IF NOT EXISTS menu "
               "(id INTEGER NOT NULL PRIMARY KEY, "
               "photo TEXT, name TEXT, description TEXT, price INTEGER)")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        print(tuple(data.values()))
        cursor.execute("INSERT INTO menu VALUES "
                       "(?, ?, ?, ?, ?)", tuple(data.values()))
        db.commit()


async def sql_command_all():
    return cursor.execute("SELECT * FROM menu").fetchall()


async def sql_command_delete(id):
    cursor.execute("DELETE FROM menu WHERE id == ?", (id,))
    db.commit()


async def sql_commands_get_all_id():
    return cursor.execute("SELECT id FROM menu").fetchall()
