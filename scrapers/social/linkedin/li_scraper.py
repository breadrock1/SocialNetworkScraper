from typing import Dict
from linkedin_api import Linkedin
from logging import info, exception

from config import (
    LI_USERNAME,
    LI_PASSWORD
)


class LiScraper(object):
    def __init__(self):
        self.api = None

        self.app_user = LI_USERNAME
        self.app_passwd = LI_PASSWORD

        self.parsed_data = {}

    def __init_api(self) -> Linkedin or None:
        try:
            api = Linkedin(self.app_user, self.app_passwd)
        except Exception as e:
            exception(msg=f'[-]\tFailed to initialize linkedin api: {e}')
            return None

        return api

    def __extract_data(self, data: Dict[str, Dict], key: str) -> Dict or str:
        return data.get(key) if key in data else ''

    def get_parsed_data(self) -> Dict[str, str or Dict]:
        return self.parsed_data

    def scrape(self, user_id: str or int) -> None:
        info(msg='[*]\tStarting the linkedin scraping process...', level=0)

        self.api = self.__init_api()

        if self.api is not None:

            user_info = self.api.get_profile(user_id)
            contact_info = self.api.get_profile_contact_info(user_id)

            profile_id = self.__extract_data(data=user_info, key='profile_id')
            first_name = self.__extract_data(data=user_info, key='firstName')
            last_name = self.__extract_data(data=user_info, key='lastName')
            city = self.__extract_data(data=user_info, key='geoLocationName')
            birthdate = self.__extract_data(data=contact_info, key='birthdate')
            email = self.__extract_data(data=contact_info, key='email_address')

            self.parsed_data.update({
                'id'            : profile_id,
                'email'         : email,
                'first_name'    : first_name,
                'last_name'     : last_name,
                'bday'          : birthdate,
                'city'          : city
            })

        info(msg='[+]\tThe linkedin scraping process has been done!', level=0)
