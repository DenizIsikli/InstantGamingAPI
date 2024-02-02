import sqlite3


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()

    @staticmethod
    def create_connection(db_name):
        try:
            conn = sqlite3.connect(db_name, check_same_thread=False)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise e

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Media (
                    name TEXT NOT NULL,
                    year INTEGER,
                    duration TEXT,
                    link TEXT
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def add_media(self, media):
        try:
            cursor = self.conn.cursor()

            media_data = [
                (media.name, media.year, media.duration, media.link)
                for media in media
            ]

            cursor.executemany('''
                INSERT INTO Media (name, year, duration, link)
                VALUES (?, ?, ?, ?)
            ''', media_data)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding media: {e}")

    def get_media_by_name(self, media_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Media WHERE name = ?", (media_name,))
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Error retrieving media: {e}")
            return None

    def delete_media(self, media_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Media WHERE name = ?", (media_name,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting media: {e}")

    def clear_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Media")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error clearing table: {e}")

    def close_connection(self):
        self.conn.close()


if __name__ == '__main__':
    db = Database('Quitt.db')
    db.clear_table()
    db.close_connection()
