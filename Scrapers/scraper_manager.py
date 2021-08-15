import json

from typing import Dict

from Scrapers.Osint.DehashedScraper import DehashedScraper
from Scrapers.Osint.EmailrepScraper import EmailrepScraper
from Scrapers.Social.Facebook.FbScraper import FbScraper
from Scrapers.Social.LinkedIn.LiScraper import LiScraper
from Scrapers.Social.MyMail.MyMailScraper import MyMailScraper
from Scrapers.Social.Twitter.TwScraper import TwScraper
from Scrapers.Social.Vkontakte.VkScraper import VkScraper


class ScraperManager(object):
    def __init__(self):
        pass

    @staticmethod
    def scrapeOSINTSites(credentials: json) -> Dict:
        emailrepScraper = EmailrepScraper()
        dehashedScraper = DehashedScraper()

        email = credentials.get('OSINT').get('email')

        emailrepScraper.scrape(user_email=email)
        dehashedScraper.scrape(user_email=email)

        return {
            'Emailrep': emailrepScraper.get_parsed_data(),
            'Dehashed': dehashedScraper.get_parsed_data()
        }

    @staticmethod
    def scrapeSocialNetworks(credentials: Dict[str, Dict]) -> Dict:
        vk_scraper = VkScraper()
        li_scraper = LiScraper()
        fb_scraper = FbScraper()
        tw_scraper = TwScraper()
        mm_scraper = MyMailScraper()

        if 'Vkontakte' in credentials:
            vk_id = credentials.get('Vkontakte').get('id')
            vk_scraper.scrape(user=vk_id)

        if 'LinkedIn' in credentials:
            li_id = credentials.get('LinkedIn').get('id')
            li_scraper.scrape(user_id=li_id)

        if 'Twitter' in credentials:
            tw_id = credentials.get('Twitter').get('id')
            tw_scraper.scrape(user=tw_id)

        if 'Facebook' in credentials:
            fb_id = credentials.get('Facebook').get('id')
            fb_token = credentials.get('Facebook').get('user_access_token')

            fb_scraper.scrape(user=fb_id, user_access_token=fb_token)

        if 'MyMailRu' in credentials:
            mm_id = credentials.get('MyMailRu').get('id')
            mm_scraper.scrape(email=mm_id)

        return {
            'Vkontakte': vk_scraper.get_parsed_data(),
            'Facebook': fb_scraper.get_parsed_data(),
            'Twitter': tw_scraper.get_parsed_data(),
            'MyMail': mm_scraper.get_parsed_data(),
            'LinkedIn': li_scraper.get_parsed_data()
        }
