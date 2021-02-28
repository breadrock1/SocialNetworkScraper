"""
This request url help u get user access token for Vk account if dis token is need.

scope = 'photos,audio,video,docs,notes,pages,status,offers,questions,wall,' \
        'groups,email,notifications,stats,ads,offline,docs,pages,stats,notifications'

oauth = f'https://oauth.vk.com/authorize?client_id=7752097&scope={scope}&response_type=token'
"""

from typing import Dict
from requests import post
from logging import info, warning

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

    def __get_vk_data(self, method: str, data: Dict[str, str]) -> Dict[str, str or Dict]:
        response = post(
            url=f'https://api.vk.com/method/{method}',
            data=data,
            verify=False,
            allow_redirects=False
        )

        if response.status_code != OK_STATUS_CODE:
            return {}

        return response.json()

    def get_parsed_data(self) -> Dict[str, str or Dict]:
        return self.parsed_data

    def scrape(self, user: int or str) -> None:

        info(msg='[*]\tStarting the Vkontakte scraping process...', level=0)

        # first name, last name, date of birth, city
        user_info = self.__get_vk_data(
            method='users.get',
            data={
                'user_ids': user,
                'fields': 'bdate,city,country',
                'access_token': self.access_token,
                'v': self.app_version
            }
        ).get('response')[0]
        self.parsed_data.update(user_info)

        # friends
        user_friends = self.__get_vk_data(
            method='friends.get',
            data={
                'user_id': user,
                'access_token': self.access_token,
                'v': self.app_version
            }
        ).get('response').get('items')
        self.parsed_data.update({'friends': user_friends})

        # followers
        user_followers = self.__get_vk_data(
            method='users.getFollowers',
            data={
                'user_id': user,
                'access_token': self.access_token,
                'v': self.app_version
            }
        ).get('response').get('items')
        self.parsed_data.update({'followers': user_followers})

        # groups
        user_groups = self.__get_vk_data(
            method='groups.get',
            data={
                'user_id': user,
                'extended': 1,
                'filter': 'all',
                'access_token': self.access_token,
                'v': self.app_version
            }
        ).get('response').get('items')
        self.parsed_data.update({'groups': user_groups})

        # posts
        user_wall = self.__get_vk_data(
            method='wall.get',
            data={
                'owner_id': user,
                'extended': 1,
                'filter': 'all',
                'access_token': self.access_token,
                'v': self.app_version
            }
        ).get('response').get('items')
        self.parsed_data.update({'posts': []})

        for user_post in user_wall:
            post_id = user_post.get('id')

            try:
                user_post.pop('id')
                user_post.pop('attachments')
            except KeyError:
                warning(msg=f'[!]\tWarning! The post: \"{post_id}\" has no any attachments.')

            # reposts
            try:
                user_reposts = self.__get_vk_data(
                    method='wall.getReposts',
                    data={
                        'owner_id': user,
                        'post_id': post_id,
                        'access_token': self.access_token,
                        'v': self.app_version
                    }
                ).get('response').get('items')
            except AttributeError:
                warning(msg=f'[!]\tWarning! There are no any reports for post: \"{post_id}\".')
                user_reposts = []

            #  comments
            try:
                user_comments = self.__get_vk_data(
                    method='wall.getComments',
                    data={
                        'owner_id': user,
                        'post_id': post_id,
                        'extended': 1,
                        'filter': 'all',
                        'access_token': self.app_service,
                        'v': self.app_version
                    }
                ).get('response').get('items')
            except AttributeError:
                warning(msg=f'[!]\tWarning! There are no any comments for post: \"{post_id}\".')
                user_comments = []

            user_post.get('comments').update({'commenters': user_comments})
            user_post.get('reposts').update({'reporters': user_reposts})

            self.parsed_data.get('posts').append({post_id: user_post})

        info(msg='[+]\tThe Vkontakte scraping process has been done!', level=0)
