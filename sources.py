import requests
import re
from datetime import datetime


class CurrencyAzSource:


    def is_alive(self):
        pass

    def get_supported_currencies(self):
        return ('AZN', 'USD', 'EUR', 'RUB')

    def get_rate(self, currency):
        if currency.lower() == 'azn':
            return 1

        request = requests.get('http://currency.az')
        content = request.content.decode()
        pattern = f'[a-z <">=]+1 {currency}[a-z /"<>=-]+(?P<rate>[0-9.]+) AZN'
        match = re.search(pattern, content, re.IGNORECASE)
        result = match.group('rate')
        return float(result)


    def validate_currency(self, curr):
        if curr in self.get_supported_currencies():
            return True, 'valid'
        else:
            return False, f'There isn\'t any currency  type as {curr.upper()}. Try again'


class CentralBankSource:

    def build_url(self):
        now = datetime.now()
        new_day = now.strftime('%d.%m.%Y')
        return f'https://www.cbar.az/currencies/{new_day}.xml'

    def get_rate(self, currency):
        if currency.upper() == 'AZN':
            return 1
        pattern = r'<Valute Code="(?P<valute>{})">\n.+\n.+\n +<Value>(?P<value>[0-9]+\.[0-9]+)'.format(currency)
        response = requests.get(self.build_url())
        content = response.content.decode()
        match = re.search(pattern, content, re.IGNORECASE)
        return float(match.group('value'))

    def get_all_rates(self):
        pattern = r'<Valute Code="(?P<valute_code>[a-z]+)">\n +.+\n +<Name>(?P<name>[^<]+)</Name>\n +<Value>(?P<value>[0-9.]+)'

        response = requests.get(self.build_url())
        content = response.content.decode()
        matches = re.findall(pattern, content, re.IGNORECASE)
        result = []
        for match in matches:
            rate = {}
            rate['code'] = match[0]
            rate['name'] = match[1]
            rate['rate'] = float(match[2])
            result.append(rate)
        return result

    def get_supported_currencies(self):
        pattern = r'<Valute Code="(?P<valute>[a-z]+)">\n.+\n.+\n +<Value>(?P<value>[0-9]+\.[0-9]+)'
        response = requests.get(self.build_url())
        content = response.content.decode()
        matches = re.findall(pattern, content, re.IGNORECASE)
        valutes = ['AZN']
        for match in matches:
            valutes.append(match[0])
        return valutes

    def is_alive(self):
        response = requests.get(self.build_url())
        return bool(response)

    def validate_currency(self, curr):
        if curr in self.get_supported_currencies():
            return True, 'valid'
        else:
            return False, f'There isn\'t any currency  type as {curr.upper()}. Try again'

