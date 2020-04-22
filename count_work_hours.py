"""
Count how long the screenshots were running for (ie. how long i worked)
get the timedelta between the last file and the first for each dir

"""
from datetime import datetime, timedelta
import os
import operator
from functools import reduce

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


def get_one_day_duration(day:list)->timedelta:
    """"""
    all_screenshots_times = get_all_screenshots_times(day)

    one_day_start = all_screenshots_times[0]
    one_day_end = all_screenshots_times[-1]
    one_day_pauses = get_sum_pauses(all_screenshots_times)

    one_day_duration = one_day_end - one_day_start - one_day_pauses

    return one_day_duration


total_work_times = []
for day in all_days:
    day_dir = sorted(os.listdir(f"{screenshots_dir}/{day}"))
    if day_dir != []:
        dur = get_one_day_duration(day_dir)
        if dur < timedelta(hours=1) or day.startswith('Apéro'):
            continue
        else:
            print(day, dur, sep=' : ')
            total_work_times.append(dur)


total_time = reduce(operator.add, total_work_times)
total_time_in_hours = round(total_time.total_seconds()/60/60)

print(total_time_in_hours, "hours worked this month")