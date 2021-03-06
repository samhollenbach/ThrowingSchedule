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



def get_pitching_days_from_date(pitching_date, data):
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

    return get_pitching_day(weeks, dates, pitching_date), get_pitching_day(weeks, dates, pitching_date+datetime.timedelta(days=1))

def get_pitching_day(weeks, dates, pitching_date):
    sunday_day, days_sep = closest_date(dates,pitching_date)
    week_index = [w[0] for w in weeks].index(sunday_day)
    current_week = weeks[week_index]
    return current_week[days_sep+1]


def get_day_info(day, info_file="ThrowingInfo.csv"):
    data = csv.reader(open(files_path+info_file,'r'),delimiter=',')
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


def push_day(pitching_day, token, info_type, next_day):
    day_info = get_day_info(pitching_day)

    title = "Throwing Day, {}".format(datetime.date.today().strftime("%A %m/%d/%y"))
    info_string = ""
    title += ": {}".format(pitching_day)
    if info_type is not 0:
        collect = True
        info_string += "\\n"
        if day_info is None:
            info_string += "No info available"
        else:
            info_string += "*{}*\\n".format(day_info[1][0])
            for info in day_info[2:]:
                if not info or info[0] == "Exercise":
                    continue
                info = list(filter(lambda a: a != '', info))
                if len(info) is 1:
                    if info_type is 1 and info[0] != "Throwing":
                        collect = False
                    else:
                        collect = True
                        info_string += "--{}--\\n".format(info[0])
                    continue
                for i,e in enumerate(info):
                    if e != '' and collect:
                        if i is 0:
                            info_string += "\u2022 {}".format(e)
                        elif i is 2:
                            info_string += "x {}".format(e)

                        else:
                            info_string += ", {}".format(e)
                if collect:
                    info_string += "\\n"

    if next_day != "":
        info_string += "\\n*Tomorrow: {}*".format(next_day)

    headers = {'Content-Type': 'application/json',}
    data = '{{"type": "note", "title": "{}", "body": "{}"}}'.format(title,info_string)
    requests.post('https://api.pushbullet.com/v2/pushes', headers=headers, data=data.encode('utf-8'), auth=(token, ''))

def push_to(file_path,name,token,with_info):
    schedule_file = "{}Schedules/{} - Throwing Schedule.csv".format(file_path,name)
    with open(schedule_file, 'r') as r:
        data = csv.reader(r,delimiter=',')
        pitching_day, next_day = get_pitching_days_from_date(datetime.date.today(),data)
        push_day(pitching_day, token, with_info, next_day)



files_path = "/home/ec2-user/ThrowingSchedule/"
#files_path = ""
config_file = "PushConfig.csv"


with open(files_path+config_file, 'r') as r:
    data = csv.reader(r,delimiter=',')

    header = next(data)
    for d in data:
        if d[1] == '':
            print("No auth token found")
            continue
        push_to(files_path,d[0],d[1],int(d[2]))




