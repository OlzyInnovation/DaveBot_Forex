import requests
import json
import time
from datetime import datetime, timedelta
from pymongo import MongoClient

# from automation import workbook
from symbols import symbols
from periods import periods
from utils import crazy_calculations, search_data, days_months_years


# Calculate time for period time lapse
t = time.localtime()
start_time = time.strftime("%H:%M:%S", t)
print(f'Data fetch starting at: {start_time}')

now = datetime.now()

print(f'now: {now}')

# Counter to switch to socket
counter = 0

# Refresh Times
five_minutes = now + timedelta(minutes=5)
fifteen_minutes = now + timedelta(minutes=15)
one_hour = now + timedelta(hours=1)
four_hours = now + timedelta(hours=4)
one_day = now + timedelta(hours=24)

# # Moving Averages
five_minutes_moving_average: list = []
fifteen_minutes_moving_average: list = []
one_hour_moving_average: list = []
four_hour_moving_average: list = []
one_day_moving_average: list = []

# Price
price: float = 0


# Period lists
five_min_period = []
fifteen_min_period = []
one_hour_period = []
four_hour_period = []
one_day_period = []

# Sorted lists
# Five Minutes
five_min_open = []
five_min_close = []
five_min_high = []
five_min_low = []

# Fifteen Minutes
fifteen_min_open = []
fifteen_min_close = []
fifteen_min_high = []
fifteen_min_low = []

# One Hour
one_hour_open = []
one_hour_close = []
one_hour_high = []
one_hour_low = []

# Four Hours
four_hours_open = []
four_hours_close = []
four_hours_high = []
four_hours_low = []

# One Day
one_day_open = []
one_day_close = []
one_day_high = []
one_day_low = []

# Current Times
five_min_start_current = ''
five_min_end_current = ''
fifteen_min_start_current = ''
fifteen_min_end_current = ''
one_hour_start_current = ''
one_hour_end_current = ''
four_hour_start_current = ''
four_hour_end_current = ''
one_day_start_current = ''
one_day_end_current = ''
day_track_start = ''
day_track_end = ''
month_track_start = ''
month_track_end = ''
year_track_start = ''
year_track_end = ''

# Sleep Time
sleep_time = 300

# API_KEY
api_key = ''  # api Key

client = MongoClient()


def create_db():
    try:
        global client
        dbs = client.list_database_names()
        if 'variables' in dbs:
            client.drop_database('variables')
            print('Previous Database Deleted')
        db = client.variables
        variables = db.variables
        for i in range(0, len(symbols)):
            variable_dict = {"symbol": symbols[i], "values": {"5MIN": {"success": 0, "unsuccess": 0, "black_x": 0, "price": 0, "ma": 0}, "15MIN": {"success": 0, "unsuccess": 0, "black_x": 0, "price": 0, "ma": 0}, "1HRS": {
                "success": 0, "unsuccess": 0, "black_x": 0, "price": 0, "ma": 0}, "4HRS": {"success": 0, "unsuccess": 0, "black_x": 0, "price": 0, "ma": 0}, "1DAY": {"success": 0, "unsuccess": 0, "black_x": 0, "price": 0, "ma": 0}}}

            variables.insert_one(variable_dict)

        print("Database Created")
    except Exception as e:
        print(f"Database not created {e}")


def search_db(symbol: str, period: str) -> list[int]:
    try:
        global client
        db = client.variables
        variables = db.variables
        new_list = []
        sym = variables.find_one({"symbol": symbol})
        # success_count = sym[period][0]
        success_count = int(sym['values'][period]['success'])
        # success_count = int(sym['values'][period]['success'])
        unsuccess_count = int(sym['values'][period]['unsuccess'])
        # blackx_count = sym[period][1]
        blackx_count = int(sym['values'][period]['black_x'])
        new_list.append(success_count)
        new_list.append(unsuccess_count)
        new_list.append(blackx_count)
        return new_list
    except Exception as e:
        print(f"Error occured with database search: {e}")


def update_db(symbol: str, period: str, success: int, unsuccess: int, black_x: int, price, ma) -> None:
    try:
        global client
        db = client.variables
        variables = db.variables

        new_values = {'success': success, 'unsuccess': unsuccess,
                      'black_x': black_x, "price": price, "ma": ma}
        myquery = {"symbol": symbol}
        newvalues = {"$set": {f"values.{period}": new_values}}

        variables.update_one(myquery, newvalues)
        print(f'{symbol} {period} values updated to: Success -> {success}, Unsuccess -> {unsuccess}, Black_x -> {black_x}')
    except Exception as e:
        print(f"Error occured with database update: {e}")


def get_current_price(symbol: str) -> str:
    global price

    try:
        url = f'https://rest.coinapi.io/v1/symbols?filter_symbol_id={symbol}'
        headers = {'X-CoinAPI-Key': f'{api_key}'}
        response = requests.get(url, headers=headers).json()
        current_price = float(response[0]['price'])
        print(f'{symbol} Current Price is: {current_price}')

        price = current_price
    except Exception as e:
        return f"Could not fetch current price: {e}"


# This calculates the moving averages for each given period
# and is abstracted out for easier CI (continuous integration)
def calculate_ma(total: float, period: str):
    global five_minutes_moving_average
    global fifteen_minutes_moving_average
    global one_hour_moving_average
    global four_hour_moving_average
    global one_day_moving_average
    try:
        ma: float = 20.0
        moving_average = float(total / ma)
        if period == '5MIN':

            five_minutes_moving_average.append(moving_average)

        with open(f'{period}_ma_confirmation.json', 'w') as f:
            f.write(str(five_minutes_moving_average))

        if period == '15MIN':

            fifteen_minutes_moving_average.append(moving_average)

        if period == '1HRS':

            one_hour_moving_average.append(moving_average)
        if period == '4HRS':

            four_hour_moving_average.append(moving_average)
        if period == '1DAY':

            one_day_moving_average.append(moving_average)
    except Exception as e:
        print(f"Moving Average Calculation Error: {e}")

# Based on period, sorts the periods' close data and calls the 'calculate_ma' function


def new_function(param: list, period: str):
    global counter
    try:
        # print(f'Total Range is currently, {total_range}')
        track = 0
        #     track = 0
        # elif counter > 0:
        #     track = 0

        if counter <= 0:
            if period == '5MIN':
                for i in range(0, len(param)):
                    if track == 20:
                        continue
                    else:
                        total = 0
                        split_list = param[track:track + 20]
                        for i in range(0, len(split_list)):
                            total += float(split_list[i])
                        track += 1
                        calculate_ma(total, period)
            if period == '15MIN':
                for i in range(0, len(param)):
                    if track == 20:
                        continue
                    else:
                        total = 0
                        split_list = param[track:track + 20]
                        for i in range(0, len(split_list)):
                            total += float(split_list[i])
                        track += 1
                        calculate_ma(total, period)
            if period == '1HRS':
                for i in range(0, len(param)):
                    if track == 20:
                        continue
                    else:
                        total = 0
                        split_list = param[track:track + 20]
                        for i in range(0, len(split_list)):
                            total += float(split_list[i])
                        track += 1
                        calculate_ma(total, period)
            if period == '4HRS':
                for i in range(0, len(param)):
                    if track == 20:
                        continue
                    else:
                        total = 0
                        split_list = param[track:track + 20]
                        for i in range(0, len(split_list)):
                            total += float(split_list[i])
                        track += 1
                        calculate_ma(total, period)
            if period == '1DAY':
                for i in range(0, len(param)):
                    if track == 20:
                        continue
                    else:
                        total = 0
                        split_list = param[track:track + 20]
                        for i in range(0, len(split_list)):
                            total += float(split_list[i])
                        track += 1
                        calculate_ma(total, period)
        elif counter > 0:
            if period == '5MIN':
                for i in range(0, len(param)):
                    if track == 1:
                        continue
                    else:
                        total = 0
                        split_list = param[track:track + 20]
                        for i in range(0, len(split_list)):
                            total += float(split_list[i])
                        track += 1
                        calculate_ma(total, period)
            if period == '15MIN':
                for i in range(0, len(param)):
                    if track == 1:
                        continue
                    else:
                        total = 0
                        split_list = param[track:track + 20]
                        for i in range(0, len(split_list)):
                            total += float(split_list[i])
                        track += 1
                        calculate_ma(total, period)
            if period == '1HRS':
                for i in range(0, len(param)):
                    if track == 1:
                        continue
                    else:
                        total = 0
                        split_list = param[track:track + 20]
                        for i in range(0, len(split_list)):
                            total += float(split_list[i])
                        track += 1
                        calculate_ma(total, period)
            if period == '4HRS':
                for i in range(0, len(param)):
                    if track == 1:
                        continue
                    else:
                        total = 0
                        split_list = param[track:track + 20]
                        for i in range(0, len(split_list)):
                            total += float(split_list[i])
                        track += 1
                        calculate_ma(total, period)
            if period == '1DAY':
                for i in range(0, len(param)):
                    if track == 1:
                        continue
                    else:
                        total = 0
                        split_list = param[track:track + 20]
                        for i in range(0, len(split_list)):
                            total += float(split_list[i])
                        track += 1
                        calculate_ma(total, period)
    except Exception as e:
        print(f"Error occured during sorting: {e}")


