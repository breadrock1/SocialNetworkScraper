from scrapers.osint.dehashed_scraper import DehashedScraper
from scrapers.osint.emailrep_scraper import EmailrepScraper


def test_osint_scrapers():
    email = 'yuliya.chesnok.88@bk.ru'

    emailrepScraper = EmailrepScraper()
    dehashedScraper = DehashedScraper()

    emailrepScraper.scrape(user_email=email)
    dehashedScraper.scrape(user_email=email)

    assert emailrepScraper.get_parsed_data() == {}
    assert dehashedScraper.get_parsed_data() == {}
