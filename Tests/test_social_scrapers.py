from Scrapers.Social.Facebook.FbScraper import FbScraper
from Scrapers.Social.LinkedIn.LiScraper import LiScraper
from Scrapers.Social.Twitter.TwScraper import TwScraper
from Scrapers.Social.MyMail.MyMailScraper import MyMailScraper
from Scrapers.Social.Vkontakte.VkScraper import VkScraper


# TODO: Some tests for modules TwitterScraper, FacebookScraper and MyMailScraper are not available coz need API Keys
def test_social_scrapers():
    vkScraper = VkScraper()
    liScraper = LiScraper()
    twScraper = TwScraper()
    mmScraper = MyMailScraper()
    fbScraper = FbScraper(user_access_token='')

    vkScraper.scrape(user='')
    mmScraper.scrape(email='')
    liScraper.scrape(user_id='')
    twScraper.scrape(user='')
    fbScraper.scrape(user=0)

    assert vkScraper.get_parsed_data()
    assert fbScraper.get_parsed_data() == {}
    assert twScraper.get_parsed_data() == {}
    assert mmScraper.get_parsed_data() == {}
    assert liScraper.get_parsed_data() == {}
