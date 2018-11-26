import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import json
from pprint import pprint
from dateutil import parser
import datetime as dt
import matplotlib.dates as mdates
import pandas as pd

userNames = ['zeev_grim', 'grim_valerie']

with open('data.json') as f:
    data = json.load(f)

for user in userNames:
    x, y, y1, y2 = [], [], [], []

    for i in data[user]:
        y.append(int(i['followers']))
        y1.append(int(i['following']))
        y2.append(float(i['avgEngagement']))
        d = ''
        dateArray = i['date'].split(' ')[0].split('-')[::-1]

        for datePart in dateArray: 
            d += datePart + '/'
        d = d[:-1]

        date = dt.datetime.strptime(d,'%d/%m/%Y').date()
        x.append(date)

    df=pd.DataFrame({'x': x, 'y': y, 'y1': y1, 'y2': y2})

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    plt.ylabel('followers')
    plt.plot( 'x', 'y', data=df, marker='', color='royalblue', linewidth=2)
    plt.gcf().autofmt_xdate()
    plt.savefig(user + '_followers.png')
    plt.clf()

    plt.ylabel('following')
    plt.plot( 'x', 'y1', data=df, marker='', color='mediumorchid', linewidth=2)
    plt.gcf().autofmt_xdate()
    plt.savefig(user + '_following.png')
    plt.clf()

    plt.ylabel('average engagement')
    plt.plot( 'x', 'y2', data=df, marker='', color='mediumseagreen', linewidth=2)
    plt.gcf().autofmt_xdate()
    plt.savefig(user + '_avgEngagement.png')
    plt.clf()
    
    pprint('Saved all 3 files for: ' + user)
