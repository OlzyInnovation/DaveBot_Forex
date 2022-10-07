import json


def search_data(symbol: str, period: str, current_start_time: str, current_end_time: str):
    f = open(f'socket_{symbol}_{period}.json', 'r+')
    f_json_data = json.load(f)
    # sorted_open = time_open.split('T')[1].split('.')[0]
    # # time_close = data['time_close']
    # # f.close()
    counter = 0
    for data in f_json_data:

        # time_open = data['time_open']
        time_open = data['time_open']
        time_period_start = data['time_period_start']
        sorted_period_start = time_period_start.split('T')[1].split('.')[0]
        time_period_end = data['time_period_end']
        sorted_period_end = time_period_end.split('T')[1].split('.')[0]
        # print('Time Open:  {}'.format(time_open))
        # print('Sorted Open:  {}'.format(sorted_open))
        # if (sorted_open == '06:15:00'):
        if (sorted_period_start == current_start_time and sorted_period_end == current_end_time):
            print('Counter is {}'.format(counter))
            # print(f_json_data[counter])
            return f_json_data[counter]

        counter += 1


def check_zeros(number_to_check: int) -> str:
    stringified = str(number_to_check)
    try:
        if stringified[0] and stringified[1]:
            return stringified
    except IndexError:
        return '0' + stringified


def crazy_calculations(period: str, value: str):
    print('Calculations for update Here...')
    print(f'Period gotten {period}')
    print(f'Value gotten {value}')

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
    elif(period == '1DAY'):
        if (hour_split == 23):
            hour_split = 0
        else:
            hour_split += 1

    join_splits = check_zeros(hour_split) + \
        ':' + check_zeros(minute_split) + ':' + second_split
    # call update_current_time function here instead
    print('Join SPlits: ', join_splits)
    return join_splits


def days_months_years(value: str | int):
    print('Calculations for days months years Here...')
    print(f'Value gotten {value}')
    value_check = int(value)
    value_check += 1

    return_value = check_zeros(value_check)
    return return_value


if __name__ == '__main__':
    chk = days_months_years('1')
    print(chk)
