import requests
import re


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

    def get_rate(self, currency):
        pass

    def get_supported_currencies(self):
        pass

    def is_alive(self):
        pass

