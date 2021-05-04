from Scrapers.Social.Facebook.FbScraper import FbScraper
from Scrapers.Social.LinkedIn.LiScraper import LiScraper
from Scrapers.Social.Twitter.TwScraper import TwScraper
from Scrapers.Social.MyMail.MyMailScraper import MyMailScraper
from Scrapers.Social.Vkontakte.VkScraper import VkScraper


# TODO: Some tests for modules TwitterScraper, FacebookScraper and MyMailScraper are not available coz need API Keys
def test_social_scrapers():
    vkScraper = VkScraper()
    liScraper = LiScraper()
    fbScraper = FbScraper()
    twScraper = TwScraper()
    mmScraper = MyMailScraper()

    vkScraper.scrape(user='')
    mmScraper.scrape(email='')
    liScraper.scrape(user_id='')

    # tw_id = 'Yulia58368327'
    # twScraper.scrape(user=tw_id)

    # fb_id = 101313718664029
    # fb_token = 'EAAMTR2pPmqUBACIvzmRoZBJTbLwqlioQZBLkxU5xQHoTn3WRxhh91xE6knuZCCRWoKWMDr' \
    #            'OzebuCzSCLUuMT6S531ok54SYF8yTqecndLULRl0TlVVjdCkDOjRJKd4ibZCbZC4pI1vECV' \
    #            'di2i9Qgsh4yPI3W7gPIfomFyO3Im0cxQry9ZCsdhwQxniqFtqfAmmjNf6ZBs7NZAtFtsCZA' \
    #            'RGUPGbwXkLRVfijaVKNg69hThCwZDZD'
    # fbScraper.scrape(user=fb_id, user_access_token=fb_token)

    assert vkScraper.get_parsed_data()
    assert fbScraper.get_parsed_data() == {}
    assert twScraper.get_parsed_data() == {}
    assert mmScraper.get_parsed_data() == {}
    assert liScraper.get_parsed_data() == {}
