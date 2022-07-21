from websocket import create_connection
import json
from os.path import exists as file_exists



api_key =  "123655DD-2A99-4772-84F4-C7692BB7682B"


class CoinAPIv1_subscribe(object):
  def __init__(self, apikey):
    self.type = "hello"
    self.apikey = apikey
    self.heartbeat = False
    self.subscribe_data_type = ["ohlcv"]
    self.subscribe_filter_period_id = ['5MIN', '15MIN', '1HRS', '4HRS', '1DAY']
    self.subscribe_filter_symbol_id = ['BINANCE_SPOT_MATIC_USDT','BINANCE_SPOT_LUNA_USDT', 'BINANCE_SPOT_ETH_USDT', 'BINANCE_SPOT_ADA_USDT', 'BINANCE_SPOT_SOL_USDT', 'BINANCE_SPOT_CRV_USDT','BINANCE_SPOT_BTC_USDT' ]


def sort_data(msg: dict):
  period_id = msg['period_id']
  time_period_start = msg['time_period_start']
  time_period_end = msg['time_period_end']
  time_open = msg['time_open']
  time_close = msg['time_close']
  price_open = msg['price_open']
  price_high = msg['price_high']
  price_low = msg['price_low']
  price_close = msg['price_close']
  volume_traded = msg['volume_traded']
  trades_count = msg['trades_count']
  symbol_id = msg['symbol_id']

  new_dict: dict = {
      "time_period_start": time_period_start,
      "time_period_end": time_period_end,
      "time_open": time_open,
      "time_close": time_close,
      "price_open": price_open,
      "price_high": price_high,
      "price_low": price_low,
      "price_close": price_close,
      "volume_traded": volume_traded,
      "trades_count": trades_count
    }
  is_file =  file_exists(f'socket_{symbol_id}_{period_id}.json')
  if is_file:
    f = open(f'socket_{symbol_id}_{period_id}.json', 'r+')
    json_data = json.load(f)
    json_data.insert(0, new_dict)
    f.seek(0)
    f.write(str(json_data))
    f.truncate()

    # read input file
    final = open(f'socket_{symbol_id}_{period_id}.json', "r")
    # read file contents to string
    data = final.read()
    # replace all occurrences of the single quote
    data = data.replace('\'', '"')
    # close the input file
    final.close()
    # open the input file in write mode
    final = open(f'socket_{symbol_id}_{period_id}.json', "w")
    # overrite the input file with the resulting data
    final.write(data)
    # close the file
    final.close()

    print('Added new entry!')
  else:
    print(f'socket_{symbol_id}_{period_id}.json does not exist')
    g = open(f'socket_{symbol_id}_{period_id}.json', 'w')
    # arr = []
    g.write(str([]))
    g.close()

    f = open(f'socket_{symbol_id}_{period_id}.json', 'r+')
    json_data = json.load(f)
    json_data.insert(0, new_dict)
    f.seek(0)
    f.write(str(json_data))
    f.truncate()

    # read input file
    final = open(f'socket_{symbol_id}_{period_id}.json', "r")
    # read file contents to string
    data = final.read()
    # replace all occurrences of the single quote
    data = data.replace('\'', '"')
    # close the input file
    final.close()
    # open the input file in write mode
    final = open(f'socket_{symbol_id}_{period_id}.json', "w")
    # overrite the input file with the resulting data
    final.write(data)
    # close the file
    final.close()

    print('Created and Added new entry!')



ws = create_connection("wss://ws.coinapi.io/v1")
sub = CoinAPIv1_subscribe(api_key)
ws.send(json.dumps(sub.__dict__))

while True:
  msg =  json.loads(ws.recv())
  sort_data(msg)