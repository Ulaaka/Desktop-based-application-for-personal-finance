import mysql.connector

class database:

    def __init__(self):

        self.db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "Ulaaka_1223",
            database ="finance_db"
        )

        self.cursor = self.db.cursor(buffered=True)

db  = database()