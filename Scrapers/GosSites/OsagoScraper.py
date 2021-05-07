from typing import Dict
from requests import post
from logging import info


class OsagoScraper(object):
    def __init__(self):
        self.parsed_data = {}

    def __gen_osago_data(self, data: Dict[str, str or int]) -> Dict:
        response = post(
            url='https://elpas.ru/api.php',
            data=data,
            headers={
                'Content-Type': 'application/json'
            },
            verify=False,
            allow_redirects=False
        )

        if response.status_code != 200:
            return {}

        return response.json()

    def get_parsed_data(self) -> Dict[str, str or Dict]:
        return self.parsed_data

    def scrape(self, user_data: Dict[str, str]) -> None:
        info(msg='[*]\tStarting the OSAGO scraping process...', level=0)

        user_data = self.__gen_osago_data(
            data={
                # id операции (API_GET_DATA)
                "top": "25",
                # id2 операции
                "subtop": "1",
                # тип операции (_ZKZ_INS)
                "type": "34",
                # id Партнера
                "id": "1256987",
                # подпись запроса
                "hash": "b9c4302230696ff1436h554122b071",
                # гос.номер ТС
                "licenseplate": "А000АА00"
            }
        )

        self.parsed_data.update({
            'user_data': user_data
        })

        info(msg='[+]\tThe OSAGO scraping process has been done!', level=0)