def create_json(symbol: str, period: str, param: list):
    try:

        with open(f'{symbol}_{period}_data.json', 'w+') as f:
            f.write(str(param))

        # read input file
        final = open(f'{symbol}_{period}_data.json', "r")
        # read file contents to string
        data = final.read()
        # replace all occurrences of the single quote
        data = data.replace('\'', '"')
        # close the input file
        final.close()
        # open the input file in write mode
        final = open(f'{symbol}_{period}_data.json', "w")
        # overrite the input file with the resulting data
        final.write(data)
        # close the file
        final.close()
    except Exception as e:
        print(f"Could not edit json files: {e}")


def edit_json(symbol: str, period: str):
    global five_min_start_current
    global five_min_end_current
    global fifteen_min_start_current
    global fifteen_min_end_current
    global one_hour_start_current
    global one_hour_end_current
    global four_hour_start_current
    global four_hour_end_current
    global one_day_start_current
    global one_day_end_current
    new_data = ''

    try:
        if period == '5MIN':
            new_data = search_data(
                symbol, period, five_min_start_current, five_min_end_current)
        if period == '15MIN':
            new_data = search_data(
                symbol, period, fifteen_min_start_current, fifteen_min_end_current)
        if period == '1HRS':
            new_data = search_data(
                symbol, period, one_hour_start_current, one_hour_end_current)
        if period == '4HRS':
            new_data = search_data(
                symbol, period, four_hour_start_current, four_hour_end_current)
        if period == '1DAY':
            new_data = search_data(
                symbol, period, one_day_start_current, one_day_end_current)

        print(f'New Data: {new_data}')

        # New
        # f = open(f'socket_{symbol}_{period}.json', 'r+')
        # f_json_data = json.load(f)
        # first_el = f_json_data[0]
        # f.close()

        g = open(f'{symbol}_{period}_data.json', 'r+')
        g_json_data = json.load(g)
        # g_json_data.insert(0, first_el)
        g_json_data.insert(0, new_data)
        g.seek(0)
        g.write(str(g_json_data))
        g.truncate()
        g.close()

        # Old
        # Edit and replace single quotes with double quotes
        # read input file
        final = open(f'{symbol}_{period}_data.json', "r")
        # read file contents to string
        data = final.read()
        # replace all occurrences of the single quote
        data = data.replace('\'', '"')
        # close the input file
        final.close()
        # open the input file in write mode
        final = open(f'{symbol}_{period}_data.json', "w")
        # overrite the input file with the resulting data
        final.write(data)
        # close the file
        final.close()
    except Exception as e:
        print(f"Could not create json files: {e}")


def reset_timer():
    print('Reset Timer...')
    current_time = datetime.now()
    global five_minutes
    global fifteen_minutes
    global one_hour
    global four_hours
    global one_day

    '''

    global symbols
    global five_min_start_current
    global five_min_end_current
    global fifteen_min_start_current
    global fifteen_min_end_current
    global one_hour_start_current
    global one_hour_end_current
    global four_hour_start_current
    global four_hour_end_current
    global one_day_start_current
    global one_day_end_current

    '''

    if current_time >= five_minutes:
        five_minutes = current_time + timedelta(minutes=5)
        update_current_times('5MIN')
        print('Five Minutes Timer Reset!')
    if current_time >= fifteen_minutes:
        fifteen_minutes = current_time + timedelta(minutes=15)
        update_current_times('15MIN')
        print('Fifteen Minutes Timer Reset!')
    if current_time >= one_hour:
        one_hour = current_time + timedelta(hours=1)
        update_current_times('1HRS')
        print('One Hour Timer Reset!')
    if current_time >= four_hours:
        four_hours = current_time + timedelta(hours=4)
        update_current_times('4HRS')
        print('Four Hours Timer Reset!')
    if current_time >= one_day:
        one_day = current_time + timedelta(hours=24)
        update_current_times('1DAY')
        print('One Day Timer Reset!')

    print('Reset Timer Done!...')


def get_further_price(symbol: str, period: str):
    global price
    f = open(f'{symbol}_{period}_data.json', 'r+')
    f_json_data = json.load(f)
    first_el_price = f_json_data[0]['price_close']
    f.close()
    price = first_el_price


def further_runs():
    print('Further Runs...')
    # Timers
    global five_minutes
    global fifteen_minutes
    global one_hour
    global four_hours
    global one_day
    # Current Times
    global five_min_start_current
    global five_min_end_current
    global fifteen_min_start_current
    global fifteen_min_end_current
    global one_hour_start_current
    global one_hour_end_current
    global four_hour_start_current
    global four_hour_end_current
    global one_day_start_current
    global one_day_end_current
    for symbol in symbols:
        for period in periods:
            if period == '5MIN' and datetime.now() >= five_minutes:
                edit_json(symbol, period)
                get_further_price(symbol, period)
                get_keys(symbol, period)
                s_count, un_count, x_count = search_db(symbol, period)
                calculate(period, symbol, s_count, un_count, x_count)
            if period == '15MIN' and datetime.now() >= fifteen_minutes:
                edit_json(symbol, period)
                get_keys(symbol, period)
                s_count, un_count, x_count = search_db(symbol, period)
                calculate(period, symbol, s_count, un_count, x_count)
            if period == '1HRS' and datetime.now() >= one_hour:
                edit_json(symbol, period)
                get_keys(symbol, period)
                s_count, un_count, x_count = search_db(symbol, period)
                calculate(period, symbol, s_count, un_count, x_count)
            if period == '4HRS' and datetime.now() >= four_hours:
                edit_json(symbol, period)
                get_keys(symbol, period)
                s_count, un_count, x_count = search_db(symbol, period)
                calculate(period, symbol, s_count, un_count, x_count)
            if period == '1DAY' and datetime.now() >= one_day:
                edit_json(symbol, period)
                get_keys(symbol, period)
                s_count, un_count, x_count = search_db(symbol, period)
                calculate(period, symbol, s_count, un_count, x_count)

    print('Further runs done, calling reset...')
    reset_timer()


