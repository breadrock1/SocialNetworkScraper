from Scrapers.Social.Facebook.FbScraper import FbScraper
from Scrapers.Social.LinkedIn.LiScraper import LiScraper
from Scrapers.Social.Twitter.TwScraper import TwScraper
from Scrapers.Social.MyMail.MyMailScraper import MyMailScraper
from Scrapers.Social.Vkontakte.VkScraper import VkScraper

if __name__ == '__main__':
    vkScraper = VkScraper()
    liScraper = LiScraper()
    fbScraper = FbScraper()
    twScraper = TwScraper()
    mmScraper = MyMailScraper()

    vk_id = '633470190'
    vkScraper.scrape(user=vk_id)

    li_id = 'yulia-chesnokova-590525207'
    liScraper.scrape(user_id=li_id)

    tw_id = 'navalny'
    twScraper.scrape(user=tw_id)

    fb_id = 101313718664029
    fb_token = 'EAAMTR2pPmqUBACIvzmRoZBJTbLwqlioQZBLkxU5xQHoTn3WRxhh91xE6knuZCCRWoKWMDr' \
               'OzebuCzSCLUuMT6S531ok54SYF8yTqecndLULRl0TlVVjdCkDOjRJKd4ibZCbZC4pI1vECV' \
               'di2i9Qgsh4yPI3W7gPIfomFyO3Im0cxQry9ZCsdhwQxniqFtqfAmmjNf6ZBs7NZAtFtsCZA' \
               'RGUPGbwXkLRVfijaVKNg69hThCwZDZD'
    fbScraper.scrape(user=fb_id, user_access_token=fb_token)

    mm_id = 'yuliya.chesnok.88@bk.ru'
    mm_token = 'be6ef89965d58e56dec21acb9b62bdaa'
    mmScraper.scrape(email='yuliya.chesnok.88@bk.ru')

    assert vkScraper.get_parsed_data()
    assert fbScraper.get_parsed_data()
    assert twScraper.get_parsed_data()
    assert mmScraper.get_parsed_data()
    assert liScraper.get_parsed_data()
