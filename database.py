import sqlite3


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    name TEXT NOT NULL,
                    price TEXT NOT NULL,
                    link TEXT
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def add_product(self, product):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO products (name, price, link)
                VALUES (?, ?, ?)
            ''', (product.name, product.price, product.link))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding product: {e}")

    def get_product_by_name(self, product_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM products WHERE name = ?", (product_name,))
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Error retrieving product: {e}")
            return None

    def update_product_price(self, product_name, new_price):
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE products SET price = ? WHERE name = ?", (new_price, product_name))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating product price: {e}")

    def delete_product(self, product_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM products WHERE name = ?", (product_name,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting product: {e}")

    def close_connection(self):
        self.conn.close()
