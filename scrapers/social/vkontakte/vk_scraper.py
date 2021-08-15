from typing import Dict
from logging import info, warning
from requests import post, RequestException

from config import (
    VK_APP_VERSION,
    VK_APP_SERVICE_KEY,
    VK_APP_ACCESS_TOKEN
)

OK_STATUS_CODE = 200


class VkScraper(object):
    def __init__(self):
        self.app_version = VK_APP_VERSION
        self.app_service = VK_APP_SERVICE_KEY
        self.access_token = VK_APP_ACCESS_TOKEN

        self.parsed_data = {}

    def __extract_data(self, data: Dict[str, str or Dict], key: str) -> Dict:
        try:
            return data.get(key)
        except AttributeError as e:
            print(f'Error! There is no key {key}: {e}')
            return {}

    def __get_vk_data(self, method: str, data: Dict[str, str or Dict]) -> Dict[str, str or Dict] or None:
        try:
            response = post(
                url=f'https://api.vk.com/method/{method}',
                data=data,
                verify=False,
                allow_redirects=False
            )
        except RequestException as e:
            warning(msg=f'[!]\tFailed to send request: {e.strerror}')
            return None

        try:
            return response.json().get('response')
        except KeyError as e:
            warning(msg=f'[!]\tFailed to send request: {e}')
            return {}

    def get_parsed_data(self) -> Dict[str, str or Dict]:
        return self.parsed_data

    def scrape(self, user: int or str) -> None:
        info(msg='[*]\tStarting the vkontakte scraping process...', level=0)

        # first name, last name, date of birth, city
        vk_data = self.__get_vk_data(
            method='users.get',
            data={
                'user_ids'      : user,
                'fields'        : 'bdate,city,country',
                'access_token'  : self.access_token,
                'v'             : self.app_version
            }
        )
        user_info = vk_data[0] if vk_data else {}

        first_name = self.__extract_data(data=user_info, key='first_name')
        last_name = self.__extract_data(data=user_info, key='last_name')
        birthdate = self.__extract_data(data=user_info, key='bdate')
        hometown = self.__extract_data(data=user_info.get('city'), key='title')

        # friends
        vk_data = self.__get_vk_data(
            method='friends.get',
            data={
                'user_id'       : user,
                'access_token'  : self.access_token,
                'v'             : self.app_version
            }
        )
        user_friends = [] if vk_data is None else self.__extract_data(data=vk_data, key='items')

        # followers
        vk_data = self.__get_vk_data(
            method='users.getFollowers',
            data={
                'user_id'       : user,
                'access_token'  : self.access_token,
                'v'             : self.app_version
            }
        )
        user_followers = [] if vk_data is None else self.__extract_data(data=vk_data, key='items')

        # groups
        vk_data = self.__get_vk_data(
            method='groups.get',
            data={
                'user_id'       : user,
                'extended'      : 1,
                'filter'        : 'all',
                'access_token'  : self.access_token,
                'v'             : self.app_version
            }
        )
        user_groups = [] if vk_data is None else self.__extract_data(data=vk_data, key='items')

        # posts
        vk_data = self.__get_vk_data(
            method='wall.get',
            data={
                'owner_id'      : user,
                'extended'      : 1,
                'filter'        : 'all',
                'access_token'  : self.access_token,
                'v'             : self.app_version
            }
        )
        user_wall = [] if vk_data is None else self.__extract_data(data=vk_data, key='items')

        user_post: Dict
        for user_post in user_wall:
            post_id = user_post.get('id')

            # reposts
            vk_data = self.__get_vk_data(
                method='wall.getReposts',
                data={
                    'owner_id'      : user,
                    'post_id'       : post_id,
                    'access_token'  : self.access_token,
                    'v'             : self.app_version
                }
            )
            user_reposts = [] if vk_data is None else self.__extract_data(data=vk_data, key='items')

            #  comments
            vk_data = self.__get_vk_data(
                method='wall.getComments',
                data={
                    'owner_id'      : user,
                    'post_id'       : post_id,
                    'extended'      : 1,
                    'filter'        : 'all',
                    'access_token'  : self.app_service,
                    'v'             : self.app_version
                }
            )
            user_comments = [] if vk_data is None else self.__extract_data(data=vk_data, key='items')

            user_post.get('reposts').update({'reporters': user_reposts})
            user_post.get('comments').update({'commenters': user_comments})

        self.parsed_data.update({
            'first_name': first_name,
            'last_name' : last_name,
            'birthday'  : birthdate,
            'city'      : hometown,
            'friends'   : user_friends,
            'followers' : user_followers,
            'groups'    : user_groups,
            'posts'     : user_wall
        })

        info(msg='[+]\tThe vkontakte scraping process has been done!', level=0)
