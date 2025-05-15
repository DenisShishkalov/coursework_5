from typing import List
import psycopg2


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

    def get_companies_and_vacancies_count(self) -> None | List:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        try:
            with self.connection.cursor() as curr:
                curr.execute(
                    """SELECT e.name, COUNT(v.id) AS vacancy_count 
                    FROM employers e
                    LEFT JOIN vacancies v USING(employer_id)
                    GROUP BY e.name;
                    """
                )
                data_ = curr.fetchall()
                if data_:
                    return data_
        except psycopg2.Error as e:
            print(f'Произошла ошибка: {e}, при получении данных')
            return []

    def get_all_vacancies(self) -> None | List:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        try:
            with self.connection.cursor() as curr:
                curr.execute(
                    """SELECT v.name AS vacancy_name, e.name AS company_name, v.salary, v.url 
                    FROM vacancies v
                    LEFT JOIN employers e USING(employer_id);
                    """
                )
                data_ = curr.fetchall()
                if data_:
                    return data_

        except psycopg2.Error as e:
            print(f'Произошла ошибка: {e}, при получении данных')
            return []

    def get_avg_salary(self) -> None | List:
        """Получает среднюю зарплату по вакансиям. """
        try:
            with self.connection.cursor() as curr:
                curr.execute(
                    """
                    SELECT ROUND(AVG(salary)) FROM vacancies;
                    """
                )
                data_ = curr.fetchall()
                if data_:
                    return data_

        except psycopg2.Error as e:
            print(f'Произошла ошибка: {e}, при получении данных')
            return []

    def get_vacancies_with_higher_salary(self) -> None | List:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        try:
            with self.connection.cursor() as curr:
                curr.execute(
                    """
                    SELECT * FROM vacancies
                    WHERE salary > (SELECT AVG(salary) FROM vacancies);
                    """
                )
                data_ = curr.fetchall()
                if data_:
                    return data_

        except psycopg2.Error as e:
            print(f'Произошла ошибка: {e}, при получении данных')
            return []

    def get_vacancies_with_search(self, search: str) -> None | List:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        try:
            with self.connection.cursor() as curr:
                curr.execute(
                    """SELECT * FROM vacancies
                    WHERE name LIKE %s;
                    """,
                        (f"%{search}%",),
                    )

                data_ = curr.fetchall()
                if data_:
                    return data_

        except psycopg2.Error as e:
            print(f'Произошла ошибка: {e}, при получении данных')
            return []
