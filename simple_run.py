from typing import Dict
from pathlib import Path
from logging import info
from json import dump, load
from argparse import ArgumentParser, Namespace

from Scrapers.Social.Twitter.TwScraper import TwScraper
from Scrapers.Social.Facebook.FbScraper import FbScraper
from Scrapers.Social.LinkedIn.LiScraper import LiScraper
from Scrapers.Social.Vkontakte.VkScraper import VkScraper
from Scrapers.Social.MyMail.MyMailScraper import MyMailScraper

from Scrapers.Osint.EmailrepScraper import EmailrepScraper
from Scrapers.Osint.DehashedScraper import DehashedScraper


def _writeOutResults(results: str, data: Dict) -> None:
    def generate_filename() -> str:
        return f'{results}/users.json'

    with open(generate_filename(), 'w+') as file:
        dump(
            data,
            file,
            indent=4,
            sort_keys=False
        )
        file.close()


def _readInputData(path: str) -> Dict[str, Dict]:
    with open(path, 'r') as file:
        data = load(
            file
        )
        file.close()

    return data


def __scrapeOSINTSites(credentials: Dict[str, Dict]) -> Dict:
    emailrepScraper = EmailrepScraper()
    dehashedScraper = DehashedScraper()

    email = credentials.get('OSINT').get('email')

    emailrepScraper.scrape(user_email=email)
    dehashedScraper.scrape(user_email=email)

    return {
        'Emailrep': emailrepScraper.get_parsed_data(),
        'Dehashed': dehashedScraper.get_parsed_data()
    }


def __scrapeSocialNetworks(credentials: Dict[str, Dict]) -> Dict:
    vkScraper = VkScraper()
    liScraper = LiScraper()
    fbScraper = FbScraper()
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

        fbScraper.scrape(user=fb_id, user_access_token=fb_token)

    if 'MyMailRu' in credentials:
        mm_id = credentials.get('MyMailRu').get('id')
        mmScraper.scrape(email=mm_id)

    return {
        'Vkontakte' : vkScraper.get_parsed_data(),
        'Facebook'  : fbScraper.get_parsed_data(),
        'Twitter'   : twScraper.get_parsed_data(),
        'MyMail'    : mmScraper.get_parsed_data(),
        'LinkedIn'  : liScraper.get_parsed_data()
    }


def _runScraperScripts(args: Namespace):
    results_dir = args.o
    user_creds_file = args.u

    user_creds = _readInputData(path=user_creds_file)

    scraped_data = {}
    scraped_data.update(
        __scrapeOSINTSites(credentials=user_creds)
    )
    scraped_data.update(
        __scrapeSocialNetworks(credentials=user_creds)
    )

    _writeOutResults(
        results_dir,
        scraped_data
    )

    info(msg='[+]\tThe scraping process has been done!')


if __name__ == '__main__':
    argumentParser = ArgumentParser(
        prog='PersonScraper',
        usage='''
                ./simple_run.py {-u --user-file} [-o --output-file] 
            ''',
        description='''
                This python script automate process of scraping information from social networks and gos-sites
            ''',
        add_help=True,
        allow_abbrev=True
    )

    argumentParser.add_argument(
        '-u', metavar='--user-file', type=str, required=True,
        help='Specify file with user credentials.'
    )
    argumentParser.add_argument(
        '-o', metavar='--output-file', type=str, required=False,
        help='Specify path to output file.',
        default=str(Path() / 'Results')
    )

    arguments = argumentParser.parse_args()
    _runScraperScripts(args=arguments)
