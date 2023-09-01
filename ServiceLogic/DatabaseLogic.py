import sqlite3


class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect("swCamera_db.db", timeout=5)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE if not exists config (key TEXT, value TEXT)")

    def get_consumer_key(self):
        consumer_key = self.cursor.execute("select value from config where key = 'consumer_key'").fetchone()
        return consumer_key[0]

    def get_consumer_secret(self):
        consumer_secret = self.cursor.execute("SELECT value FROM config where key = 'consumer_secret'").fetchone()
        return consumer_secret[0]

    def check_is_consumer_in_db(self):
        consumer_key = self.cursor.execute("select value from config where key = 'consumer_key'").fetchall()
        consumer_secret = self.cursor.execute("select value from config where key = 'consumer_secret'").fetchall()
        if not consumer_key:
            self.cursor.execute("insert into config values ('consumer_key', "
                                "'CV5EFv5JYlwy3JTBI9dICuJgBTcfvEmgqmNquwPt')")
            self.connection.commit()
        if not consumer_secret:
            self.cursor.execute("insert into config values ('consumer_secret', "
                                "'fz3kdAJlw1VB9VutPDxtULE1ujvOLBzjekHZb18C')")
            self.connection.commit()



