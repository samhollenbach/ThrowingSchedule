import csv
import datetime
import requests
import difflib

def closest_date(dates, today):
    closest = dates[0]
    for d in dates:
        days_delta = (today - d).days
        if days_delta < 0:
            continue
        elif days_delta < (today - closest).days:
            closest = d
    return (closest, (today-closest).days)

def get_pitching_day(data):
    dates = []
    weeks = []
    for l in data:
        date = l[0]
        date_split = date.split("/")
        if len(date_split) is 3:
            date_split = [int(d) for d in date_split]
            date = datetime.date(date_split[2],date_split[0],date_split[1])
            dates.append(date)
            weeks.append([date] + l[1:8])
    today = datetime.date.today()
    sunday_day, days_sep = closest_date(dates,today)
    week_index = [w[0] for w in weeks].index(sunday_day)
    current_week = weeks[week_index]
    return current_week[days_sep+1]

def get_day_info(day, info_file="ThrowingInfo.csv"):
    data = csv.reader(open(info_file,'r'),delimiter=',')
    data = [d for d in data]
    data_fit = []

    data_col1 = []
    data_col2 = []

    for line in data:
        line = line[0:4]
        if line[0] is '':
            if len(data_col1) > 0:
                data_fit.append(data_col1)
                data_col1 = []
        else:
            data_col1.append(line)
    if len(data_col1) > 0:
        data_fit.append(data_col1)

    for line2 in data:
        line2 = line2[4:8]
        if line2[0] is '':
            if len(data_col2) > 0:
                data_fit.append(data_col2)
                data_col2 = []
        else:
            data_col2.append(line2)
    if len(data_col2) > 0:
            data_fit.append(data_col2)

    names = [d[0][0] for d in data_fit]
    matches = difflib.get_close_matches(day, names, 1)
    if len(matches) == 0:
        return None
    for d in data_fit:
        if d[0][0] == matches[0]:
            return d


def push_day(pitching_day, with_info):
    day_info = get_day_info(pitching_day)
    info_string = "{}".format(pitching_day)
    if with_info:
        info_string += "\\n\\n"
        for info in day_info[1:]:
            info = list(filter(lambda a: a != '', info))
            for i,e in enumerate(info):
                if e != '':
                    info_string += "{}".format(e)
                    if i is not len(info)-1:
                        info_string += ", "
            info_string += "\\n"
    headers = {'Content-Type': 'application/json',}
    data = '{{"type": "note", "title": "Throwing Day {}", "body": "{}"}}'.format(datetime.date.today().strftime("%m/%d/%y"), info_string)
    requests.post('https://api.pushbullet.com/v2/pushes', headers=headers, data=data, auth=('o.V8x8MqKcPdMqkuot9W3COnIwg5JqPciX', ''))


include_info = True
schedule_file = "ThrowingSchedule.csv"

with open(schedule_file, 'r') as r:
    data = csv.reader(r,delimiter=',')
    pitching_day = get_pitching_day(data)
    push_day(pitching_day, include_info)

