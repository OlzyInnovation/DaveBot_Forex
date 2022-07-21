# import requests
import json

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



def get_further_price(symbol:str, period: str):
    # global price
    f = open(f'socket_{symbol}_{period}.json', 'r+')
    f_json_data = json.load(f)
    first_el_price = f_json_data[0]['price_close']
    f.close()
    price = first_el_price
    print(price)

get_further_price('BINANCE_SPOT_ADA_USDT', '5MIN')