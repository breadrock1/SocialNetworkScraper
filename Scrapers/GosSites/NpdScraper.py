from typing import Dict
from requests import post
from logging import info
from datetime import date, datetime


class NpdScraper(object):
    def __init__(self):
        self.parsed_data = {}

    def __get_current_date(self) -> str:
        now = datetime.now()
        return date(now.year, now.month, now.day).isoformat()

    def __gen_npd_data(self, data: Dict[str, str or int]) -> Dict[str, str]:
        response = post(
            url='https://statusnpd.nalog.ru:443/api/v1/tracker/taxpayer_status',
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

        info(msg='[*]\tStarting the NPD scraping process...', level=0)

        user_data = self.__gen_npd_data(
            data={
                'inn': user_id,
                'requestDate"': self.__get_current_date()
            }
        )

        self.parsed_data.update({
            'user_data': user_data
        })

        info(msg='[+]\tThe NPD scraping process has been done!', level=0)
