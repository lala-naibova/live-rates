import requests
import re


def get_rate(currency):

    if currency.lower() == 'azn':
        return 1

    request = requests.get('http://currency.az')
    content = request.content.decode()
    pattern = f'[a-z <">=]+1 {currency}[a-z /"<>=-]+(?P<rate>[0-9.]+) AZN'
    match = re.search(pattern, content, re.IGNORECASE)
    result = match.group('rate')
    return float(result)


yes_no = 'y'
while yes_no.lower() == 'y':
    cur1 = input('From:')
    cur2 = input('To:')
    if cur1.lower() == cur2.lower():
        print('Currencies are same, please try again')
        continue

    amount = float(input('How much? '))

    m_from = amount * get_rate(cur1)

    rate = get_rate(cur2)

    print(round(m_from / rate, 2), cur2.upper())
    yes_no = input('Do you want to continue? (y/n): ')

