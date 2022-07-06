import psycopg2
from config import URI

db = psycopg2.connect(URI, sslmode="require")
cursor = db.cursor()


def psql_create():
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS users "
                       "(id TEXT PRIMARY KEY, username TEXT, fullname TEXT);")
        db.commit()
    except:
        cursor.execute("rollback")
        cursor.execute("CREATE TABLE IF NOT EXISTS users "
                       "(id TEXT PRIMARY KEY, username TEXT, fullname TEXT);")
        db.commit()


async def psql_command_insert(state):
    async with state.proxy() as data:
        print(tuple(data.values()))
        cursor.execute("INSERT INTO menu VALUES "
                       "(?, ?, ?, ?, ?)", tuple(data.values()))
        db.commit()


async def psql_command_all():
    return cursor.execute("SELECT * FROM menu").fetchall()


async def psql_command_delete(id):
    cursor.execute("DELETE FROM menu WHERE id == ?", (id,))
    db.commit()


async def psql_commands_get_all_id():
    return cursor.execute("SELECT id FROM menu").fetchall()
