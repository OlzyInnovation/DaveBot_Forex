from tkinter import N
import requests
import json
import time
from datetime import datetime, timedelta
import pymongo
from pymongo import MongoClient

# Enter preferred symbols/ticker below
symbols: list[str] = ['BINANCE_SPOT_ETH_USDT']
#symbols: list[str] = ['BINANCE_SPOT_MATIC_USDT','BINANCE_SPOT_LUNA_USDT', 'BINANCE_SPOT_ETH_USDT', 'BINANCE_SPOT_ADA_USDT', 'BINANCE_SPOT_SOL_USDT', 'BINANCE_SPOT_CRV_USDT','BINANCE_SPOT_BTC_USDT' ]

# Sample periods
# periods: list[str] = ['5MIN', '15MIN', '1HRS', '4HRS', '1DAY']
periods: list[str] = ['5MIN', '15MIN']

# Calculate time for period time lapse
t = time.localtime()
start_time = time.strftime("%H:%M:%S", t)
print(f'Data fetch starting at: {start_time}')

now = datetime.now()

print(f'now {now}')

five_minutes = now + timedelta(minutes=5)
fifteen_minutes = now + timedelta(minutes=10)
one_hour = now + timedelta(hours=1)
four_hours = now + timedelta(hours=4)
one_day = now + timedelta(hours=24)

# Moving Averages
five_minutes_moving_average: list = []
fifteen_minutes_moving_average: list = []
one_hour_moving_average: list = []
four_hour_moving_average: list = []
one_day_moving_average: list = []

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

# Resistance running counts
black_x_resistance_running_count_five_min: int = 0
black_x_resistance_running_count_fifteen_min: int = 0
black_x_resistance_running_count_one_hr: int = 0
black_x_resistance_running_count_four_hrs: int = 0
black_x_resistance_running_count_one_day: int = 0

# Support running counts
black_x_support_running_count_five_min: int = 0
black_x_support_running_count_fifteen_min: int = 0
black_x_support_running_count_one_hr: int = 0
black_x_support_running_count_four_hrs: int = 0
black_x_support_running_count_one_day: int = 0

# Success
success_five_min = 0
success_fifteen_min: list[int] = []
success_one_hr: list[int] = []
success_four_hrs: list[int] = []
success_one_day: list[int] = []

# Unuccess
unsuccess_five_min = 0
unsuccess_fifteen_min: list[int] = []
unsuccess_one_hr: list[int] = []
unsuccess_four_hrs: list[int] = []
unsuccess_one_day: list[int] = []

black_x_five_min = 0
black_x_fifteen_minutes: list[int] = []
black_x_one_hour: list[int] = []
black_x_four_hours: list[int] = []
black_x_one_day: list[int] = []


def get_current_price(symbol: str) -> float:
    try:
        url = f'https://rest.coinapi.io/v1/symbols?filter_symbol_id={symbol}'
        headers = {'X-CoinAPI-Key': '123655DD-2A99-4772-84F4-C7692BB7682B'}
        response = requests.get(url, headers=headers).json()
        current_price = float(response[0]['price'])
        print(f'{symbol} Current Price is: {current_price}')
        return current_price
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
        


def new_function(param: list, period: str):
    global five_minutes_moving_average
    global fifteen_minutes_moving_average
    global one_hour_moving_average
    global four_hour_moving_average
    global one_day_moving_average

    counter = 0
    if period == '5MIN':
        for i in range(0, len(five_min_close)):
            if counter == 20:
                continue
            else:
                total = 0
                split_list = five_min_close[counter:counter + 20]
                for i in range(0, len(split_list)):
                    total += float(split_list[i])
                counter += 1
                calculate_ma(total, period)
    if period == '15MIN':
        for i in range(0, len(fifteen_min_close)):
            if counter == 20:
                continue
            else:
                total = 0
                split_list = fifteen_min_close[counter:counter + 20]
                for i in range(0, len(split_list)):
                    total += float(split_list[i])
                counter += 1
                calculate_ma(total, period)
                

        # with open('list_confirmation.json', 'w+') as f:
        #     f.write(str(five_minutes_moving_average))


def create_json(period: str, param: list):
    # with open(f'{period}_period.json', 'w+') as f:
    with open(f'{period}_period.json', 'w+') as f:
        f.write(str(param))


    #read input file
    final = open(f'{period}_period.json', "r")
    #read file contents to string
    data = final.read()
    #replace all occurrences of the single quote
    data = data.replace('\'', '"')
    #close the input file
    final.close()
    #open the input file in write mode
    final = open(f'{period}_period.json', "w")
    #overrite the input file with the resulting data
    final.write(data)
    #close the file
    final.close()


