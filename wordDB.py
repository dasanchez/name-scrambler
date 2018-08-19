import sqlite3

class wordDB():

    def __init__(self):
        self._db_connection = sqlite3.connect(':memory:')
        self._db_cur = self._db_connection.cursor()

    def query(self, query):
        return self._db_cur.execute(query)

    def commit(self):
        return self._db_connection.commit()

    def __del__(self):
        self._db_connection.close()