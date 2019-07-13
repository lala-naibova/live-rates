from sources import CurrencyAzSource

currency_az = CurrencyAzSource()

yes_no = 'y'


def get_currency_input(src, message):
    curr = input(message)

    is_valid, error = src.validate_currency(curr.upper())

    while not is_valid:
        print(error)
        curr = input(message)
        is_valid, error = src.validate_currency(curr.upper())

    return curr


def number_input(msg):
    num = input(msg)
    while not num.isnumeric():
        print(f"{num} - is not a NUMBER!!!")
        num = input(msg)
    return float(num)


while yes_no.lower() == 'y':

    cur_from = get_currency_input(currency_az, 'From:')
    cur_to = get_currency_input(currency_az, 'To:')

    if cur_from.lower() == cur_to.lower():
        print('Currencies are same, please try again')
        continue

    amount = number_input("How much?")

    m_from = amount * currency_az.get_rate(cur_from)

    rate = currency_az.get_rate(cur_to)

    print(round(m_from / rate, 2), cur_to.upper())
    yes_no = input('Do you want to continue? (y/n): ')

print('bye...')
