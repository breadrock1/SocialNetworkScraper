from typing import Dict
from logging import exception, info
from requests import get, RequestException

from config import DEHASHED_API_KEY


class DehashedScraper(object):
    def __init__(self):
        self.parsed_data = {}
        self.api_key = DEHASHED_API_KEY

    # TODO: Need add optional to choose email or phone or ... parameter
    def __get_user_data(self, email: str) -> Dict[str, Dict or str] or None:
        keys = f'query=email:{email}'
        url = f'https://api.dehashed.com/search?{keys}'

        try:
            data = get(
                url=url,
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

    def scrape(self, user_email: str, user_phone=str or None) -> None:

        info(msg='[+]\tStarting the Dehashed scraping process...', level=0)

        user_phone_data = self.__get_user_data(email=user_email) \
            if user_phone else {}

        user_email_data = self.__get_user_data(email=user_email) \
            if user_email else {}

        self.parsed_data.update({
            user_phone_data,
            user_email_data
        })

        info(msg='[+]\tThe Dehashed scraping process has been done!', level=0)
