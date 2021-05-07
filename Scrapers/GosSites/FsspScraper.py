from typing import Dict
from requests import post
from logging import info
from datetime import date, datetime

from config import FSSPRUS_API_KEY


class FsspScraper(object):
    def __init__(self):
        self.parsed_data = {}
        self.api_key = FSSPRUS_API_KEY

    def __get_current_date(self) -> str:
        now = datetime.now()
        return date(now.year, now.month, now.day).isoformat()

    def __gen_fssp_data(self, method: str, data: Dict[str, str or int]) -> Dict[str, str]:
        response = post(
            url=f'https://api-ip.fssprus.ru/api/v1.0/{method}',
            data=data,
            verify=False,
            allow_redirects=False
        )

        if response.status_code != 200:
            return {}

        return response.json()

    def get_parsed_data(self) -> Dict[str, str or Dict]:
        return self.parsed_data

    def scrape(self, user_data: Dict[str: str or int]) -> None:

        info(msg='[*]\tStarting the FSSP scraping process...', level=0)

        # number
        region = user_data.get('region')
        address = user_data.get('address')
        # dd.mm.yyyy
        birthday = user_data.get('birthday')
        last_name = user_data.get('last_name')
        first_name = user_data.get('first_name')
        second_name = user_data.get('second_name')

        # Request to search for information about an individual
        user_data = self.__gen_fssp_data(
            method='/search/physical',
            data={
                'token'     : self.api_key,
                'region'    : region,
                'firstname' : first_name,
                'secondname': second_name,
                'lastname'  : last_name,
                'birthday'  : birthday
            }
        )
        self.parsed_data.update(user_data)

        # Request to search for information about a legal entity
        user_legal = self.__gen_fssp_data(
            method='/search/ip',
            data={
                'token'     : self.api_key,
                'region'    : region,
                'address'   : address,
                'name'      : f'{second_name} {first_name} {last_name}'
            }
        )
        self.parsed_data.update(user_legal)

        # Request to search for information on enforcement proceedings
        user_ip = self.__gen_fssp_data(
            method='/search/legal',
            data={
                'token' : self.api_key,
                # Enforcement proceedings number in the format "n ... n/yy/dd/rr" or "n ... n/yy/ddddd-IP"
                'number': ''
            }
        )
        self.parsed_data.update(user_ip)

        info(msg='[+]\tThe FSSP scraping process has been done!', level=0)
