from django.db import connections

class DatabaseManager:
    def __init__(self, database_name="default"):
        self.database_name = database_name

    def __enter__(self):
        self.connection = connections[self.database_name]
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()

    def execute(self, query):
        self.cursor.execute(query)
        
    def fetchall(self):
        return self.cursor.fetchall()
    
    def fetchone(self):
        return self.cursor.fetchone()
        