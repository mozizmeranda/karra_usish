import sqlite3


class Database:

    def __init__(self, db_name="users.db"):
        self.path_to_db = db_name

    def connection(self):
        connection = sqlite3.connect(self.path_to_db)
        return connection

    def execute(self, sql: str, params: tuple = None, fetchone: bool = False, fetchall: bool = False,
                 commit: bool = False):
        if not params:
            params = tuple()

        connection = self.connection()
        cursor = connection.cursor()
        cursor.execute(sql, params)

        data = None

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




