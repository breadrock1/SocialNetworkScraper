from re import search
from typing import Dict
from hashlib import md5
from json import JSONDecodeError
from logging import exception, info
from requests import get, post, RequestException

from config import (
    MM_APP_ID,
    MM_USERNAME,
    MM_PASSWORD,
    MM_APP_SECRET_KEY,
    MM_APP_PRIVATE_KEY
)


class MyMailScraper(object):
    def __init__(self):
        self.app_id = MM_APP_ID
        self.username = MM_USERNAME
        self.password = MM_PASSWORD
        self.app_secret_key = MM_APP_SECRET_KEY
        self.app_private_key = MM_APP_PRIVATE_KEY

        self.uid = None
        self.session_key = None

        self.parsed_data = {}

    def __get_user_id(self, email: str) -> int or None:
        try:
            user = search(r"^.+?(?=@)", email).group()
            domain = search(r"@[a-zA-Z]*", email).group()[1:]
        except AttributeError as e:
            print(f'Failed to parse email address: {e}')
            return None

        url = f'http://appsmail.ru/platform/{domain}/{user}/'

        try:
            response = get(
                url=url,
                verify=False,
                allow_redirects=False
            )
            user_id = response.json().get('uid')
        except RequestException or JSONDecodeError as e:
            exception(msg=f'[-]\tFailed to get user uid: {e.msg}')
            return None

        return user_id

    def __gen_sig_key(self, data: Dict[str, str]) -> str:
        sort = dict(sorted(data.items()))
        params = ''.join(
            [(k + '=' + v) for k, v in sort.items()]
        )
        params = self.uid + params + self.app_private_key

        return md5(params.encode('utf-8')).hexdigest()

    def __gen_session_key(self, data: Dict[str, str or int]) -> Dict[str, str]:
        response = post(
            url='https://appsmail.ru/oauth/token',
            headers={
                'Host'          : 'appsmail.ru',
                'Content-Type'  : 'application/x-www-form-urlencoded'
            },
            data=data,
            verify=False,
            allow_redirects=False
        )

        if response.status_code != 200:
            return {}

        return response.json()

    def __get_data(self, data: Dict[str, str or int]) -> Dict[str, str]:
        response = post(
            url='http://www.appsmail.ru/platform/api/',
            data=data,
            verify=False,
            allow_redirects=False
        )

        if response.status_code != 200:
            return {}

        return response.json()

    def get_parsed_data(self) -> Dict[str, str or Dict]:
        return self.parsed_data

    def scrape(self, email: str) -> None:
        self.uid = self.__get_user_id(email=email)

        if self.uid is None:
            return

        self.session_key = self.__gen_session_key(
            data={
                'client_id'     : self.app_id,
                'client_secret' : self.app_private_key,
                'username'      : self.username,
                'password'      : self.password,
                'grant_type'    : 'password',
                'scope'         : 'widget'
            }
        )

        # first and last name, bdate, city, email ...
        method = 'users.getInfo'
        user_info = self.__get_data(
            data={
                'method'        : method,
                'app_id'        : self.app_id,
                'session_key'   : self.session_key,
                'uids'          : self.uid,
                'sig'           : self.__gen_sig_key(
                    data={
                        'method': method,
                        'app_id': str(self.app_id),
                        'uids'  : self.uid
                    }
                )
            }
        )
        self.parsed_data.update(user_info)

        # friends -> list ids
        method = 'friends.get'
        friends = self.__get_data(
            data={
                'method'    : method,
                'app_id'    : self.app_id,
                'ext'       : 0,
                'sig'       : self.__gen_sig_key(
                    data={
                        'method': method,
                        'app_id': str(self.app_id),
                        'uids'  : self.uid
                    }
                )
            }
        )
        self.parsed_data.update(friends)

        # streams
        method = 'stream.get'
        streams = self.__get_data(
            data={
                'method'        : method,
                'app_id'        : self.app_id,
                'session_key'   : self.session_key,
                'limit'         : 100,
                'sig'           : self.__gen_sig_key(
                    data={
                        'method': method,
                        'app_id': str(self.app_id)
                    }
                )
            }
        )
        self.parsed_data.update(streams)

        info(msg='[+] The scraping MyMailRu has been done!', level=0)
