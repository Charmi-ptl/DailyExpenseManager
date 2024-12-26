import sqlite3
class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS expense_record (item_name text, item_price float, purchase_date date)"
        )
        # Add category column if it doesn't exist
        try:
            self.cur.execute("ALTER TABLE expense_record ADD COLUMN category TEXT")
        except sqlite3.OperationalError:
            pass  # Ignore if column already exists
        self.conn.commit()

    def fetchRecord(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def insertRecord(self, item_name, item_price, purchase_date):
        self.cur.execute("INSERT INTO expense_record VALUES (?, ?, ?)",
                         (item_name, item_price, purchase_date))
        self.conn.commit()

    def insertRecordWithCategory(self, item_name, item_price, purchase_date, category):
        self.cur.execute("INSERT INTO expense_record (item_name, item_price, purchase_date, category) VALUES (?, ?, ?, ?)",
                         (item_name, item_price, purchase_date, category))
        self.conn.commit()

    def fetchByCategory(self, category):
        self.cur.execute("SELECT * FROM expense_record WHERE category=?", (category,))
        return self.cur.fetchall()

    def updateCategory(self, rid, category):
        self.cur.execute("UPDATE expense_record SET category = ? WHERE rowid = ?", (category, rid))
        self.conn.commit()

    def removeRecord(self, rowid):
        self.cur.execute("DELETE FROM expense_record WHERE rowid=?", (rowid,))
        self.conn.commit()

    def updateRecord(self, item_name, item_price, purchase_date, rid):
        self.cur.execute("UPDATE expense_record SET item_name = ?, item_price = ?, purchase_date = ? WHERE rowid = ?",
                         (item_name, item_price, purchase_date, rid))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
