from typing import Dict
from requests import post
from logging import info


# Запрос списка сообщений, опубликованных за дату
params_1 = '''
<startDate>2014-12-14T00:00:00</startDate>
<endDate xsi:nil="true"/>
'''

# Запрос сообщения по id
params_2 = '''
<id>156460</id>
'''


class FedresScraper(object):
    def __init__(self):
        self.parsed_data = {}

    def __gen_fedres_data(self, data: str) -> str:
        response = post(
            url='https://fedresurs.ru',
            data=data,
            headers={
                'Content-Type': 'application/xml'
            },
            verify=False,
            allow_redirects=False
        )

        if response.status_code != 200:
            return ''

        return response.text

    def get_parsed_data(self) -> Dict[str, str or Dict]:
        return self.parsed_data

    def scrape(self, user_data: Dict[str, str]) -> None:
        info(msg='[*]\tStarting the Fedresurs scraping process...', level=0)

        template = '''
                <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
                <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                    <GetMessageIds xmlns="http://tempuri.org/"> %s </GetMessageIds>
                </s:Body>
                </s:Envelope>
            '''

        user_data = self.__gen_fedres_data(
            data=(template % params_1)
        )

        self.parsed_data.update({
            'user_data': user_data
        })

        info(msg='[+]\tThe Fedresurs scraping process has been done!', level=0)
