from json import load
from typing import Dict
from pathlib import Path
from os.path import basename


def _read_input_data(path: str) -> Dict[str, Dict]:
    with open(path, 'r') as file:
        data = load(file)
        file.close()

    return data


def test_parse_input_file():
    path_to_file = (Path() / 'tests' / 'users' / 'yuliya_chesnokova.json').absolute()
    credentials = _read_input_data(str(path_to_file))

    try:
        assert 'twitter' in credentials
        assert 'facebook' in credentials
        assert 'linkedin' in credentials
        assert 'MyMailRu' in credentials
        assert 'vkontakte' in credentials

        assert credentials.get('vkontakte').get('id') == '633470190'
        assert credentials.get('twitter').get('id') == 'Yulia58368327'
        assert credentials.get('facebook').get('id') == '101313718664029'
        assert credentials.get('MyMailRu').get('id') == 'yuliya.chesnok.88@bk.ru'
        assert credentials.get('linkedin').get('id') == 'yulia-chesnokova-590525207'
    except AssertionError as e:
        print(f'Assertion failed: {e}')
        exit(-1)

    print(f'The test {basename(__file__)} has been finished successful!')
