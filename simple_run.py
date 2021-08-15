from typing import Dict
from pathlib import Path
from logging import info
from json import dump, load
from argparse import ArgumentParser, Namespace

from scrapers.scraper_manager import ScraperManager


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
        data = load(file)
        file.close()

    return data


def _runScraperScripts(args: Namespace):
    info(msg='[+]\tStarting scraper process...')

    results_dir = args.o
    user_credentials_file = args.u

    user_credentials = _readInputData(path=user_credentials_file)

    scraped_data = {}
    scraped_data.update(
        ScraperManager.scrapeOSINTSites(credentials=user_credentials)
    )
    scraped_data.update(
        ScraperManager.scrapeSocialNetworks(credentials=user_credentials)
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
        default=str(Path() / 'results')
    )

    arguments = argumentParser.parse_args()
    _runScraperScripts(args=arguments)
