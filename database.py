import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS
        products (
            "product_id"	INTEGER UNIQUE NOT NULL,
            "product_name"	TEXT UNIQUE NOT NULL ,
            "product_stock"	INTEGER NOT NULL,
	        PRIMARY KEY("product_id" AUTOINCREMENT)
        );
        """)
        self.conn.commit()

    def fetch_by_product_name(self, product_name):
        self.cur.execute(
            "SELECT rowid, product_id, product_name, product_stock FROM products WHERE product_name=?", (product_name,))
        row = self.cur.fetchall()
        return row


    def fetch_all_rows(self):
        self.cur.execute(
            """SELECT product_id, product_name, product_stock FROM products""")
        rows = self.cur.fetchall()
        return rows

    def fetch_by_rowid(self, rowid):
        self.cur.execute(
            "SELECT rowid, product_id, product_name, product_stock FROM products WHERE rowid=?", (rowid,))
        row = self.cur.fetchall()
        return row

    def fetch_by_product_id(self, product_id):
        self.cur.execute(
            "SELECT rowid, product_id, product_name, product_stock FROM products WHERE product_id=?", (product_id,))
        row = self.cur.fetchall()
        return row

    def insert(self, product_id, product_name, product_stock):
        self.cur.execute("""INSERT INTO products (product_id, product_name, product_stock) VALUES (?, ?, ?)""",
        (product_id, product_name, product_stock))
        self.conn.commit()

    def remove(self, product_id):
        self.cur.execute(
            "DELETE FROM products WHERE product_id=?", (product_id, ))
        self.conn.commit()

    def update(self, rowid, product_id, product_name, product_stock):
        self.cur.execute("""UPDATE products SET
            product_id=?,
            product_name=?,
            product_stock=?
            WHERE
            rowid=?
        """, (product_id, product_name, product_stock, rowid))
        self.conn.commit()

    # Defining a destructor to close connections
    def __del__(self):
        self.conn.close()

