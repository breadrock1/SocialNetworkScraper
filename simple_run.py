from sys import argv
from typing import Dict
from time import time_ns
from logging import info
from json import dump, load

from config import RESULTS_DIR
from Scrapers.Twitter.TwScraper import TwScraper
from Scrapers.Facebook.FbScraper import FbScraper
from Scrapers.LinkedIn.LiScraper import LiScraper
from Scrapers.Vkontakte.VkScraper import VkScraper
from Scrapers.MyMail.MyMailScraper import MyMailScraper


def writeOutResults(data: Dict) -> None:

    def generate_filename() -> str:
        return f'{RESULTS_DIR}/{str(time_ns())}.json'

    with open(generate_filename(), 'w+') as file:
        dump(
            data,
            file,
            indent=4,
            sort_keys=False
        )
        file.close()


def readInputData(path: str) -> Dict[str, Dict]:
    with open(path, 'r') as file:
        data = load(
            file
        )
        file.close()

    return data


if __name__ == '__main__':

    if len(argv) < 2:
        raise ValueError(
            '[-]\tError! Missing path to file argument. You need specify path to file with user credentials'
            f'\nUsage: {argv[0]} "path to file"'
        )

    user_creds = readInputData(path=argv[1])

    vkScraper = VkScraper()
    liScraper = LiScraper()
    fbScraper = FbScraper()
    twScraper = TwScraper()
    mmScraper = MyMailScraper()

    if 'Vkontakte' in user_creds:
        vk_id = user_creds.get('Vkontakte').get('id')
        vkScraper.scrape(user=vk_id)

    if 'LinkedIn' in user_creds:
        li_id = user_creds.get('LinkedIn').get('id')
        liScraper.scrape(user_id=li_id)

    if 'Twitter' in user_creds:
        tw_id = user_creds.get('Twitter').get('id')
        # twScraper.scrape(user=tw_id)

    if 'Facebook' in user_creds:
        fb_id = user_creds.get('Facebook').get('id')
        fb_token = user_creds.get('Facebook').get('user_access_token')

        fbScraper.scrape(user=fb_id, user_access_token=fb_token)

    if 'MyMailRu' in user_creds:
        mm_id = user_creds.get('MyMailRu').get('id')
        mm_token = user_creds.get('MyMailRu').get('session_key')

        # mmScraper.scrape(email='')

    writeOutResults({
        'Vkontakte' : vkScraper.get_parsed_data(),
        'Facebook'  : fbScraper.get_parsed_data(),
        'Twitter'   : twScraper.get_parsed_data(),
        'MyMail'    : mmScraper.get_parsed_data(),
        'LinkedIn'  : liScraper.get_parsed_data()
    })

    info(msg='[+]\tThe scraping process has been done!')