# Based on period, opens the periods' json data, sorts it and creates new json OHLC files
# On new OHLC json files creation, also based on period, calls the 'new_function' function
def get_keys(symbol: str, period: str):
    # global five_minutes_moving_average
    # global fifteen_minutes_moving_average
    # global one_hour_moving_average
    # global four_hour_moving_average
    # global one_day_moving_average

    with open(f'{symbol}_{period}_data.json', 'r+') as f:
        json_data = json.load(f)
        # first_el_price = json_data[0]
        for i in json_data:
            # now i is a dict
            for key in i.keys():
                if period == '5MIN':
                    if key == 'price_close':
                        # print every key of each dict
                        five_min_close.append(float(i.get(key)))
                    elif key == 'price_open':
                        five_min_open.append(float(i.get(key)))
                    elif key == 'price_high':
                        five_min_high.append(float(i.get(key)))
                    elif key == 'price_low':
                        five_min_low.append(float(i.get(key)))

                elif period == '15MIN':
                    if key == 'price_close':
                        # print every key of each dict
                        fifteen_min_close.append(float(i.get(key)))
                    elif key == 'price_open':
                        fifteen_min_open.append(float(i.get(key)))
                    elif key == 'price_high':
                        fifteen_min_high.append(float(i.get(key)))
                    elif key == 'price_low':
                        fifteen_min_low.append(float(i.get(key)))

                elif period == '1HRS':
                    if key == 'price_close':
                        # print every key of each dict
                        one_hour_close.append(float(i.get(key)))
                    elif key == 'price_open':
                        one_hour_open.append(float(i.get(key)))
                    elif key == 'price_high':
                        one_hour_high.append(float(i.get(key)))
                    elif key == 'price_low':
                        one_hour_low.append(float(i.get(key)))

                elif period == '4HRS':
                    if key == 'price_close':
                        # print every key of each dict
                        four_hours_close.append(float(i.get(key)))
                    elif key == 'price_open':
                        four_hours_open.append(float(i.get(key)))
                    elif key == 'price_high':
                        four_hours_high.append(float(i.get(key)))
                    elif key == 'price_low':
                        four_hours_low.append(float(i.get(key)))

                elif period == '1DAY':
                    if key == 'price_close':
                        # print every key of each dict
                        one_day_close.append(float(i.get(key)))
                    elif key == 'price_open':
                        one_day_open.append(float(i.get(key)))
                    elif key == 'price_high':
                        one_day_high.append(float(i.get(key)))
                    elif key == 'price_low':
                        one_day_low.append(float(i.get(key)))
    f.close()

    # os.remove(f'{period}_period.json')
    if period == '5MIN':
        with open(f'{period}_close.json', 'w+') as f:
            f.write(str(five_min_close))
        with open(f'{period}_open.json', 'w+') as f:
            f.write(str(five_min_open))
        with open(f'{period}_high.json', 'w+') as f:
            f.write(str(five_min_high))
        with open(f'{period}_low.json', 'w+') as f:
            f.write(str(five_min_low))
        # Reverse close list to make earliest candle first
        # reversed_list = five_min_close[::-1]
        new_function(five_min_close, period)
    elif period == '15MIN':
        with open(f'{period}_close.json', 'w+') as f:
            f.write(str(fifteen_min_close))
        with open(f'{period}_open.json', 'w+') as f:
            f.write(str(fifteen_min_open))
        with open(f'{period}_high.json', 'w+') as f:
            f.write(str(fifteen_min_high))
        with open(f'{period}_low.json', 'w+') as f:
            f.write(str(fifteen_min_low))
        # Reverse close list to make earliest candle first
        # reversed_list = fifteen_min_close[::-1]
        new_function(fifteen_min_close, period)
    elif period == '1HRS':
        with open(f'{period}_close.json', 'w+') as f:
            f.write(str(one_hour_close))
        with open(f'{period}_open.json', 'w+') as f:
            f.write(str(one_hour_open))
        with open(f'{period}_high.json', 'w+') as f:
            f.write(str(one_hour_high))
        with open(f'{period}_low.json', 'w+') as f:
            f.write(str(one_hour_low))
        # Reverse close list to make earliest candle first
        # reversed_list = one_hour_close[::-1]
        new_function(one_hour_close, period)
    elif period == '4HRS':
        with open(f'{period}_close.json', 'w+') as f:
            f.write(str(four_hours_close))
        with open(f'{period}_open.json', 'w+') as f:
            f.write(str(four_hours_open))
        with open(f'{period}_high.json', 'w+') as f:
            f.write(str(four_hours_high))
        with open(f'{period}_low.json', 'w+') as f:
            f.write(str(four_hours_low))
        # Reverse close list to make earliest candle first
        # reversed_list = four_hours_close[::-1]
        new_function(four_hours_close, period)
    elif period == '1DAY':
        with open(f'{period}_close.json', 'w+') as f:
            f.write(str(one_day_close))
        with open(f'{period}_open.json', 'w+') as f:
            f.write(str(one_day_open))
        with open(f'{period}_high.json', 'w+') as f:
            f.write(str(one_day_high))
        with open(f'{period}_low.json', 'w+') as f:
            f.write(str(one_day_low))
        # Reverse close list to make earliest candle first
        # reversed_list = one_day_close[::-1]
        new_function(one_day_close, period)

    print("Get Keys Completed")
    print("-------------")


# API call for periods and symbols data abstracted
def period_api_request(symbol: str, period: str):

    url = f'https://rest.coinapi.io/v1/ohlcv/{symbol}/latest?period_id={period}'
    headers = {'X-CoinAPI-Key': f'{api_key}'}
    response = requests.get(url, headers=headers).json()

    # # Get last N elements from list
    # res = response
    create_json(symbol, period, response)
    get_keys(symbol, period)
    s_count, un_count, x_count = search_db(symbol, period)
    calculate(period, symbol, s_count, un_count, x_count)


def set_current_times(symbol: str, period: str):
    # global periods
    # sorted_start = ''
    # sorted_end = ''

    # Current Times
    global five_min_start_current
    global five_min_end_current
    global fifteen_min_start_current
    global fifteen_min_end_current
    global one_hour_start_current
    global one_hour_end_current
    global four_hour_start_current
    global four_hour_end_current
    global one_day_start_current
    global one_day_end_current
    global day_track_start
    global day_track_end
    global month_track_start
    global month_track_end
    global year_track_start
    global year_track_end

    f = open(f'{symbol}_{period}_data.json', 'r+')
    f_json_data = json.load(f)

    time_start = f_json_data[0]['time_period_start']
    sorted_start = time_start.split('T')[1].split('.')[0]

    time_end = f_json_data[0]['time_period_end']
    sorted_end = time_end.split('T')[1].split('.')[0]

    if(period == '5MIN'):
        five_min_start_current = sorted_start
        five_min_end_current = sorted_end
        print(
            f'{period} current times set to {five_min_start_current} and {five_min_end_current}')
    if(period == '15MIN'):
        fifteen_min_start_current = sorted_start
        fifteen_min_end_current = sorted_end
        print(
            f'{period} current times set to {fifteen_min_start_current} and {fifteen_min_end_current}')
    if(period == '1HRS'):
        one_hour_start_current = sorted_start
        one_hour_end_current = sorted_end
        print(
            f'{period} current times set to {one_hour_start_current} and {one_hour_end_current}')
    if(period == '4HRS'):
        four_hour_start_current = sorted_start
        four_hour_end_current = sorted_end
        print(
            f'{period} current times set to {four_hour_start_current} and {four_hour_end_current}')
    if(period == '1DAY'):
        sorted_day_start = time_start.split('T')[0].split('-')[-1]
        sorted_day_end = time_end.split('T')[0].split('-')[-1]
        sorted_month_start = time_start.split('T')[0].split('-')[1]
        sorted_month_end = time_end.split('T')[0].split('-')[1]
        sorted_year_start = time_start.split('T')[0].split('-')[0]
        sorted_year_end = time_end.split('T')[0].split('-')[0]
        day_track_start = sorted_day_start
        day_track_end = sorted_day_end
        one_day_start_current = sorted_start
        one_day_end_current = sorted_end
        month_track_start = sorted_month_start
        month_track_end = sorted_month_end
        year_track_start = sorted_year_start
        year_track_end = sorted_year_end
        print(
            f'{period} current times set to {one_day_start_current} and {one_day_end_current}')
        print(
            f'{period} day track dates set to {day_track_start} and {day_track_end}')
        print(
            f'{period} month track dates set to {month_track_start} and {month_track_end}')
        print(
            f'{period} year track dates set to {year_track_start} and {year_track_end}')


