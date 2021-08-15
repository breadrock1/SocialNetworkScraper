import json

from typing import Dict
from flask import Flask, request, abort

from config import HOST, PORT
from scrapers.scraper_manager import ScraperManager


app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
