import json

from typing import Dict

from scrapers.osint.dehashed_scraper import DehashedScraper
from scrapers.osint.emailrep_scraper import EmailrepScraper
from scrapers.social.facebook.fb_scraper import FbScraper
from scrapers.social.linkedin.li_scraper import LiScraper
from scrapers.social.mymail.my_mail_scraper import MyMailScraper
from scrapers.social.twitter.tw_scraper import TwScraper
from scrapers.social.vkontakte.vk_scraper import VkScraper


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

        if 'vkontakte' in credentials:
            vk_id = credentials.get('vkontakte').get('id')
            vk_scraper.scrape(user=vk_id)

        if 'linkedin' in credentials:
            li_id = credentials.get('linkedin').get('id')
            li_scraper.scrape(user_id=li_id)

        if 'twitter' in credentials:
            tw_id = credentials.get('twitter').get('id')
            tw_scraper.scrape(user=tw_id)

        if 'facebook' in credentials:
            fb_id = credentials.get('facebook').get('id')
            fb_token = credentials.get('facebook').get('user_access_token')

            fb_scraper.scrape(user=fb_id, user_access_token=fb_token)

        if 'MyMailRu' in credentials:
            mm_id = credentials.get('MyMailRu').get('id')
            mm_scraper.scrape(email=mm_id)

        return {
            'vkontakte': vk_scraper.get_parsed_data(),
            'facebook': fb_scraper.get_parsed_data(),
            'twitter': tw_scraper.get_parsed_data(),
            'mymail': mm_scraper.get_parsed_data(),
            'linkedin': li_scraper.get_parsed_data()
        }
