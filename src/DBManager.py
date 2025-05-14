import psycopg2


# create to db
class DBManager:
    def __init__(self, host: str, database: str, user: str, password: str) -> None:
        """ Инициализация данных, подключение к БД"""
        try:
            self.connection = psycopg2.connect(host=host, database=database, user=user, password=password)
        except psycopg2.Error as e:
            print(f'Ошибка подключения к БД {e}')

    def close_conn(self) -> None:
        """Функция прекращения соединения с БД"""
        if self.connection:
            self.connection.close()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        with self.connection.cursor() as curr:
            curr.execute("""
            SELECT
            """)




    # def create_database(self):
    #     """Создание базы данных, если ее не существует"""
    #     try:
    #         conn = psycopg2.connect(
    #             host='localhost',
    #             database='coursework_5',
    #             user='postgres',
    #             password='123')
    #
    #         conn.autocommit = True
    #         cursor = conn.cursor()
    #
    #         cursor.execute




    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям. """

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""

    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""



        # with psycopg2.connect(host='localhost', database='coursework_5', user='postgres', password='123') as conn:
        #     with conn.cursor() as cur:
        #         # execute query
        #         cur.execute("INSERT INTO tut VALUES(%s, %s)", (1, 'hAPPY'))
        #         cur.execute("SELECT * FROM tut")
        #
        #         rows = cur.fetchall()
        #         for row in rows:
        #             print(row)
