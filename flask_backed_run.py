import json

from typing import Dict, List
from flask import Flask, request, abort

from config import HOST, PORT
from Scrapers.ScraperManager import ScraperManager


app = Flask(__name__)


def extractDictDataByKey(json_data: json, key: str) -> List[str]:
    try:
        return json_data.get(key)
    except KeyError as e:
        print(f'Error while parsing request json-data: {e.with_traceback()}')
        return []


def launchScrapingProcess(credentials: json, mode: str) -> Dict:
    if mode == 'full_scraping':
        scraped_data = {}

        scraped_data.update(
            ScraperManager.scrapeOSINTSites(credentials=credentials)
        )

        scraped_data.update(
            ScraperManager.scrapeSocialNetworks(credentials=credentials)
        )

        return scraped_data

    elif mode == 'vk_scraping':
        vk_ids = extractDictDataByKey(json_data=credentials, key='ids')

        return ScraperManager.scrapeVkontakte(ids=vk_ids)

    elif mode == 'osint_scraping':
        return ScraperManager.scrapeOSINTSites(credentials=credentials)

    elif mode == 'social_scraping':
        return ScraperManager.scrapeSocialNetworks(credentials=credentials)

    return {'Error': 'Wrong request...'}


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def indexPage():
    return {}


@app.route('/full_scraping', methods=['POST'])
def launchFullScraping():
    if request.method == 'POST':
        return launchScrapingProcess(credentials=request.get_json(), mode='full_scraping')

    abort(405)


@app.route('/social_scraping', methods=['POST'])
def launchSocialScraping():
    if request.method == 'POST':
        return launchScrapingProcess(credentials=request.get_json(), mode='social_scraping')

    abort(405)


@app.route('/osint_scraping', methods=['POST'])
def launchOsintScraping():
    if request.method == 'POST':
        return launchScrapingProcess(credentials=request.get_json(), mode='osint_scraping')

    abort(405)


@app.route('/vk_scraping', methods=['POST'])
def launchVkScraping():
    if request.method == 'POST':
        return launchScrapingProcess(credentials=request.get_json(), mode='vk_scraping')

    abort(405)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