def get_keys(period: str):
    global five_minutes_moving_average
    global fifteen_minutes_moving_average
    global one_hour_moving_average
    global four_hour_moving_average
    global one_day_moving_average


    with open(f'{period}_period.json', 'r+') as f:
        json_data = json.load(f)
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
                    
    if period == '5MIN':
        with open(f'{period}_close.json', 'w+') as f:
            f.write(str(five_min_close))
        with open(f'{period}_open.json', 'w+') as f:
            f.write(str(five_min_open))
        with open(f'{period}_high.json', 'w+') as f:
            f.write(str(five_min_high))
        with open(f'{period}_low.json', 'w+') as f:
            f.write(str(five_min_low))
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
        new_function(fifteen_min_close, period)
    elif period == '1HRS':
        new_function(one_hour_close, period)
    elif period == '4HRS':
        new_function(four_hours_close, period)
    elif period == '1DAY':
        new_function(one_day_close, period)
    


    print("Get Keys Completed")
    print("-------------")


# API call for periods and symbols data abstracted
def period_api_request(symbol: str, period: str):

    url = f'https://rest.coinapi.io/v1/ohlcv/{symbol}/latest?period_id={period}'
    headers = {'X-CoinAPI-Key': '123655DD-2A99-4772-84F4-C7692BB7682B'}
    response = requests.get(url, headers=headers).json()

    # # Get last N elements from list
    # res = response
    create_json(period, response)
    get_keys(period)
    calculate(period, symbol)


def confirm_period_delay():
    print('Confirm delay period here')
    try:
        sleep_time = 300
        # Five Minute Sleep Time
        time.sleep(sleep_time)
        for symbol in symbols:
            get_current_price(symbol)
            for period in periods:
                if period == '5MIN' and (str(five_minutes - now) <= str(now)):
                    get_keys(period)
                    calculate(period, symbol)
                
                # if period == '15MIN' and (str(fifteen_minutes - now) <= str(now)):
                #     # # if now >= fifteen_minutes and period == '15MIN':
                #     period_api_request(symbol, period)
                
                # if period == '1HRS' and (str(one_hour - now) <= str(now)):
                #     period_api_request(symbol, period)
                
                # if period == '4HRS' and (str(four_hours - now) <= str(now)):
                #     period_api_request(symbol, period)
               
                # if period == '1DAY' and (str(one_day - now) <= str(now)):
                #     period_api_request(symbol, period)
                
        confirm_period_delay()
    except Exception:
        print('Confirm Period Delay Exception')
        time.sleep(3)
        confirm_period_delay()


# GET latest data for each given period
def get_periods() -> None:
    print('Get Periods here')
    try:
        for symbol in symbols:
            get_current_price(symbol)
            for period in periods:
                period_api_request(symbol, period)

        # confirm_period_delay()

    except Exception:
        print('Get Periods Exception')
        time.sleep(3)
        confirm_period_delay()


