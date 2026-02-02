import sqlite3


class sqlite_connection:
    def __init__(self, path):
        self.path = path
        
    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        return self.connection
    
    def __exit__(self, exception_type, exception_value, exception_tb):
        if exception_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.connection.close()
        return False
    