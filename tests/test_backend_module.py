import json

from time import sleep
from pathlib import Path
from requests import post
from flask_backed_run import app
from multiprocessing import Process


result_full_scraping_response = {
    'Dehashed': {},
    'Emailrep': {},
    'facebook': {},
    'linkedin': {},
    'mymail': {},
    'twitter': {},
    'vkontakte': {
        'birthday': None,
        'city': {},
        'first_name': None,
        'followers': [],
        'friends': [],
        'groups': [],
        'last_name': None,
        'posts': []
    }
}


def _runBackendApp() -> None:
    app.run(host='127.0.0.1', port=7654)


def _createProcess() -> Process:
    return Process(target=_runBackendApp, name='flask_backend_process')


def _readUserFile() -> json:
    file_path = Path('users', 'yuliya_chesnokova.json').absolute()
    user_file = open(str(file_path), 'rb')

    return json.load(user_file)


def _sendRequestToScraping(mode: str) -> json:
    response = post(
        url=f'http://127.0.0.1:7654/{mode}',
        json=_readUserFile()
    )

    return response.json()


def test_backend_module():
    backend_process = _createProcess()
    backend_process.start()

    sleep(2)

    try:
        response_index = _sendRequestToScraping(mode='index')
        response_full_scraping = _sendRequestToScraping(mode='full_scraping')

        assert response_index == {}
        assert response_full_scraping == result_full_scraping_response

    except Exception as e:
        print(f'Error while executing request. {e.with_traceback}')

    finally:
        backend_process.kill()