def calculate(period: str, symbol: str) -> None:
    print('Calculate Here')
    total_range = 20

    global black_x_resistance_running_count_five_min
    global black_x_resistance_running_count_fifteen_min
    global black_x_resistance_running_count_one_hr
    global black_x_resistance_running_count_four_hrs
    global black_x_resistance_running_count_one_day
    global black_x_support_running_count_five_min

    global success_five_min
    global success_fifteen_min
    global success_one_hr
    global success_four_hrs
    global success_one_day

    global unsuccess_five_min
    global unsuccess_fifteen_min
    global unsuccess_one_hr
    global unsuccess_four_hrs
    global unsuccess_one_day

    global black_x_five_min
    global black_x_fifteen_minutes
    global black_x_one_hour
    global black_x_four_hours
    global black_x_one_day

    
    try:
        if period == '5MIN':
            global five_minutes_moving_average
            open_list = five_min_open[:total_range]
            high_list = five_min_high[:total_range]
            low_list = five_min_low[:total_range]
            close_list = five_min_close[:total_range]
          
            # print(f'Origin - This is successful: {successful} and this is unsuccessful: {unsuccessful}')

            for i in range(0, total_range):

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
                    if success_five_min > 0:
                        unsuccess_five_min += 1
                        print(f'unsuccess_five_min count: {unsuccess_five_min}')
                    else:
                        unsuccess_five_min = 0
                        print(f'unsuccess_five_min reset: {unsuccess_five_min}')
                    print(str(i) + ' unsuccess')
                else:
                    # Is Resistance
                    if res_cond1:
                        if res_cond2:
                            # Added

                            success_five_min += 1
                            print(f'success_five_min count: {success_five_min}')
                            print('RES SUCCESS')
                            print(str(i) + ' success Res1')
                            print(str(open_list[-i]) + ' open < ' + str(five_minutes_moving_average[-i]) + ' MA ' + str(high_list[-i]) + ' high >= ' + str(five_minutes_moving_average[-i]) + ' MA ')
                            print(str(i) + ' success Res2')
                            print(str(close_list[-i]) + ' close <= ' + str(five_minutes_moving_average[-i]) + ' MA')
                        else:
                            # If res_cond1 TRUE and res_cond2 FALSE
                            # Added
                            if success_five_min > 0:
                                black_x_five_min += 1
                                print(f'black_x_five_min count: {black_x_five_min}')
                            else:
                                black_x_five_min = 0
                            print('BlackXres ')
                            print(str(i) + ' success Res1')
                            print(str(open_list[-i]) + ' open < ' + str(five_minutes_moving_average[-i]) + ' MA ' + str(high_list[-i]) + ' high >= ' + str(five_minutes_moving_average[-i]) + ' MA ')
                            print(str(i) + ' unsuccess Res2')
                            print(str(close_list[-i]) + ' close > ' + str(five_minutes_moving_average[-i]) + ' MA')
	            
                    # Is Support
                    if sup_cond1:
                        if sup_cond2:
                            # Added
                            success_five_min += 1
                            print(f'success_five_min count: {success_five_min}')
                            print('SUP SUCCESS')
                            print(str(i) + ' success Sup1')
                            print(str(open_list[-i]) + ' open > ' + str(five_minutes_moving_average[-i]) + ' MA ' + str(low_list[-i]) + ' low <= ' + str(five_minutes_moving_average[-i]) + ' MA ')
                            print(str(i) + ' success Sup2')
                            print(str(close_list[-i]) + ' close >= ' + str(five_minutes_moving_average[-i]) + ' MA')

                        else:
                            # If sup_cond1 TRUE and sup_cond2 FALSE
                            # Added
                            if success_five_min > 0:
                                black_x_five_min += 1
                                print(f'black_x_five_min count: {black_x_five_min}')
                            else:
                                black_x_five_min = 0
                                print(f'black_x_five_min count: {black_x_five_min}')
                            print('BlackXsup')
                            print(str(i) + ' success Sup1')
                            print(str(open_list[-i]) + ' open > ' + str(five_minutes_moving_average[-i]) + ' MA ' + str(low_list[-i]) + ' low <= ' + str(five_minutes_moving_average[-i]) + ' MA ')
                            print(str(i) + ' unsuccess Res2')
                            print(str(close_list[-i]) + ' close < ' + str(five_minutes_moving_average[-i]) + ' MA')
                print(f'Prelim calculations: \n Black X: {black_x_five_min} \n Success: {success_five_min} \n Unsuccess: {unsuccess_five_min}')
                print(f'success_five_min running count: {success_five_min}')
                print(f'unsuccess_five_min running count: {unsuccess_five_min}')
                print(f'black_x_five_min running count: {black_x_five_min}')
                print("-------------")

                # print(f'Successful is {success_five_min} and Unsuccessful is {unsuccess_five_min}')

                try:
                    final_sum = black_x_five_min / success_five_min
                    print(f'Current blackX/success division is {final_sum}')
                    if final_sum >= 0.5:
                        black_x_five_min = 0
                        success_five_min = 0
                        unsuccess_five_min = 0
                        print(f'Final calculations: \n Black X: {black_x_five_min} \n Success: {success_five_min} \n Unsuccess: {unsuccess_five_min}')
                        print("-------------")
                    if unsuccess_five_min == 20:
                        black_x_five_min = 0
                        success_five_min = 0
                        unsuccess_five_min = 0
                        print(f'Force reset all parameters as unsuccess_five_min == {unsuccess_five_min}')
                        print("-------------")
                except ZeroDivisionError:
                        print(f'Current blackX/success division got a zero division')
                        black_x_five_min = 0
                        success_five_min = 0
                        unsuccess_five_min = 0
                        print(f'Final calculations: \n Black X: {black_x_five_min} \n Success: {success_five_min} \n Unsuccess: {unsuccess_five_min}')
                        print("-------------")
    except Exception:
        print('Calculate Exception')
        time.sleep(3)
        confirm_period_delay()


if __name__ == '__main__':
    get_periods()
