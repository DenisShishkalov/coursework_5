import psycopg2


class CreateDBandTables:
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
    def create_tables_employers(data_connect: dict, db_name: str) -> None:
        """Создание таблицы работодателей"""
        data_connect['database'] = db_name
        try:
            conn = psycopg2.connect(**data_connect)
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS employers (
                        id SERIAL PRIMARY KEY,
                        employer_id VARCHAR UNIQUE,
                        name VARCHAR NOT NULL,
                        url VARCHAR,
                        open_vacancies INTEGER
                        );
                        """)
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
                cursor.execute("""
                                    CREATE TABLE IF NOT EXISTS vacancies (
                                    id SERIAL PRIMARY KEY,
                                    name VARCHAR NOT NULL,
                                    description TEXT,
                                    salary INTEGER,
                                    published_at DATE,
                                    employer_id VARCHAR NOT NULL,
                                    CONSTRAINT fk_employer_id FOREIGN KEY(employer_id) 
                                    REFERENCES employers(employer_id) ON DELETE CASCADE,
                                    url VARCHAR NOT NULL
                    );
                """)

            conn.commit()

        except psycopg2.Error as e:
            print(f"Ошибка при создании таблицы: {e}")

    @staticmethod
    def insert_data_vacancies(data_connect: dict, db_name: str, data_: list) -> None:
        """
        Метод заполнения таблицы вакансий
        """
        data_connect['database'] = db_name
        try:
            with psycopg2.connect(**data_connect) as conn:
                with conn.cursor() as curr:
                    for v in data_:
                        salary = None
                        if v.get("salary") is not None:
                            salary = v["salary"].get("from", None)
                        curr.execute(
                            """
                            INSERT INTO vacancies (name, salary, employer_id, url) 
                            VALUES(%s, %s, %s, %s)""",
                            (
                                v["name"],
                                salary,
                                v["employer"]["id"],
                                v["alternate_url"],
                            ),
                        )

                    conn.commit()
        except psycopg2.Error as e:
            print(f"Ошибка при заполнении таблицы: {e}")

    @staticmethod
    def insert_data_employers(data_connect: dict, db_name: str, data_: dict) -> None:
        """Метод добавления информации работодателей"""
        data_connect["database"] = db_name
        try:
            with psycopg2.connect(**data_connect) as conn:
                with conn.cursor() as curr:
                    for employer_id, employer_info in data_.items():
                        if isinstance(employer_info, dict) and employer_info:
                            open_vacancies = employer_info.get("open_vacancies", 0)
                            name = employer_info.get("name", "Неизвестно")
                            url = employer_info.get("url", "")

                            curr.execute(
                                """INSERT INTO employers (employer_id, name, url, open_vacancies)
                                           VALUES (%s, %s, %s, %s)
                                           """,
                                (employer_id, name, url, open_vacancies),
                            )
                        else:
                            print(
                                f"Неверный формат данных для работодателя {employer_id}: {employer_info}"
                            )

                    conn.commit()

        except psycopg2.Error as e:
            print(f"Ошибка при заполнении таблицы: {e}")
