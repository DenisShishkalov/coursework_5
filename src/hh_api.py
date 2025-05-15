import requests


class HeadHunterAPI:
    """Kласс, предполагающий получение вакансий с сайта hh.ru, наследуемый от класса WorkAPI."""

    def __init__(self, base_url="https://api.hh.ru/") -> None:
        self.__base_url = base_url

    @property
    def base_url(self):
        return self.__base_url


class Employer(HeadHunterAPI):

    def employer_search(self, search: str) -> list:
        """Метод получения работодателей по переданному слову"""
        response = requests.get(f"{self.base_url}employers?text={search}&page=0&per_page=100")
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print("Ошибка при отправке запроса")
            return []

    def employer_id(self, search: str) -> list[dict]:
        """Метод получения id работодателя"""
        employers = self.employer_search(search)

        ids = []
        for employer in employers:
            data_ = {employer["id"]: employer["name"]}
            ids.append(data_)
        if ids:
            return ids
        else:
            print("Айди не найдены")

    def info_employer(self, employer_id: int):
        """ Метод получения информации о работодателе"""
        response = requests.get(f"{self.base_url}employers/{employer_id}")
        if response.status_code == 200:
            return response.json()
        else:
            print("Ошибка при получении информации о работодателе")
            return None


class Vacancy(HeadHunterAPI):
    """
    Класс для работы с API HeadHunter.
    """

    def connection(self, employer_id: int) -> None | list:
        """
        Метод, который подключается к апи hh.ru и получает вакансии по айди работодателя в формате json словарей
        """
        url = f"{self.base_url}vacancies?employer_id={employer_id}"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()["items"]

        else:
            print(f"Запрос не был успешным. Возможная причина: {response.reason}")
            return []
