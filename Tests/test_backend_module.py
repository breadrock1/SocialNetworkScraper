import json

from time import sleep
from pathlib import Path
from typing import Dict

from requests import post
from flask_backed_run import app
from multiprocessing import Process


result_full_scraping_response = {
    'Dehashed': {},
    'Emailrep': {},
    'Facebook': {},
    'LinkedIn': {},
    'MyMail': {},
    'Twitter': {},
    'Vkontakte': {
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


def _readUserFile(file_path: Path) -> json:
    user_file = open(str(file_path), 'rb')

    return json.load(user_file)


def _sendRequestToScraping(mode: str, json_data: Dict) -> json:
    response = post(
        url=f'http://127.0.0.1:7654/{mode}',
        json=json_data
    )

    return response.json()


def test_backend_module():
    backend_process = _createProcess()
    backend_process.start()

    sleep(2)

    vk_ids_file = Path('Tests', 'Users', 'vk_ids.json').absolute()
    user_file = Path('Tests', 'Users', 'yuliya_chesnokova.json').absolute()

    user_data = _readUserFile(file_path=user_file)
    vk_ids_data = _readUserFile(file_path=vk_ids_file)

    try:
        response_index = _sendRequestToScraping(mode='index', json_data=user_data)
        response_vk_scraping = _sendRequestToScraping(mode='vk_scraping', json_data=vk_ids_data)
        response_full_scraping = _sendRequestToScraping(mode='full_scraping', json_data=user_data)

        assert response_index == {}
        assert response_vk_scraping == {}
        assert response_full_scraping == result_full_scraping_response

    except Exception as e:
        print(f'Error while executing request. {e.with_traceback}')

    finally:
        backend_process.kill()
