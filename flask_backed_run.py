import json
from typing import Dict
from flask import Flask, request, abort

from Scrapers.SraperManager import ScraperManager


app = Flask(__name__)


def loadJsonData(data) -> json:
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        print(f'[-]\tFailed to decode json data. Error: {e.msg}')
        return {'result': -1, 'message': e.msg}


def scrapeFull(credentials: json) -> Dict:
    scraped_data = {}

    scraped_data.update(
        ScraperManager.scrapeOSINTSites(credentials=credentials)
    )
    scraped_data.update(
        ScraperManager.scrapeSocialNetworks(credentials=credentials)
    )

    return scraped_data


@app.route('/full_osint', methods=['POST'])
def startFullOsintModule():
    if request.method == 'POST':
        data = request.get_data().decode('UTF-8')
        user_creds = loadJsonData(data)

        return scrapeFull(credentials=user_creds)

    abort(405)
