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


sort_data('BINANCE_SPOT_ADA_USDT', '5MIN')
