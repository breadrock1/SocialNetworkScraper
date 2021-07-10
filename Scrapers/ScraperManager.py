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
        fbScraper = None
        vkScraper = VkScraper()
        liScraper = LiScraper()
        twScraper = TwScraper()
        mmScraper = MyMailScraper()

        if 'Vkontakte' in credentials:
            vk_id = credentials.get('Vkontakte').get('id')
            vkScraper.scrape(user=vk_id)

        if 'LinkedIn' in credentials:
            li_id = credentials.get('LinkedIn').get('id')
            liScraper.scrape(user_id=li_id)

        if 'Twitter' in credentials:
            tw_id = credentials.get('Twitter').get('id')
            twScraper.scrape(user=tw_id)

        if 'Facebook' in credentials:
            fb_id = credentials.get('Facebook').get('id')
            fb_token = credentials.get('Facebook').get('user_access_token')

            fbScraper = FbScraper(user_access_token=fb_token)
            fbScraper.scrape(user=fb_id)

        if 'MyMailRu' in credentials:
            mm_id = credentials.get('MyMailRu').get('id')
            mmScraper.scrape(email=mm_id)

        return {
            'Vkontakte': vkScraper.get_parsed_data(),
            'Facebook': fbScraper.get_parsed_data(),
            'Twitter': twScraper.get_parsed_data(),
            'MyMail': mmScraper.get_parsed_data(),
            'LinkedIn': liScraper.get_parsed_data()
        }
