import sqlite3

from topic.all_topics import *

DATABASE_PATH = '../db/challenge.db'


class DatabaseEngine:
    def __init__(self):
        try:
            self.db_con = sqlite3.connect(DATABASE_PATH)
        except Exception as e:
            print('Ошибка при открытии бызы данных:', e)
            quit()

    def insert_challenge(self, title, mixed, learning):
        try:
            cur = self.db_con.cursor()
            insert_query = "INSERT INTO challenges(title, mixing, training) VALUES (?, ?, ?)"
            cur.execute(insert_query, (title, mixed, learning))
            self.db_con.commit()
        except Exception as e:
            print(e)
            self.close()
            return -1

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
            self.close()
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

    def get_test_params(self, id_challenge):
        record_challenge = self.search_info_for_challenge(id_challenge)
        try:
            cur = self.db_con.cursor()
            select_query = "SELECT module_name, class_name, count_task FROM challenge_items WHERE challenge = ?"
            result = cur.execute(select_query, (id_challenge,)).fetchall()
        except Exception as e:
            print('Ошибка при поиске challenge в базе данных по title', e)
            return -1
        result.sort(key=lambda x: x[0])
        dict_result = dict()
        for module_name, class_name, count_task in result:
            if module_name not in dict_result:
                dict_result[module_name] = [(class_name, count_task)]
            else:
                dict_result[module_name].append((class_name, count_task))
        return record_challenge, dict_result

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
            self.close()
            return -1
        if len(result) == 0:
            print(f'Ошибка базы данных. Не найдено ни одного challenge!')
            self.close()
            return -1
        return result

    def update_challenges(self, field, value_field, id_challenge):
        try:
            cur = self.db_con.cursor()
            update_query = f"UPDATE challenges SET {field}='{value_field}' WHERE challenge_id = ?"
            cur.execute(update_query, (id_challenge,))
            self.db_con.commit()
            cur.close()
        except Exception as e:
            print('Ошибка изменении таблицы challenge в базе данных', e)
            self.close()
            return -1

    def delete_items_for_challenge(self, id_challenge):
        try:
            cur = self.db_con.cursor()
            delete_items_query = 'DELETE from challenge_items WHERE challenge = ?'
            cur.execute(delete_items_query, (id_challenge,))
            self.db_con.commit()
        except Exception as e:
            print(
                f'Ошибка при удалении из таблицы challenge_items записей с challenge={id_challenge}',
                e
            )
            self.close()
            return -1
        return 0

    def delete_challenge(self, id_challenge):
        res_value = self.delete_items_for_challenge(id_challenge)
        if res_value == -1:
            return -1
        try:
            cur = self.db_con.cursor()
            delete_query = 'DELETE from challenges WHERE challenge_id = ?'
            cur.execute(delete_query, (id_challenge,))
            self.db_con.commit()
        except Exception as e:
            print(
                f'Ошибка при удалении из таблицы challenges записи с challenge_id={id_challenge}', e)
            self.close()
            return -1
        return 0

    def close(self):
        self.db_con.close()



