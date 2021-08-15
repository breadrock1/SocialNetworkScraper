from scrapers.social.facebook.FbScraper import FbScraper
from scrapers.social.linkedin.LiScraper import LiScraper
from scrapers.social.twitter.TwScraper import TwScraper
from scrapers.social.mymail.MyMailScraper import MyMailScraper
from scrapers.social.vkontakte.VkScraper import VkScraper


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
