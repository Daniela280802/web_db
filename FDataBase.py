import psycopg2
from psycopg2.extras import DictCursor


# получение всех доступных заданий из бд
def getTaskAnounce(db):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM task ORDER BY task_id")
            res = cursor.fetchall()
            if res:
                return res
    except Exception as e:
        print(e)
        print("Ошибка в получении заданий.")

    return []


# получение всех клиентов из бд
def getClientAnounce(con):
    try:
        with con.cursor(cursor_factory=DictCursor) as cursor:

            cursor.execute("SELECT * FROM client ORDER BY client_id")
            res = cursor.fetchall()
            if res:
                return res
    except Exception as e:
        print(e)
        print("Ошибка в получении клиентов.")

    return []


# поиск клиента по его id
def findClientById(client_id, db):
    try:
        with db.cursor() as cursor:

            cursor.execute(f'SELECT * FROM client WHERE client_id={client_id}')
            res = cursor.fetchone()
            if res:
                return res
    except Exception as e:
        print(e)
        print("Ошибка получения клиента по его id.")

    return False


# добавление нового задания в бд
def addtask(finish, task_desc, contract, author, executor, client, priority, con):
    try:
        with con.cursor() as cursor:
            cursor.execute("CALL new_task(%s,%s,%s,%s,%s,%s,%s)",
                           (finish, task_desc, contract, author, executor, client, priority))
            con.commit()

    except Exception as e:
        print("Ошибка добавления задачи " + e)
        return False

    return True


# получить задание по его id из бд
def getTask(id, db):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM task WHERE task_id =%(task_id)s",
                           {'task_id': id})
            res = cursor.fetchone()
            if res:
                return res
    except Exception as e:
        print(e)
        print("Ошибка получения таска из БД")
    return (False, False)


#  для менеджера и обычного сотрудника функции изменения задания разные.
def updateTask(status, executor, priority, description, finish, db, task_id, is_manager):
    try:
        with db.cursor() as cursor:
            if is_manager:
                cursor.execute(f'''UPDATE task SET task_description = '{description}',
                                task_status = '{status}',executor_id = '{executor}',
                                priority = '{priority}',finish_date = '{finish}',
                                WHERE task_number = '{task_id}' ''')
            else:
                cursor.execute(f'''UPDATE task SET task_description = '{description}',
                                    task_status = '{status}',task_priority = '{priority}',
                                    finish_date = '{finish}'
                                    WHERE task_id = '{task_id}' ''')

    except Exception as e:
        print(e)
        print("Ошибка получения таска из БД")


# добавление нового пользователя в бд
def addUser(name, login, password, phone, email, role, con):
    try:
        id_role = 0
        if role == 'worker':
            id_role = 2
        if role == 'master':
            id_role = 1
        with con.cursor() as cursor:
            cursor.execute("CALL create_user(%s,%s,%s,%s,%s,%s)", (name, email, phone, login, password, id_role))
            con.commit()
    except Exception as e:
        print(e)
        print("Ошибка добавления пользователя в бд")
        return False

    return True


# получение пользователя из бд по его Id
def getUser(user_id, db):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM staff WHERE staff_id = %(staff_id)s",
                           {'staff_id': user_id})
            res = cursor.fetchone()
            if not res:
                print("Пользовтель не найден.")
                return False
            return res
    except Exception as e:
        print(e)
        print("Ошибка получения данных из бд.")
    return False


# получение пользователя из бд по его логину
def getUserByLogin(login, con):
    try:
        with con.cursor(cursor_factory=DictCursor) as cursor:
            try:
                cursor.execute("SELECT * FROM staff WHERE staff_login = %(staff_login)s",
                               {'staff_login': login})
                res = cursor.fetchone()
            except psycopg2.OperationalError as e:
                print(e)
                res = False
            return res

    except Exception as e:
        print(e)
        print("Ошибка получения пользователя из бд.")

    return False


# создание отчета по заданиям
def getReport(path, db):
    try:
        with db.cursor() as cursor:
            cursor.execute(f'''CALL export_report_json('{path}')''')

    except Exception as e:
        print(e)
        print("Ошибка вызова функции генерации отчета.")
        return False

    return True


# создание отчета по заданиям для конкретного пользователя
def get_report_task(path, start, finish, id, db):
    try:
        with db.cursor() as cursor:
            cursor.execute(f'''CALL export_data_csv ('{id}','{start}','{finish}','{path}')''')

    except Exception as e:
        print(e)
        print("Ошибка вызова функции генерации отчета по сотруднику.")
        return False

    return True
