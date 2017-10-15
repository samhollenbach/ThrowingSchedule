import csv
import datetime
import requests

def closest_date(dates, today):
    closest = dates[0]
    for d in dates:
        days_delta = (today - d).days
        if days_delta < 0:
            continue
        elif days_delta < (today - closest).days:
            closest = d
    return (closest, (today-closest).days)

with open("/home/ec2-user/ThrowingSchedule/ThrowingSchedule.csv", "r") as r:
    reader = csv.reader(r,delimiter=',')
    dates = []
    weeks = []
    for l in reader:
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
    current_day = current_week[days_sep+1]
    headers = {
        'Content-Type': 'application/json',
    }

    data = '{{"type": "note", "title": "Throwing Day {}", "body": "{}"}}'.format(today.strftime("%m/%d/%y"), current_day)


    requests.post('https://api.pushbullet.com/v2/pushes', headers=headers, data=data, auth=('o.V8x8MqKcPdMqkuot9W3COnIwg5JqPciX', ''))