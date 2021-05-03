from typing import Dict
from requests import post
from logging import info
from datetime import date, datetime


class FsspScraper(object):
    def __init__(self):
        self.parsed_data = {}

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

    def scrape(self, user_id: str or int) -> None:

        info(msg='[*]\tStarting the FSSP scraping process...', level=0)

        user_data = self.__gen_fssp_data(
            method='',
            data={
            }
        )

        self.parsed_data.update({
            'user_data': user_data
        })

        info(msg='[+]\tThe FSSP scraping process has been done!', level=0)