def update_current_times(period: str):
    global symbols
    global five_min_start_current
    global five_min_end_current
    global fifteen_min_start_current
    global fifteen_min_end_current
    global one_hour_start_current
    global one_hour_end_current
    global four_hour_start_current
    global four_hour_end_current
    global one_day_start_current
    global one_day_end_current
    global day_track_start
    global day_track_end
    global month_track_start
    global month_track_end
    global year_track_start
    global year_track_end
    leap_months = [4, 6, 9, 11]

    if(period == '5MIN'):
        five_min_start_current = crazy_calculations(
            period, five_min_start_current)
        five_min_end_current = crazy_calculations(
            period, five_min_end_current)
        print(
            f'{period} current times updated to {five_min_start_current} and {five_min_end_current}')
        # print(
        #     f'Others remain "15MIN": {fifteen_min_start_current, fifteen_min_end_current}, "1": {fifteen_min_start_current, fifteen_min_end_current}')
    if(period == '15MIN'):
        fifteen_min_start_current = crazy_calculations(
            period, fifteen_min_start_current)
        fifteen_min_end_current = crazy_calculations(
            period, fifteen_min_end_current)
        print(
            f'{period} current times updated to {fifteen_min_start_current} and {fifteen_min_end_current}')
    if(period == '1HRS'):
        one_hour_start_current = crazy_calculations(
            period, one_hour_start_current)
        one_hour_end_current = crazy_calculations(
            period, one_hour_end_current)
        print(
            f'{period} current times updated to {one_hour_start_current} and {one_hour_end_current}')
    if(period == '4HRS'):
        four_hour_start_current = crazy_calculations(
            period, four_hour_start_current)
        four_hour_end_current = crazy_calculations(
            period, four_hour_end_current)
        print(
            f'{period} current times updated to {four_hour_start_current} and {four_hour_end_current}')
    if(period == '1DAY'):
        pass
        one_day_start_current = crazy_calculations(
            period, one_day_start_current)
        one_day_end_current = crazy_calculations(
            period, one_day_end_current)

        # OTHERS GO HERE
        if (month_track_start in leap_months and day_track_start == 30):
            day_track_end = '01'
        day_track_start = days_months_years(day_track_start)
        day_track_end = days_months_years(day_track_end)

        # day_track_start = days_months_years(day_track_start, 'month')
        # day_track_end = days_months_years(day_track_end, 'month')

        # day_track_start = days_months_years(day_track_start, 'day')
        # day_track_end = days_months_years(day_track_end, 'day')
        print(
            f'{period} current times updated to {one_day_start_current} and {one_day_end_current}')
        print(
            f'{period} day track dates updated to {day_track_start} and {day_track_end}')
        print(
            f'{period} month track dates updated to {month_track_start} and {month_track_end}')
        print(
            f'{period} year track dates updated to {year_track_start} and {year_track_end}')


def confirm_period_delay():
    print('Confirm delay period here')
    global fifteen_minutes
    global one_hour
    global four_hours
    global one_day
    global counter
    global sleep_time
    global periods

    print('Counter is currently', counter)
    # try:
    # if counter <= 0:
    #     for symbol in symbols:
    #         for period in periods:
    #             # get_current_price(symbol)
    #             if period == '5MIN':
    #                 get_current_price(symbol)
    #                 period_api_request(symbol, period)

    #             if period == '15MIN' and datetime.now() >= fifteen_minutes:
    #                 period_api_request(symbol, period)

    #             if period == '1HRS' and datetime.now() >= one_hour:
    #                 period_api_request(symbol, period)

    #             if period == '4HRS' and datetime.now() >= four_hours:
    #                 period_api_request(symbol, period)

    #             if period == '1DAY' and datetime.now() >= one_day:
    #                 period_api_request(symbol, period)

    # elif counter > 0:

    #     further_runs()
    #     update_current_times()

    # counter = 1
    # print('Counter is currently', counter)
    # print('Sleeping...')
    # time.sleep(sleep_time)
    # print('Awake...')
    # confirm_period_delay()
    print('Sleeping...')
    time.sleep(sleep_time)
    further_runs()
    # update_current_times()
    confirm_period_delay()
    # except Exception:
    #     print('Confirm Period Delay Exception')
    #     time.sleep(3)
    #     confirm_period_delay()


# GET latest data for each given period
def get_periods() -> None:
    global counter
    print(f'Counter is currently {counter}')
    print('Get Periods here')
    # try:
    if counter <= 0:
        create_db()
        for symbol in symbols:
            for period in periods:
                get_current_price(symbol)
                period_api_request(symbol, period)
                set_current_times(symbol, period)

        counter = 1
        confirm_period_delay()
    else:
        confirm_period_delay()

    # except Exception:
    #     print('Get Periods Exception')
    #     time.sleep(3)
    #     confirm_period_delay()


