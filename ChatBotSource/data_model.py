import sqlite3

class DbConnect():
    def __init__(self):
        self.connection = sqlite3.connect("train_db.sqlite")
        self.cursor = self.connection.cursor()

DbConnect()