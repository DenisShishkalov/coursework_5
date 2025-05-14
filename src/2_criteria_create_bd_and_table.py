import psycopg2


class CreateDBandTables:
# def create_connection():
#     """Функция, создающая соединение с БД """
#     try:
#         connection = psycopg2.connect(
#             host='localhost',
#             database='coursework_5',
#             user='postgres',
#             password='123')
#         cursor = connection.cursor()
#         print("Успешное подключение к базе данных")
#
#     except Exception as e:
#         raise RuntimeError(f'Ошибка подключения к БД: {e}')

    @staticmethod
    def create_database(data_connect: dict, db_name: str) -> None:
        """Создание базы данных, если ее не существует"""
        try:
            conn = psycopg2.connect(**data_connect)
            conn.autocommit = True

            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE {db_name};")

        except Exception as e:
            print(f'Произошла ошибка при создании БД {e}')

    @staticmethod
    def create_tables_company(data_connect: dict, db_name: str) -> None:
        """Создание таблицы компаний"""
        data_connect['database'] = db_name
        try:
            conn = psycopg2.connect(**data_connect)
            with conn.cursor() as cursor:
                cursor.execute("""CREATE TABLE If NOT EXISTS companies(
                               id SERIAL PRIMARY KEY,
                               employer_id VARCHAR UNIQUE,
                               name VARCHAR NOT NULL,
                               url VARCHAR);
                               """
                               )
            conn.commit()

        except psycopg2.Error as e:
            print(f"Ошибка при создании таблицы: {e}")

    @staticmethod
    def create_vacancies_table(data_connect: dict, db_name: str) -> None:
        """
        Создание таблицы вакансий выбранных компаний
        """
        data_connect['database'] = db_name
        conn = psycopg2.connect(**data_connect)
        try:
            with conn.cursor() as cursor:
                cursor.execute("""CREATE TABLE If NOT EXISTS vacancies(
                                       id SERIAL PRIMARY KEY,
                                       name VARCHAR NOT NULL,
                                       salary POSITIVE INTEGER,
                                       description TEXT,
                                       employer_id VARCHAR NOT NULL,
                                       CONSTRAINT fk_employer_id FOREIGN KEY(employer_id)
                                       REFERENCES employers(employer_id) ON DELETE CASCADE,
                                       url VARCHAR NOT NULL);
                                       """
                               )
            conn.commit()

        except psycopg2.Error as e:
            print(f"Ошибка при создании таблицы: {e}")