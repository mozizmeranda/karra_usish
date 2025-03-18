import sqlite3 as sq


class Database:

    def __init__(self, db_name="users.db"):
        self.path_to_db = db_name

    @property
    def connection(self):
        return sq.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()

        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        if commit:
            connection.commit()
        connection.close()

        return data

    def create_table(self):
        sql = "CREATE TABLE IF NOT EXISTS Users(id INT, name TEXT, number TEXT)"
        self.execute(sql, commit=True)

    def insert_into(self, id: int, name: str, number: str):
        sql = "INSERT OR IGNORE INTO Users(id, name, number) VALUES (?, ?, ?)"
        parameters = (id, name, number)
        self.execute(sql, parameters=parameters, commit=True)

    def get_all_users(self):
        sql = "SELECT id FROM Users"
        data = self.execute(sql, fetchall=True)
        return data


database = Database()

users = database.get_all_users()
for i in users:
    print(i)



