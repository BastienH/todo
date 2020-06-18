"""
Count how long the screenshots were running for (ie. how long i worked)
get the timedelta between the last file and the first for each dir

"""
from datetime import datetime, timedelta
import os, sys
import operator
from functools import reduce

try:
    dates = sys.argv[1:]
except IndexError:
    dates = [datetime.strftime(datetime.today(),  '%m')]
print(dates)
    
screenshots_dir = r'.\screenshots'

all_days = sorted(os.listdir(screenshots_dir))


def get_all_screenshots_times(day:list):
    """"""
    all_screenshots_times = []
    for screenshot in day:
        time_ = screenshot.split('_')[-1].replace('.png', '')
        time_ = datetime.strptime(time_, '%H-%M-%S')
        all_screenshots_times.append(time_)
    all_screenshots_times = sorted(all_screenshots_times)

    return all_screenshots_times


def get_sum_pauses(day:list, pause_time=None)->timedelta:
    """"""
    if pause_time is None:
        time_between_shots = timedelta(minutes=1)
    pauses = []
    for index, screenshot in enumerate(day):
        if index == len(day) - 1:
            break
        if day[index + 1] - day[index] > time_between_shots:
            pause_time = day[index + 1] - day[index]
            pauses.append(pause_time)
        else:
            continue
    if pauses == []:
        return timedelta(seconds=0)
    else:
        pauses_sum = reduce(operator.add, pauses)

    return pauses_sum


def calc_one_day_duration(day_dir: str)->timedelta:
    """"""
    days_images = sorted(os.listdir(day_dir))
    if days_images == []:
        one_day_duration=timedelta(0)
    else: 
        all_screenshots_times = get_all_screenshots_times(days_images)
        one_day_start = all_screenshots_times[0]
        one_day_end = all_screenshots_times[-1]
        one_day_pauses = get_sum_pauses(all_screenshots_times)

        one_day_duration = one_day_end - one_day_start - one_day_pauses

    return one_day_duration

def all_days_for_month(all_days:list, month:str)->list:
    """"""
    new_days_list = []
    for day in all_days:
        try:
            if day.split('-')[1] == month:
                new_days_list.append(day)
        except:
            pass
    return new_days_list

total_work_times = []

for month in dates:
    all_days = all_days_for_month(all_days, month)
    for day in all_days:
        day_dir = f"{screenshots_dir}/{day}"
        day_duration = calc_one_day_duration(day_dir)
        if day_duration < timedelta(hours=1) or not day[:1].startswith('2'):
            continue
        else:
            print(day, day_duration, sep=' : ')
            total_work_times.append(day_duration)
    print(month, total_work_times)

def determine_holidays():
    pass

total_time = reduce(operator.add, total_work_times)
total_time_in_hours = round(total_time.total_seconds()/60/60)

print("Average :", reduce(operator.add, total_work_times)/len(total_work_times))
print(total_time_in_hours, "hours worked this month")
