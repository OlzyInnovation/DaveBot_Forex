# import requests
import json

# GET REST DATA

# api_key = 'B82F729F-DD09-4A7D-B7D9-9E3C60C4CF0D'
# symbol = 'BINANCE_SPOT_ADA_USDT'
# url = f'https://rest.coinapi.io/v1/symbols?filter_symbol_id={symbol}'
# headers = {'X-CoinAPI-Key': 'B82F729F-DD09-4A7D-B7D9-9E3C60C4CF0D'}
# # response = requests.get(url, headers=headers).json()
# response = requests.get(url, headers=headers)
# print(response.text)
# current_price = float(response[0]['price'])
# print(f'{symbol} Current Price is: {current_price}')

# 123655DD-2A99-4772-84F4-C7692BB7682B


# GET JSON DATA

# def get_further_price(symbol:str, period: str):
#     # global price
#     f = open(f'socket_{symbol}_{period}.json', 'r+')
#     f_json_data = json.load(f)
#     first_el_price = f_json_data[0]['price_close']
#     f.close()
#     price = first_el_price
#     print(price)

# get_further_price('BINANCE_SPOT_ADA_USDT', '5MIN')


# GET JSON DATA 2

def sort_data(symbol: str, period: str):

    f = open(f'socket_{symbol}_{period}.json', 'r+')
    f_json_data = json.load(f)
    time_open = f_json_data[0]['time_open']
    time_close = f_json_data[0]['time_close']
    time_period_start = f_json_data[0]['time_period_start']
    time_period_end = f_json_data[0]['time_period_end']
    f.close()

    sorted_open = time_open.split('T')[1].split('.')[0]
    sorted_open_hour = sorted_open.split(':')[0]
    sorted_open_minute = sorted_open.split(':')[-2]
    sorted_open_second = sorted_open.split(':')[-1]

    sorted_close = time_close.split('T')[1].split('.')[0]
    sorted_close_day = time_close.split('T')[0].split('-')[-1]
    sorted_close_hour = sorted_close.split(':')[0]
    sorted_close_minute = sorted_close.split(':')[-2]
    sorted_close_second = sorted_close.split(':')[-1]

    sorted_period_start = time_period_start.split('T')[1].split('.')[0]
    sorted_period_start_hour = sorted_period_start.split(':')[0]
    sorted_period_start_minute = sorted_period_start.split(':')[-2]
    sorted_period_start_second = sorted_period_start.split(':')[-1]

    sorted_period_end = time_period_end.split('T')[1].split('.')[0]
    sorted_period_end_hour = sorted_period_end.split(':')[0]
    sorted_period_end_minute = sorted_period_end.split(':')[-2]
    sorted_period_end_second = sorted_period_end.split(':')[-1]

    sorted_period_end_day = time_period_end.split('T')[0].split('-')[-1]

    print(f'Sorted Open: {sorted_open}')
    print(f'Sorted Open Second: {sorted_open_second}')
    print(f'Sorted Open Minute: {sorted_open_minute}')
    print(f'Sorted Open Hour: {sorted_open_hour}')

    print(f'Sorted Close: {sorted_close}')
    print(f'Sorted Close Day: {sorted_close_day}')
    print(f'Sorted Close Second: {sorted_close_second}')
    print(f'Sorted Close Minute: {sorted_close_minute}')
    print(f'Sorted Close Hour: {sorted_close_hour}')

    print(f'Sorted Period Start: {sorted_period_start}')
    print(f'Sorted Period Start Second: {sorted_period_start_second}')
    print(f'Sorted Period Start Minute: {sorted_period_start_minute}')
    print(f'Sorted Period Start Hour: {sorted_period_start_hour}')

    print(f'Sorted Period End: {sorted_period_end}')
    print(f'Sorted Period End Second: {sorted_period_end_second}')
    print(f'Sorted Period End Minute: {sorted_period_end_minute}')
    print(f'Sorted Period End Hour: {sorted_period_end_hour}')
    print(f'Sorted Period End Day: {sorted_period_end_day}')
    '''
        For 5 minute data
        if minute subtraction is >= 4 && second subtraction is >= 54

        For 15 minute data
        if minute subtraction is >= 14 && second subtraction is >= 54

        For 1 hour data
        if sorted_close_hour == sorted_period_end_hour && minute subtraction is == 59 && second subtraction is >= 54

        For 4 hour data
        if sorted_close_hour == sorted_period_end_hour && minute subtraction is == 59 && second subtraction is >= 54

        For 1 day data
        if sorted_period_end_day == sorted_close_day && sorted_close_hour == sorted_period_end_hour && minute subtraction is == 59 && second subtraction is >= 54
    '''