def calculate(period: str, symbol: str, success_count: int, unsuccess_count: int, black_x_count: int) -> None:
    print('Calculate Here')

    global price
    global counter

    if counter <= 0:
        total_range = 20
        print(f'Total Range is currently, {total_range}')
    elif counter > 0:
        total_range = 1
        print(f'Total Range is currently, {total_range}')
    # global five_minutes_moving_average
    # global fifteen_minutes_moving_average
    # global one_hour_moving_average
    # global four_hour_moving_average
    # global one_day_moving_average

    # try:
    if period == '5MIN':

        print(f"Success now: {success_count}")
        print(f"Unsuccess now: {unsuccess_count}")
        print(f"BlackX now: {black_x_count}")

        global five_minutes_moving_average
        global five_min_open
        global five_min_high
        global five_min_low
        global five_min_close

        # Reverse OHL to match C
        # C has been adjusted in get_keys
        open_list = five_min_open[:total_range]

        high_list = five_min_high[:total_range]

        low_list = five_min_low[:total_range]

        close_list = five_min_close[:total_range]

        for i in range(1, total_range + 1):

            # If open < MA and high > MA
            res_cond1 = open_list[-i] < five_minutes_moving_average[-i] and high_list[-i] >= five_minutes_moving_average[-i]
            print(str(i) + ' resC1 ' + str(res_cond1))
            # If close < MA
            res_cond2 = close_list[-i] <= five_minutes_moving_average[-i]
            print(str(i) + ' resC2 ' + str(res_cond2))

            sup_cond1 = open_list[-i] > five_minutes_moving_average[-i] and low_list[-i] <= five_minutes_moving_average[-i]
            print(str(i) + ' supC1 ' + str(sup_cond1))
            sup_cond2 = close_list[-i] >= five_minutes_moving_average[-i]
            print(str(i) + ' supC2 ' + str(sup_cond2))

            if not res_cond1 and not sup_cond1:
                # Added
                if success_count > 0:
                    unsuccess_count += 1
                    print(f'unsuccess_count count: {unsuccess_count}')
                else:
                    unsuccess_count = 0
                    print(f'unsuccess_count reset: {unsuccess_count}')
                print(str(i) + ' unsuccess')
            else:
                # Is Resistance
                if res_cond1:
                    if res_cond2:
                        # Added
                        if unsuccess_count > 0:
                            unsuccess_count = 0
                            success_count += 1
                        else:
                            success_count += 1
                        print(f'success_count count: {success_count}')
                        print('RES SUCCESS')
                        print(str(i) + ' success Res1')
                        print(str(open_list[-i]) + ' open < ' + str(five_minutes_moving_average[-i]) + ' MA ' + str(
                            high_list[-i]) + ' high >= ' + str(five_minutes_moving_average[-i]) + ' MA ')
                        print(str(i) + ' success Res2')
                        print(str(close_list[-i]) + ' close <= ' +
                              str(five_minutes_moving_average[-i]) + ' MA')
                    else:
                        # If res_cond1 TRUE and res_cond2 FALSE
                        # Added
                        if success_count > 0:
                            black_x_count += 1
                            print(f'black_x_count count: {black_x_count}')
                        else:
                            black_x_count = 0
                        print('BlackXres ')
                        print(str(i) + ' success Res1')
                        print(str(open_list[-i]) + ' open < ' + str(five_minutes_moving_average[-i]) + ' MA ' + str(
                            high_list[-i]) + ' high >= ' + str(five_minutes_moving_average[-i]) + ' MA ')
                        print(str(i) + ' unsuccess Res2')
                        print(
                            str(close_list[-i]) + ' close > ' + str(five_minutes_moving_average[-i]) + ' MA')

                # Is Support
                if sup_cond1:
                    if sup_cond2:
                        # Added
                        if unsuccess_count > 0:
                            unsuccess_count = 0
                            success_count += 1
                        else:
                            success_count += 1
                        print(f'success_count count: {success_count}')
                        print('SUP SUCCESS')
                        print(str(i) + ' success Sup1')
                        print(str(open_list[-i]) + ' open > ' + str(five_minutes_moving_average[-i]) + ' MA ' + str(
                            low_list[-i]) + ' low <= ' + str(five_minutes_moving_average[-i]) + ' MA ')
                        print(str(i) + ' success Sup2')
                        print(str(close_list[-i]) + ' close >= ' +
                              str(five_minutes_moving_average[-i]) + ' MA')

                    else:
                        # If sup_cond1 TRUE and sup_cond2 FALSE
                        # Added
                        if success_count > 0:
                            black_x_count += 1
                            print(f'black_x_count count: {black_x_count}')
                        else:
                            black_x_count = 0
                            print(f'black_x_count count: {black_x_count}')
                        print('BlackXsup')
                        print(str(i) + ' success Sup1')
                        print(str(open_list[-i]) + ' open > ' + str(five_minutes_moving_average[-i]) + ' MA ' + str(
                            low_list[-i]) + ' low <= ' + str(five_minutes_moving_average[-i]) + ' MA ')
                        print(str(i) + ' unsuccess Res2')
                        print(
                            str(close_list[-i]) + ' close < ' + str(five_minutes_moving_average[-i]) + ' MA')
            print(
                f'Prelim calculations: \n Black X: {black_x_count} \n Success: {success_count} \n Unsuccess: {unsuccess_count}')
            print(f'success_count running count: {success_count}')
            print(f'unsuccess_count running count: {unsuccess_count}')
            print(f'black_x_count running count: {black_x_count}')
            print("-------------")

            try:
                final_sum = black_x_count / success_count
                print(f'Current blackX/success division is {final_sum}')
                if final_sum >= 0.5:
                    black_x_count = 0
                    success_count = 0
                    unsuccess_count = 0
                    print(
                        f'Final calculations: \n Black X: {black_x_count} \n Success: {success_count} \n Unsuccess: {unsuccess_count}')
                    print("-------------")
                if unsuccess_count == 20:
                    black_x_count = 0
                    success_count = 0
                    unsuccess_count = 0
                    print(
                        f'Force reset all parameters as unsuccess_count == {unsuccess_count}')
                    print("-------------")
            except ZeroDivisionError:
                print(f'Current blackX/success division got a zero division')
                black_x_count = 0
                success_count = 0
                unsuccess_count = 0
                print(
                    f'Final calculations: \n Black X: {black_x_count} \n Success: {success_count} \n Unsuccess: {unsuccess_count}')
                print("-------------")
        # Excel Automation Goes Here
        # s_count, x_count = search_db(symbol, period)
        update_db(symbol, period, success_count, unsuccess_count,
                  black_x_count, price, five_minutes_moving_average[0])
        # workbook(symbol, period, price,
        #          five_minutes_moving_average[0], success_count, unsuccess_count, black_x_count)

        five_minutes_moving_average = []
        five_min_open = []
        five_min_high = []
        five_min_low = []
        five_min_close = []

    if period == '15MIN':

        print(f"Success now: {success_count}")
        print(f"Unsuccess now: {unsuccess_count}")
        print(f"BlackX now: {black_x_count}")
        global fifteen_minutes_moving_average
        global fifteen_min_open
        global fifteen_min_high
        global fifteen_min_low
        global fifteen_min_close

        # Reverse OHL to match C
        # C has been adjusted in get_keys
        open_list = fifteen_min_open[:total_range]

        high_list = fifteen_min_high[:total_range]

        low_list = fifteen_min_low[:total_range]

        close_list = fifteen_min_close[:total_range]

        # print(f'Origin - This is successful: {successful} and this is unsuccessful: {unsuccessful}')

        for i in range(1, total_range + 1):

            # If open < MA and high > MA
            res_cond1 = open_list[-i] < fifteen_minutes_moving_average[-i] and high_list[-i] >= fifteen_minutes_moving_average[-i]
            print(str(i) + ' resC1 ' + str(res_cond1))
            # If close < MA
            res_cond2 = close_list[-i] <= fifteen_minutes_moving_average[-i]
            print(str(i) + ' resC2 ' + str(res_cond2))

            sup_cond1 = open_list[-i] > fifteen_minutes_moving_average[-i] and low_list[-i] <= fifteen_minutes_moving_average[-i]
            print(str(i) + ' supC1 ' + str(sup_cond1))
            sup_cond2 = close_list[-i] >= fifteen_minutes_moving_average[-i]
            print(str(i) + ' supC2 ' + str(sup_cond2))

            if not res_cond1 and not sup_cond1:
                # Added
                if success_count > 0:
                    unsuccess_count += 1
                    print(f'unsuccess_count count: {unsuccess_count}')
                else:
                    unsuccess_count = 0
                    print(f'unsuccess_count reset: {unsuccess_count}')
                print(str(i) + ' unsuccess')
            else:
                # Is Resistance
                if res_cond1:
                    if res_cond2:
                        # Added

                        if unsuccess_count > 0:
                            unsuccess_count = 0
                            success_count += 1
                        else:
                            success_count += 1
                        print(f'success_count count: {success_count}')
                        print('RES SUCCESS')
                        print(str(i) + ' success Res1')
                        print(str(open_list[-i]) + ' open < ' + str(fifteen_minutes_moving_average[-i]) + ' MA ' + str(
                            high_list[-i]) + ' high >= ' + str(fifteen_minutes_moving_average[-i]) + ' MA ')
                        print(str(i) + ' success Res2')
                        print(str(
                            close_list[-i]) + ' close <= ' + str(fifteen_minutes_moving_average[-i]) + ' MA')
                    else:
                        # If res_cond1 TRUE and res_cond2 FALSE
                        # Added
                        if success_count > 0:
                            black_x_count += 1
                            print(f'black_x_count count: {black_x_count}')
                        else:
                            black_x_count = 0
                        print('BlackXres ')
                        print(str(i) + ' success Res1')
                        print(str(open_list[-i]) + ' open < ' + str(fifteen_minutes_moving_average[-i]) + ' MA ' + str(
                            high_list[-i]) + ' high >= ' + str(fifteen_minutes_moving_average[-i]) + ' MA ')
                        print(str(i) + ' unsuccess Res2')
                        print(str(
                            close_list[-i]) + ' close > ' + str(fifteen_minutes_moving_average[-i]) + ' MA')

                # Is Support
                if sup_cond1:
                    if sup_cond2:
                        # Added
                        if unsuccess_count > 0:
                            unsuccess_count = 0
                            success_count += 1
                        else:
                            success_count += 1
                        print(f'success_count count: {success_count}')
                        print('SUP SUCCESS')
                        print(str(i) + ' success Sup1')
                        print(str(open_list[-i]) + ' open > ' + str(fifteen_minutes_moving_average[-i]) + ' MA ' + str(
                            low_list[-i]) + ' low <= ' + str(fifteen_minutes_moving_average[-i]) + ' MA ')
                        print(str(i) + ' success Sup2')
                        print(str(
                            close_list[-i]) + ' close >= ' + str(fifteen_minutes_moving_average[-i]) + ' MA')

                    else:
                        # If sup_cond1 TRUE and sup_cond2 FALSE
                        # Added
                        if success_count > 0:
                            black_x_count += 1
                            print(f'black_x_count count: {black_x_count}')
                        else:
                            black_x_count = 0
                            print(f'black_x_count count: {black_x_count}')
                        print('BlackXsup')
                        print(str(i) + ' success Sup1')
                        print(str(open_list[-i]) + ' open > ' + str(fifteen_minutes_moving_average[-i]) + ' MA ' + str(
                            low_list[-i]) + ' low <= ' + str(fifteen_minutes_moving_average[-i]) + ' MA ')
                        print(str(i) + ' unsuccess Res2')
                        print(str(
                            close_list[-i]) + ' close < ' + str(fifteen_minutes_moving_average[-i]) + ' MA')
            print(
                f'Prelim calculations: \n Black X: {black_x_count} \n Success: {success_count} \n Unsuccess: {unsuccess_count}')
            print(f'success_count running count: {success_count}')
            print(f'unsuccess_count running count: {unsuccess_count}')
            print(f'black_x_count running count: {black_x_count}')
            print("-------------")

            # print(f'Successful is {success_count} and Unsuccessful is {unsuccess_count}')

            try:
                final_sum = black_x_count / success_count
                print(f'Current blackX/success division is {final_sum}')
                if final_sum >= 0.5:
                    black_x_count = 0
                    success_count = 0
                    unsuccess_count = 0
                    print(
                        f'Final calculations: \n Black X: {black_x_count} \n Success: {success_count} \n Unsuccess: {unsuccess_count}')
                    print("-------------")
                if unsuccess_count == 20:
                    black_x_count = 0
                    success_count = 0
                    unsuccess_count = 0
                    print(
                        f'Force reset all parameters as unsuccess_count == {unsuccess_count}')
                    print("-------------")
            except ZeroDivisionError:
                print(f'Current blackX/success division got a zero division')
                black_x_count = 0
                success_count = 0
                unsuccess_count = 0
                print(
                    f'Final calculations: \n Black X: {black_x_count} \n Success: {success_count} \n Unsuccess: {unsuccess_count}')
                print("-------------")
        # Excel Automation Goes Here
        update_db(symbol, period, success_count, unsuccess_count,
                  black_x_count, price, fifteen_minutes_moving_average[0])
        # workbook(symbol, period, price,
        #          fifteen_minutes_moving_average[0], success_count, unsuccess_count, black_x_count)

        fifteen_minutes_moving_average = []
        fifteen_min_open = []
        fifteen_min_high = []
        fifteen_min_low = []
        fifteen_min_close = []

    if period == '1HRS':

        print(f"Success now: {success_count}")
        print(f"Unsuccess now: {unsuccess_count}")
        print(f"BlackX now: {black_x_count}")

        global one_hour_moving_average
        global one_hour_open
        global one_hour_high
        global one_hour_low
        global one_hour_close

        # Reverse OHL to match C
        # C has been adjusted in get_keys
        open_list = one_hour_open[:total_range]

        high_list = one_hour_high[:total_range]

        low_list = one_hour_low[:total_range]

        close_list = one_hour_close[:total_range]

        for i in range(1, total_range + 1):

            # If open < MA and high > MA
            res_cond1 = open_list[-i] < one_hour_moving_average[-i] and high_list[-i] >= one_hour_moving_average[-i]
            print(str(i) + ' resC1 ' + str(res_cond1))
            # If close < MA
            res_cond2 = close_list[-i] <= one_hour_moving_average[-i]
            print(str(i) + ' resC2 ' + str(res_cond2))

            sup_cond1 = open_list[-i] > one_hour_moving_average[-i] and low_list[-i] <= one_hour_moving_average[-i]
            print(str(i) + ' supC1 ' + str(sup_cond1))
            sup_cond2 = close_list[-i] >= one_hour_moving_average[-i]
            print(str(i) + ' supC2 ' + str(sup_cond2))

            if not res_cond1 and not sup_cond1:
                # Added
                if success_count > 0:
                    unsuccess_count += 1
                    print(f'unsuccess_count count: {unsuccess_count}')
                else:
                    unsuccess_count = 0
                    print(f'unsuccess_count reset: {unsuccess_count}')
                print(str(i) + ' unsuccess')
            else:
                # Is Resistance
                if res_cond1:
                    if res_cond2:
                        # Added

                        if unsuccess_count > 0:
                            unsuccess_count = 0
                            success_count += 1
                        else:
                            success_count += 1
                        print(f'success_count count: {success_count}')
                        print('RES SUCCESS')
                        print(str(i) + ' success Res1')
                        print(str(open_list[-i]) + ' open < ' + str(one_hour_moving_average[-i]) + ' MA ' + str(
                            high_list[-i]) + ' high >= ' + str(one_hour_moving_average[-i]) + ' MA ')
                        print(str(i) + ' success Res2')
                        print(
                            str(close_list[-i]) + ' close <= ' + str(one_hour_moving_average[-i]) + ' MA')
                    else:
                        # If res_cond1 TRUE and res_cond2 FALSE
                        # Added
                        if success_count > 0:
                            black_x_count += 1
                            print(f'black_x_count count: {black_x_count}')
                        else:
                            black_x_count = 0
                        print('BlackXres ')
                        print(str(i) + ' success Res1')
                        print(str(open_list[-i]) + ' open < ' + str(one_hour_moving_average[-i]) + ' MA ' + str(
                            high_list[-i]) + ' high >= ' + str(one_hour_moving_average[-i]) + ' MA ')
                        print(str(i) + ' unsuccess Res2')
                        print(
                            str(close_list[-i]) + ' close > ' + str(one_hour_moving_average[-i]) + ' MA')

                # Is Support
                if sup_cond1:
                    if sup_cond2:
                        # Added
                        if unsuccess_count > 0:
                            unsuccess_count = 0
                            success_count += 1
                        else:
                            success_count += 1
                        print(f'success_count count: {success_count}')
                        print('SUP SUCCESS')
                        print(str(i) + ' success Sup1')
                        print(str(open_list[-i]) + ' open > ' + str(one_hour_moving_average[-i]) + ' MA ' + str(
                            low_list[-i]) + ' low <= ' + str(one_hour_moving_average[-i]) + ' MA ')
                        print(str(i) + ' success Sup2')
                        print(
                            str(close_list[-i]) + ' close >= ' + str(one_hour_moving_average[-i]) + ' MA')

                    else:
                        # If sup_cond1 TRUE and sup_cond2 FALSE
                        # Added
                        if success_count > 0:
                            black_x_count += 1
                            print(f'black_x_count count: {black_x_count}')
                        else:
                            black_x_count = 0
                            print(f'black_x_count count: {black_x_count}')
                        print('BlackXsup')
                        print(str(i) + ' success Sup1')
                        print(str(open_list[-i]) + ' open > ' + str(one_hour_moving_average[-i]) + ' MA ' + str(
                            low_list[-i]) + ' low <= ' + str(one_hour_moving_average[-i]) + ' MA ')
                        print(str(i) + ' unsuccess Res2')
                        print(
                            str(close_list[-i]) + ' close < ' + str(one_hour_moving_average[-i]) + ' MA')
            print(
                f'Prelim calculations: \n Black X: {black_x_count} \n Success: {success_count} \n Unsuccess: {unsuccess_count}')
            print(f'success_count running count: {success_count}')
            print(f'unsuccess_count running count: {unsuccess_count}')
            print(f'black_x_count running count: {black_x_count}')
            print("-------------")

            try:
                final_sum = black_x_count / success_count
                print(f'Current blackX/success division is {final_sum}')
                if final_sum >= 0.5:
                    black_x_count = 0
                    success_count = 0
                    unsuccess_count = 0
                    print(
                        f'Final calculations: \n Black X: {black_x_count} \n Success: {success_count} \n Unsuccess: {unsuccess_count}')
                    print("-------------")
                if unsuccess_count == 20:
                    black_x_count = 0
                    success_count = 0
                    unsuccess_count = 0
                    print(
                        f'Force reset all parameters as unsuccess_count == {unsuccess_count}')
                    print("-------------")
            except ZeroDivisionError:
                print(f'Current blackX/success division got a zero division')
                black_x_count = 0
                success_count = 0
                unsuccess_count = 0
                print(
                    f'Final calculations: \n Black X: {black_x_count} \n Success: {success_count} \n Unsuccess: {unsuccess_count}')
                print("-------------")
        # Excel Automation Goes Here
        update_db(symbol, period, success_count, unsuccess_count,
                  black_x_count, price, one_hour_moving_average[0])
        # workbook(symbol, period, price,
        #          one_hour_moving_average[0], success_count, unsuccess_count, black_x_count)

        one_hour_moving_average = []
        one_hour_open = []
        one_hour_high = []
        one_hour_low = []
        one_hour_close = []

    if period == '4HRS':

        print(f"Success now: {success_count}")
        print(f"Unsuccess now: {unsuccess_count}")
        print(f"BlackX now: {black_x_count}")

        global four_hour_moving_average
        global four_hours_open
        global four_hours_high
        global four_hours_low
        global four_hours_close

        # Reverse OHL to match C
        # C has been adjusted in get_keys
        open_list = four_hours_open[:total_range]

        high_list = four_hours_high[:total_range]

        low_list = four_hours_low[:total_range]

        close_list = four_hours_close[:total_range]

        for i in range(1, total_range + 1):

            # If open < MA and high > MA
            res_cond1 = open_list[-i] < four_hour_moving_average[-i] and high_list[-i] >= four_hour_moving_average[-i]
            print(str(i) + ' resC1 ' + str(res_cond1))
            # If close < MA
            res_cond2 = close_list[-i] <= four_hour_moving_average[-i]
            print(str(i) + ' resC2 ' + str(res_cond2))

            sup_cond1 = open_list[-i] > four_hour_moving_average[-i] and low_list[-i] <= four_hour_moving_average[-i]
            print(str(i) + ' supC1 ' + str(sup_cond1))
            sup_cond2 = close_list[-i] >= four_hour_moving_average[-i]
            print(str(i) + ' supC2 ' + str(sup_cond2))

            if not res_cond1 and not sup_cond1:
                # Added
                if success_count > 0:
                    unsuccess_count += 1
                    print(f'unsuccess_count count: {unsuccess_count}')
                else:
                    unsuccess_count = 0
                    print(f'unsuccess_count reset: {unsuccess_count}')
                print(str(i) + ' unsuccess')
            else:
                # Is Resistance
                if res_cond1:
                    if res_cond2:
                        # Added

                        if unsuccess_count > 0:
                            unsuccess_count = 0
                            success_count += 1
                        else:
                            success_count += 1
                        print(f'success_count count: {success_count}')
                        print('RES SUCCESS')
                        print(str(i) + ' success Res1')
                        print(str(open_list[-i]) + ' open < ' + str(four_hour_moving_average[-i]) + ' MA ' + str(
                            high_list[-i]) + ' high >= ' + str(four_hour_moving_average[-i]) + ' MA ')
                        print(str(i) + ' success Res2')
                        print(
                            str(close_list[-i]) + ' close <= ' + str(four_hour_moving_average[-i]) + ' MA')
                    else:
                        # If res_cond1 TRUE and res_cond2 FALSE
                        # Added
                        if success_count > 0:
                            black_x_count += 1
                            print(f'black_x_count count: {black_x_count}')
                        else:
                            black_x_count = 0
                        print('BlackXres ')
                        print(str(i) + ' success Res1')
                        print(str(open_list[-i]) + ' open < ' + str(four_hour_moving_average[-i]) + ' MA ' + str(
                            high_list[-i]) + ' high >= ' + str(four_hour_moving_average[-i]) + ' MA ')
                        print(str(i) + ' unsuccess Res2')
                        print(
                            str(close_list[-i]) + ' close > ' + str(four_hour_moving_average[-i]) + ' MA')

                # Is Support
                if sup_cond1:
                    if sup_cond2:
                        # Added
                        if unsuccess_count > 0:
                            unsuccess_count = 0
                            success_count += 1
                        else:
                            success_count += 1
                        print(f'success_count count: {success_count}')
                        print('SUP SUCCESS')
                        print(str(i) + ' success Sup1')
                        print(str(open_list[-i]) + ' open > ' + str(four_hour_moving_average[-i]) + ' MA ' + str(
                            low_list[-i]) + ' low <= ' + str(four_hour_moving_average[-i]) + ' MA ')
                        print(str(i) + ' success Sup2')
                        print(
                            str(close_list[-i]) + ' close >= ' + str(four_hour_moving_average[-i]) + ' MA')

                    else:
                        # If sup_cond1 TRUE and sup_cond2 FALSE
                        # Added
                        if success_count > 0:
                            black_x_count += 1
                            print(f'black_x_count count: {black_x_count}')
                        else:
                            black_x_count = 0
                            print(f'black_x_count count: {black_x_count}')
                        print('BlackXsup')
                        print(str(i) + ' success Sup1')
                        print(str(open_list[-i]) + ' open > ' + str(four_hour_moving_average[-i]) + ' MA ' + str(
                            low_list[-i]) + ' low <= ' + str(four_hour_moving_average[-i]) + ' MA ')
                        print(str(i) + ' unsuccess Res2')
                        print(
                            str(close_list[-i]) + ' close < ' + str(four_hour_moving_average[-i]) + ' MA')
            print(
                f'Prelim calculations: \n Black X: {black_x_count} \n Success: {success_count} \n Unsuccess: {unsuccess_count}')
            print(f'success_count running count: {success_count}')
            print(f'unsuccess_count running count: {unsuccess_count}')
            print(f'black_x_count running count: {black_x_count}')
            print("-------------")

            # print(f'Successful is {success_count} and Unsuccessful is {unsuccess_count}')

            try:
                final_sum = black_x_count / success_count
                print(f'Current blackX/success division is {final_sum}')
                if final_sum >= 0.5:
                    black_x_count = 0
                    success_count = 0
                    unsuccess_count = 0
                    print(
                        f'Final calculations: \n Black X: {black_x_count} \n Success: {success_count} \n Unsuccess: {unsuccess_count}')
                    print("-------------")
                if unsuccess_count == 20:
                    black_x_count = 0
                    success_count = 0
                    unsuccess_count = 0
                    print(
                        f'Force reset all parameters as unsuccess_count == {unsuccess_count}')
                    print("-------------")
            except ZeroDivisionError:
                print(f'Current blackX/success division got a zero division')
                black_x_count = 0
                success_count = 0
                unsuccess_count = 0
                print(
                    f'Final calculations: \n Black X: {black_x_count} \n Success: {success_count} \n Unsuccess: {unsuccess_count}')
                print("-------------")
        # Excel Automation Goes Here
        update_db(symbol, period, success_count, unsuccess_count,
                  black_x_count, price, four_hour_moving_average[0])
        # workbook(symbol, period, price,
        #          four_hour_moving_average[0], success_count, unsuccess_count, black_x_count)

        four_hour_moving_average = []
        four_hours_open = []
        four_hours_high = []
        four_hours_low = []
        four_hours_close = []

    if period == '1DAY':
        print(f"Success now: {success_count}")
        print(f"Unsuccess now: {unsuccess_count}")
        print(f"BlackX now: {black_x_count}")

        global one_day_moving_average
        global one_day_open
        global one_day_high
        global one_day_low
        global one_day_close

        # Reverse OHL to match C
        # C has been adjusted in get_keys
        open_list = one_day_open[:total_range]

        high_list = one_day_high[:total_range]

        low_list = one_day_low[:total_range]

        close_list = one_day_close[:total_range]

        for i in range(1, total_range + 1):

            # If open < MA and high > MA
            res_cond1 = open_list[-i] < one_day_moving_average[-i] and high_list[-i] >= one_day_moving_average[-i]
            print(str(i) + ' resC1 ' + str(res_cond1))
            # If close < MA
            res_cond2 = close_list[-i] <= one_day_moving_average[-i]
            print(str(i) + ' resC2 ' + str(res_cond2))

            sup_cond1 = open_list[-i] > one_day_moving_average[-i] and low_list[-i] <= one_day_moving_average[-i]
            print(str(i) + ' supC1 ' + str(sup_cond1))
            sup_cond2 = close_list[-i] >= one_day_moving_average[-i]
            print(str(i) + ' supC2 ' + str(sup_cond2))

            if not res_cond1 and not sup_cond1:
                # Added
                if success_count > 0:
                    unsuccess_count += 1
                    print(f'unsuccess_count count: {unsuccess_count}')
                else:
                    unsuccess_count = 0
                    print(f'unsuccess_count reset: {unsuccess_count}')
                print(str(i) + ' unsuccess')
            else:
                # Is Resistance
                if res_cond1:
                    if res_cond2:
                        # Added

                        if unsuccess_count > 0:
                            unsuccess_count = 0
                            success_count += 1
                        else:
                            success_count += 1
                        print(f'success_count count: {success_count}')
                        print('RES SUCCESS')
                        print(str(i) + ' success Res1')
                        print(str(open_list[-i]) + ' open < ' + str(one_day_moving_average[-i]) + ' MA ' + str(
                            high_list[-i]) + ' high >= ' + str(one_day_moving_average[-i]) + ' MA ')
                        print(str(i) + ' success Res2')
                        print(
                            str(close_list[-i]) + ' close <= ' + str(one_day_moving_average[-i]) + ' MA')
                    else:
                        # If res_cond1 TRUE and res_cond2 FALSE
                        # Added
                        if success_count > 0:
                            black_x_count += 1
                            print(f'black_x_count count: {black_x_count}')
                        else:
                            black_x_count = 0
                        print('BlackXres ')
                        print(str(i) + ' success Res1')
                        print(str(open_list[-i]) + ' open < ' + str(one_day_moving_average[-i]) + ' MA ' + str(
                            high_list[-i]) + ' high >= ' + str(one_day_moving_average[-i]) + ' MA ')
                        print(str(i) + ' unsuccess Res2')
                        print(
                            str(close_list[-i]) + ' close > ' + str(one_day_moving_average[-i]) + ' MA')

                # Is Support
                if sup_cond1:
                    if sup_cond2:
                        # Added
                        if unsuccess_count > 0:
                            unsuccess_count = 0
                            success_count += 1
                        else:
                            success_count += 1
                        print(f'success_count count: {success_count}')
                        print('SUP SUCCESS')
                        print(str(i) + ' success Sup1')
                        print(str(open_list[-i]) + ' open > ' + str(one_day_moving_average[-i]) + ' MA ' + str(
                            low_list[-i]) + ' low <= ' + str(one_day_moving_average[-i]) + ' MA ')
                        print(str(i) + ' success Sup2')
                        print(
                            str(close_list[-i]) + ' close >= ' + str(one_day_moving_average[-i]) + ' MA')

                    else:
                        # If sup_cond1 TRUE and sup_cond2 FALSE
                        # Added
                        if success_count > 0:
                            black_x_count += 1
                            print(f'black_x_count count: {black_x_count}')
                        else:
                            black_x_count = 0
                            print(f'black_x_count count: {black_x_count}')
                        print('BlackXsup')
                        print(str(i) + ' success Sup1')
                        print(str(open_list[-i]) + ' open > ' + str(one_day_moving_average[-i]) + ' MA ' + str(
                            low_list[-i]) + ' low <= ' + str(one_day_moving_average[-i]) + ' MA ')
                        print(str(i) + ' unsuccess Res2')
                        print(
                            str(close_list[-i]) + ' close < ' + str(one_day_moving_average[-i]) + ' MA')
            print(
                f'Prelim calculations: \n Black X: {black_x_count} \n Success: {success_count} \n Unsuccess: {unsuccess_count}')
            print(f'success_count running count: {success_count}')
            print(f'unsuccess_count running count: {unsuccess_count}')
            print(f'black_x_count running count: {black_x_count}')
            print("-------------")

            # print(f'Successful is {success_count} and Unsuccessful is {unsuccess_count}')

            try:
                final_sum = black_x_count / success_count
                print(f'Current blackX/success division is {final_sum}')
                if final_sum >= 0.5:
                    black_x_count = 0
                    success_count = 0
                    unsuccess_count = 0
                    print(
                        f'Final calculations: \n Black X: {black_x_count} \n Success: {success_count} \n Unsuccess: {unsuccess_count}')
                    print("-------------")
                if unsuccess_count == 20:
                    black_x_count = 0
                    success_count = 0
                    unsuccess_count = 0
                    print(
                        f'Force reset all parameters as unsuccess_count == {unsuccess_count}')
                    print("-------------")
            except ZeroDivisionError:
                print(f'Current blackX/success division got a zero division')
                black_x_count = 0
                success_count = 0
                unsuccess_count = 0
                print(
                    f'Final calculations: \n Black X: {black_x_count} \n Success: {success_count} \n Unsuccess: {unsuccess_count}')
                print("-------------")
        # Excel Automation Goes Here
        update_db(symbol, period, success_count, unsuccess_count,
                  black_x_count, price, one_day_moving_average[0])
        # workbook(symbol, period, price,
        #          one_day_moving_average[0], success_count, unsuccess_count, black_x_count)

        one_day_moving_average = []
        one_day_open = []
        one_day_high = []
        one_day_low = []
        one_day_close = []

    # except Exception:
    #     print('Calculate Exception')
    #     time.sleep(3)
    #     confirm_period_delay()


if __name__ == '__main__':
    get_periods()
    # update_current_times()
    # print(symbols[0])
    # edit_json('BINANCE_SPOT_ETH_USDT', '5MIN')
