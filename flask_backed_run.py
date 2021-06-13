import json

from typing import Dict, Union
from flask import Flask, request, abort

from Scrapers.SraperManager import ScraperManager


app = Flask(__name__)


def loadJsonDataFromRequest(data: Union[bytes, str]) -> json:
    try:
        return json.loads(data)

    except json.JSONDecodeError as e:
        print(f'[-]\tFailed to decode json data. Error: {e.msg}')
        return {'result': -1, 'message': e.msg}


def launchScrapingProcess(credentials: json, mode: str) -> Dict:
    scraped_data = {}

    if mode == '/social_scraping':
        scraped_data.update(
            ScraperManager.scrapeSocialNetworks(credentials=credentials)
        )

    elif mode == 'osint_scraping':
        scraped_data.update(
            ScraperManager.scrapeOSINTSites(credentials=credentials)
        )

    else:
        scraped_data.update(
            ScraperManager.scrapeSocialNetworks(credentials=credentials)
        )
        scraped_data.update(
            ScraperManager.scrapeOSINTSites(credentials=credentials)
        )

    return scraped_data


@app.route('/full_scraping', methods=['POST'])
def launchFullScraping():
    if request.method == 'POST':
        data = request.get_data().decode('UTF-8')
        user_creds = loadJsonDataFromRequest(data)

        return launchScrapingProcess(credentials=user_creds, mode='full_scraping')

    abort(405)


@app.route('/social_scraping', methods=['POST'])
def launchSocialScraping():
    if request.method == 'POST':
        data = request.get_data().decode('UTF-8')
        user_creds = loadJsonDataFromRequest(data)

        return launchScrapingProcess(credentials=user_creds, mode='social_scraping')

    abort(405)


@app.route('/osint_scraping', methods=['POST'])
def launchOsintScraping():
    if request.method == 'POST':
        data = request.get_data().decode('UTF-8')
        user_creds = loadJsonDataFromRequest(data)

        return launchScrapingProcess(credentials=user_creds, mode='osint_scraping')

    abort(405)


if __name__ == "__main__":
    port = 8080
    host = "0.0.0.0"
    app.run(host=host, port=port)
