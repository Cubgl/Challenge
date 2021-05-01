import sqlite3

DATABASE_PATH = '../db/challenge.db'


class DatabaseEngine:
    def __init__(self):
        self.db_con = sqlite3.connect(DATABASE_PATH)

    def insert_challenge(self, title, mixed, learning):
        try:
            cur = self.db_con.cursor()
            insert_query = "INSERT INTO challenges(title, mixing, training) VALUES (?, ?, ?)"
            cur.execute(insert_query, (title, mixed, learning))
            self.db_con.commit()
        except Exception as e:
            print(e)

    def insert_challenge_item(self, class_name, challenge_id, count_task, module_name):
        try:
            cur = self.db_con.cursor()
            insert_query = """INSERT INTO challenge_items(class_name, challenge, 
                                count_task, module_name) VALUES (?, ?, ?, ?)"""
            cur.execute(insert_query, (class_name, challenge_id, count_task, module_name))
            self.db_con.commit()
        except Exception as e:
            print('Ошибка при добавлении challenge_item в базу данных', e)

    def search_id_challenge(self, title):
        try:
            cur = self.db_con.cursor()
            select_query = "SELECT challenge_id FROM challenges WHERE title = ?"
            result = cur.execute(select_query, (title,)).fetchall()
        except Exception as e:
            print('Ошибка при добавлении challenge в базу данных', e)
            return -1
        if len(result) > 1:
            print(f'Ошибка базы данных. Найдено больше одного challenge с названием {title}!')
            self.close()
            return -1
        if len(result) == 0:
            print(f'Ошибка базы данных. Не найдено ни одного challenge с названием {title}!')
            self.close()
            return -1
        return result[0][0]

    def close(self):
        self.db_con.close()



