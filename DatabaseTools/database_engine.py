import sqlite3

from topic.all_topics import *

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
            print('Ошибка при поиске challenge в базе данных по title', e)
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

    def load_test_params(self, challenge_id):
        try:
            cur = self.db_con.cursor()
            select_query = "SELECT class_name, count_task FROM challenge_items WHERE challenge = ?"
            result = cur.execute(select_query, (challenge_id,)).fetchall()
        except Exception as e:
            print('Ошибка при поиске challenge в базе данных по title', e)
            return -1
        items_for_test = []
        for elem in result:
            class_name = elem[0]
            for i in range(elem[1]):
                item = eval(f'{class_name}()')
                items_for_test.append(item)
        data_challenge = self.search_info_for_challenge(challenge_id)
        if data_challenge[2]:
            random.shuffle(items_for_test)
        return ((data_challenge[1], data_challenge[3]), items_for_test)

    def search_info_for_challenge(self, challenge_id):
        try:
            cur = self.db_con.cursor()
            select_query = "SELECT * FROM challenges WHERE challenge_id = ?"
            result = cur.execute(select_query, (challenge_id,)).fetchall()
        except Exception as e:
            print('Ошибка при поиске challenge в базе данных по challenge_id', e)
            return -1
        if len(result) == 0:
            print(f'Ошибка базы данных. Не найдено ни одного challenge с id={challenge_id}!')
            self.close()
            return -1
        return result[0]

    def search_all_challenges(self):
        try:
            cur = self.db_con.cursor()
            select_query = "SELECT * FROM challenges"
            result = cur.execute(select_query).fetchall()
        except Exception as e:
            print('Ошибка при поиске всех challenge в базе данных', e)
            return -1
        if len(result) == 0:
            print(f'Ошибка базы данных. Не найдено ни одного challenge!')
            self.close()
            return -1
        return result


    def close(self):
        self.db_con.close()



