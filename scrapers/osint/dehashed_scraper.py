from typing import Dict
from json import JSONDecodeError
from logging import exception, info
from requests import get, Response, RequestException

from config import DEHASHED_API_KEY


class DehashedScraper(object):
    def __init__(self):
        self.parsed_data = {}
        self.api_key = DEHASHED_API_KEY

    def __parse_response_data(self, response_data: Response) -> Dict:
        try:
            return response_data.json()
        except JSONDecodeError as e:
            print(f'Error while parsing response json data...')
            return {}

    # TODO: Need add optional to choose email or phone or ... parameter
    def __get_user_data(self, email: str) -> Dict[str, Dict or str] or None:
        try:
            response = get(
                url=f'https://api.dehashed.com/search?query=email:{email}',
                headers={
                    'Key': self.api_key,
                    'User-Agent': 'Mozilla/5.0 CvCodeApp'
                },
                verify=False,
                allow_redirects=False
            )

            return self.__parse_response_data(response_data=response)

        except RequestException or JSONDecodeError as e:
            exception(msg=f'[!]\tError while getting user information: {e.strerror}')
            return {}

    def get_parsed_data(self) -> Dict[str, Dict]:
        return self.parsed_data

    def scrape(self, user_email: str, user_phone=str or None) -> None:
        info(msg='[+]\tStarting the Dehashed scraping process...', level=0)

        self.parsed_data.update(
            self.__get_user_data(email=user_email)
        )

        # TODO: need add ability to get information by phone
        # self.parsed_data.update(
        #     self.__get_user_data(email=user_email)
        # )

        info(msg='[+]\tThe Dehashed scraping process has been done!', level=0)
