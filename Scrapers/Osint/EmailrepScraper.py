from typing import Dict
from logging import exception, info
from requests import get, RequestException

from config import EMAILREP_API_KEY


class EmailrepScraper(object):
    def __init__(self):
        self.parsed_data = {}
        self.api_key = EMAILREP_API_KEY

    def __get_user_data(self, email: str) -> Dict[str, Dict or str] or None:
        try:
            data = get(
                url= f'https://emailrep.io/{email}',
                headers={
                    'Key': self.api_key,
                    'User-Agent': 'Mozilla/5.0 CvCodeApp'
                },
                verify=False,
                allow_redirects=False
            )
        except RequestException as e:
            exception(msg=f'[!]\tError while getting user information: {e.strerror}')
            return None

        return data.json()

    def get_parsed_data(self) -> Dict[str, Dict]:
        return self.parsed_data

    def scrape(self, user_email: str) -> None:

        info(msg='[+]\tStarting the Emailrep scraping process...', level=0)

        self.parsed_data.update(
            self.__get_user_data(email=user_email)
        )

        info(msg='[+]\tThe Emailrep scraping process has been done!', level=0)