def search_data(symbol: str, period: str):
    f = open(f'socket_{symbol}_{period}.json', 'r+')
    f_json_data = json.load(f)
    # time_open = f_json_data[0]['time_open']
    # time_close = f_json_data[0]['time_close']
    # time_period_start = f_json_data[0]['time_period_start']
    # time_period_end = f_json_data[0]['time_period_end']
    # f.close()
    counter = 0
    for data in f_json_data:
        # print(len(data))
        # print(data['time_open'])
        # print(data)
        time_open = data['time_open']
        sorted_open = time_open.split('T')[1].split('.')[0]

        print('Time Open:  {}'.format(time_open))
        print('Sorted Open:  {}'.format(sorted_open))
        if (sorted_open == '08:50:00'):
            print('Found 6:15')
            print('Counter is {}'.format(counter))
            # print(f_json_data[counter])
            return f_json_data[counter]

        counter += 1

    # print(len(f_json_data))
    # pass


def set_current_times():
    pass


def check_zeros(number_to_check: int) -> str:
    stringified = str(number_to_check)
    try:
        if stringified[0] and stringified[1]:
            return stringified
    except IndexError:
        return '0' + stringified


def crazy_calculations(period: str, value: str):
    # f = open(f'socket_{symbol}_{period}.json', 'r+')
    # f_json_data = json.load(f)

    # time_open = f_json_data[0]['time_open']
    # sorted_open = time_open.split('T')[1].split('.')[0]

    # print('Sorted Open is: ', sorted_open)
    # print(type(sorted_open))
    join_splits = ''
    hour_split = int(value.split(':')[0])
    minute_split = int(value.split(':')[1])
    second_split = value.split(':')[-1]
    print('Minute Split is: ', hour_split)
    print('Minute Split is: ', minute_split)
    print('Second Split is: ', second_split)
    if(period == '5MIN'):
        if (hour_split == 23 and minute_split == 55):
            hour_split = 0
            minute_split = 0
        elif (minute_split == 55):
            hour_split += 1
            minute_split = 0
        else:
            minute_split += 5

    elif(period == '15MIN'):
        if (hour_split == 23 and minute_split == 45):
            hour_split = 0
            minute_split = 0
        elif (minute_split == 45):
            hour_split += 1
            minute_split = 0
        else:
            minute_split += 15
    elif(period == '1HRS'):
        if (hour_split == 23):
            hour_split = 0
        else:
            hour_split += 1
    elif(period == '4HRS'):
        if (hour_split == 20):
            hour_split = 0
        else:
            hour_split += 4

    join_splits = check_zeros(hour_split) + \
        ':' + check_zeros(minute_split) + ':' + second_split
    # call update_current_time function here instead
    print('Join SPlits: ', join_splits)
    return join_splits

    # Remember to check for hour start numbers for zeros & more


# sort_data('BINANCE_SPOT_ADA_USDT', '5MIN')
print(search_data('BINANCE_SPOT_ETH_USDT', '5MIN'))
crazy_calculations('BINANCE_SPOT_BTC_USDT', '15MIN')
print(check_zeros(0))
