import sqlite3
import contextlib

class DbInitialization:

    def init_jokes(self):
        with contextlib.closing(sqlite3.connect('db.sqlite3')) as con:
            with con as cur:
               cur.execute('''
                   CREATE TABLE IF NOT EXISTS jokes (
                        id INTEGER PRIMARY KEY,
                        joke TEXT
                   )
               ''')

    def init_users(self):
        with contextlib.closing(sqlite3.connect('db.sqlite3')) as con:
            with con as cur:
               cur.execute('''
                   CREATE TABLE IF NOT EXISTS users (
                        chat_id varchar(30) PRIMARY KEY,
                        username varchar(255)
                   )
               ''')

    def init_user_views(self):
        with contextlib.closing(sqlite3.connect('db.sqlite3')) as con:
            with con as cur:
                cur.execute('''
                          CREATE TABLE IF NOT EXISTS user_views (
                               user_id varchar(30) PRIMARY KEY,
                               joke_id INTEGER,
                               FOREIGN KEY(user_id) REFERENCES users(chat_id),
                               FOREIGN KEY(joke_id) REFERENCES jokes(id)
                          )
                          
                      ''')

    def init(self):
        self.init_jokes()
        self.init_users()
        self.init_user_views()


class DbQuery:

    def insert_joke(self, joke_text):
        with contextlib.closing(sqlite3.connect('db.sqlite3')) as con:
            with con as cur:
               cur.execute(f"""
                       INSERT INTO jokes (joke) VALUES (?);
                     """,
                    (str(joke_text),)
                )
    def delete_joke(self, id):
        with contextlib.closing(sqlite3.connect('db.sqlite3')) as con:
            with con as cur:
               cur.execute(f"""
                       DELETE FROM jokes WHERE id = (?);
                     """,
                    (id,)
                )
    def add_user(self, username):
        with contextlib.closing(sqlite3.connect('db.sqlite3')) as con:
            with con as cur:
               cur.execute(f"""
                       INSERT or IGNORE INTO users (username) VALUES (?);
                     """,
                    (username,)
                )

    def read_joke(self, user_id, joke_id):
        with contextlib.closing(sqlite3.connect('db.sqlite3')) as con:
            with con as cur:
               cur.execute(f"""
                       INSERT INTO user_views (user_id, joke_id) VALUES (?, ?);
                     """,
                    (user_id, joke_id)
                )

    def retrieve_joke_by_id(self, joke_id):
        res = None
        with contextlib.closing(sqlite3.connect('db.sqlite3')) as con:
            with con as cur:
                query = cur.execute(f"""SELECT * FROM jokes;""")
                res = query.fetchall()
        if joke_id >=  len(res):
            return "Извините, все шутки закончились"
        else:
            return res[joke_id][1]
    def get_random_joke(self, user_id):
        with contextlib.closing(sqlite3.connect('db.sqlite3')) as con:
            with con as cur:
                query = cur.execute(f"""
                    SELECT id, joke FROM jokes
                    WHERE id NOT IN (
                        SELECT joke_id FROM user_views 
                        WHERE user_id=?
                    ) 
                    ORDER BY RANDOM() 
                    LIMIT 1;
                """,
                (user_id,))
                full_obj = query.fetchone()
                cur.execute(f"""
                    INSERT INTO user_views VALUES (?, ?)
                """, (user_id, full_obj[0]))
                return (full_obj[0], full_obj[1])
    def reset(self, user_id):
        with contextlib.closing(sqlite3.connect('db.sqlite3')) as con:
            with con as cur:
                cur.execute(f""" DELETE FROM user_views WHERE user_id = ?""", (user_id,))