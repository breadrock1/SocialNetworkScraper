from json import load
from typing import Dict
from pathlib import Path
from os.path import basename


def _readInputData(path: str) -> Dict[str, Dict]:
    with open(path, 'r') as file:
        data = load(
            file
        )
        file.close()

    return data


if __name__ == '__main__':
    path_to_file = (Path() / 'Users' / 'yuliya_chesnokova.json').absolute()
    credentials = _readInputData(str(path_to_file))

    try:
        assert 'Twitter' in credentials
        assert 'Facebook' in credentials
        assert 'LinkedIn' in credentials
        assert 'MyMailRu' in credentials
        assert 'Vkontakte' in credentials

        assert credentials.get('Vkontakte').get('id') == '633470190'
        assert credentials.get('Twitter').get('id') == 'Yulia58368327'
        assert credentials.get('Facebook').get('id') == '101313718664029'
        assert credentials.get('MyMailRu').get('id') == 'yuliya.chesnok.88@bk.ru'
        assert credentials.get('LinkedIn').get('id') == 'yulia-chesnokova-590525207'
    except AssertionError as e:
        print(f'Assertion failed: {e}')
        exit(-1)

    print(f'The test {basename(__file__)} has been finished successful!')