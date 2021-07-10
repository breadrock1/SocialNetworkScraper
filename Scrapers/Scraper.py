from typing import Dict


class Scraper(object):
    def __init__(self):
        self.parsed_data = {}

    def get_parsed_data(self) -> Dict[str, str or Dict]:
        return self.parsed_data

    def scrape(self, user: int or str) -> None:
        return
