import matplotlib.pyplot as plt
import json
from pprint import pprint
from dateutil import parser
import datetime as dt
import matplotlib.dates as mdates

userNames = ['zeev_grim', 'grim_valerie'];

with open('data.json') as f:
    data = json.load(f)

for user in userNames:
    x, y = [], []

    for i in data[user]:
        y.append(int(i['followers']))
        d = ''
        dateArray = i['date'].split(' ')[0].split('-')[::-1]

        for datePart in dateArray: 
            d += datePart + '/'
        d = d[:-1]

        date = dt.datetime.strptime(d,'%d/%m/%Y').date()
        x.append(date)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.ylabel('followers')
    plt.savefig(user + '.png')
    pprint('Saved file for: ' + user)
