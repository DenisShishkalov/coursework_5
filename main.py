import os

from src.hh_api import Vacancy

from src.criteria_create_bd_and_table import CreateDBandTables
from src.DBManager import DBManager
from src.help_func import select_employers_ids, get_full_employers_info

from dotenv import load_dotenv


load_dotenv()
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_HOST = os.getenv("DATABASE_HOST")


def main():
    """
    Функция запуска прогламмы и взаимодействия с пользователем
    """
    print(
        """Выберите 10 интересующих работодателей(компаний)"""
    )
    employers_ids = select_employers_ids()

    print("""Работодатели успешно выбраны""")
    vacancies = Vacancy()
    vacancies_list = []
    employers_with_vacancies = []

    for employer in employers_ids:
        new_vacancies = vacancies.connection(employer)
        if new_vacancies:
            vacancies_list.extend(new_vacancies)
            employers_with_vacancies.append(employer)

    if not employers_with_vacancies:
        print("Нет доступных вакансий у выбранных работодателей.")

    else:

        db_name = input("Создаем базу данных. Введите название: ")
        data_connect = {
            "host": DATABASE_HOST,
            "database": "coursework_5",
            "user": DATABASE_USER,
            "port": "5432",
            "password": DATABASE_PASSWORD,
        }

        CreateDBandTables.create_database(data_connect, db_name)

        print("Создаем указанные таблицы")
        CreateDBandTables.create_tables_employers(data_connect, db_name)
        CreateDBandTables.create_vacancies_table(data_connect, db_name)

        print("Заполняем таблицу необходимыми данными...")
        full_employers_info = get_full_employers_info(employers_ids)
        CreateDBandTables.insert_data_employers(data_connect, db_name, full_employers_info)
        print(vacancies_list)
        CreateDBandTables.insert_data_vacancies(data_connect, db_name, vacancies_list)

        db_option = DBManager(DATABASE_HOST, db_name, DATABASE_USER, DATABASE_PASSWORD)

        while True:
            print(
                """
            1. Показать компании и количество вакансий
            2. Показать все вакансии
            3. Показать среднюю зарплату
            4. Показать вакансии с зарплатой выше средней
            5. Показать вакансии по ключевому слову"""
            )

            choice = input("Выберите опцию (или введите 'отмена' для выхода): ")

            if choice == "отмена":
                break

            elif choice == "1":
                company_ = db_option.get_companies_and_vacancies_count()
                for x in company_:
                    print(f"""Company - {x[0]}: {x[1]} vacancies""")

            elif choice == "2":
                all_vacancies = db_option.get_all_vacancies()
                for i in all_vacancies:
                    print(
                        f"""Vacancy: {i[0]}
                            Salary: {i[2]}
                            Company: {i[1]}
                            URL: {i[3]}"""
                    )

            elif choice == "3":
                avg_salary = db_option.get_avg_salary()
                for i in avg_salary:
                    print(f"""Средняя сумма заработной платы по вакансии: {i[0]}""")

            elif choice == "4":
                high_salary = db_option.get_vacancies_with_higher_salary()
                for i in high_salary:
                    print(
                        f"""Vacancy: {i[1]}
                            id: {i[0]}
                            description: {i[2]}
                            salary from {i[3]}
                            published at {i[4]}
                            url: {i[6]}"""
                    )

            elif choice == "5":
                search = input("Введите ключевое слово для поиска по вакансиям: ")
                content = db_option.get_vacancies_with_search(search)
                for i in content:
                    print(
                        f"""Vacancy: {i[1]}
                            id: {i[0]}
                            description: {i[2]}
                            salary from {i[3]}
                            published at {i[4]}
                            url: {i[6]}"""
                    )

            else:
                print("Некорректный ввод. Пожалуйста, попробуйте снова.")

        db_option.close_conn()


if __name__ == "__main__":
    main()
