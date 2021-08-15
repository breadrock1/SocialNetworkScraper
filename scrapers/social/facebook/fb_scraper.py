from typing import Dict
from logging import exception, info
from requests import get, RequestException


class FbScraper(object):
    def __init__(self):
        self.parsed_data = {}
        self.user_access_token = None

    def __extract_data(self, data: Dict[str, Dict], key: str) -> Dict or str:
        return data.get(key) if key in data else ''

    def __checkResponseOnError(self, data: Dict) -> bool:
        return data.get("error")

    def __get_user_data(self, user_id: int or str) -> Dict[str, Dict or str] or None:
        url = f'https://graph.facebook.com/v9.0/{user_id}'
        fields = 'email,first_name,last_name,birthday,hometown,friends,groups,likes,posts'
        params = f'?fields={fields}&access_token={self.user_access_token}'

        try:
            data = get(
                url=(url + params),
                headers={
                    'Host': 'graph.facebook.com',
                    'User-Agent': 'Mozilla/5.0'
                },
                verify=False,
                allow_redirects=False
            ).json()

        except RequestException as e:
            exception(msg=f'[!]\tError while getting user page information: {e.strerror}')
            return None

        if self.__checkResponseOnError(data):
            return None

        return data

    def get_parsed_data(self) -> Dict[str, Dict]:
        return self.parsed_data

    def scrape(self, user: int, user_access_token: str) -> None:
        info(msg='[+]\tStarting the facebook scraping process...', level=0)

        self.user_access_token = user_access_token
        user_info = self.__get_user_data(user_id=user)

        if user_info is not None:

            email       = self.__extract_data(data=user_info, key='email')
            first_name  = self.__extract_data(data=user_info, key='first_name')
            last_name   = self.__extract_data(data=user_info, key='last_name')
            birthday    = self.__extract_data(data=user_info, key='birthday')
            city        = self.__extract_data(data=user_info.get('hometown'), key='name')
            friends     = self.__extract_data(data=user_info.get('friends'), key='data')
            posts       = self.__extract_data(data=user_info.get('posts'), key='data')
            likes       = self.__extract_data(data=user_info.get('likes'), key='data')

            self.parsed_data.update({
                'email'     : email,
                'first_name': first_name,
                'last_name' : last_name,
                'bday'      : birthday,
                'city'      : city,
                'friends'   : friends,
                'posts'     : posts,
                'likes'     : likes
            })

        info(msg='[+]\tThe facebook scraping process has been done!', level=0)
