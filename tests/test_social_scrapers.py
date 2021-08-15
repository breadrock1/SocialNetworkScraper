from scrapers.social.facebook.fb_scraper import FbScraper
from scrapers.social.linkedin.li_scraper import LiScraper
from scrapers.social.twitter.tw_scraper import TwScraper
from scrapers.social.mymail.my_mail_scraper import MyMailScraper
from scrapers.social.vkontakte.vk_scraper import VkScraper


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
    twScraper.scrape(user='')
    fbScraper.scrape(user=0, user_access_token='')

    assert vkScraper.get_parsed_data()
    assert fbScraper.get_parsed_data() == {}
    assert twScraper.get_parsed_data() == {}
    assert mmScraper.get_parsed_data() == {}
    assert liScraper.get_parsed_data() == {}
