import warnings
warnings.filterwarnings("ignore")

import os
import csv
import matplotlib.pyplot as plt
import json
from pprint import pprint
from dateutil import parser
import datetime as dt
import matplotlib.dates as mdates
import pandas as pd

# list of instagram users
userNames = ['zeev_grim', 'grim_valerie']

def createUsersHistoryCsv(userName, userData):
    with open(userName + '/' + userName + '_statistics.csv', mode='w') as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(['Date', 'Followers', '', 'Following', '', 'Engagement', ''])
        reversedData = list(reversed(userData));

        for idx, curr in enumerate(reversedData):
            if idx == len(userData) - 1:
                csvWriter.writerow([curr['date'], curr['followers'],'-', curr['following'], '-', curr['avgEngagement'], '-'])
            else:
                prev = reversedData[idx + 1]
                deltaFollowers = int(curr['followers']) - int(prev['followers'])
                deltaFollowings = int(curr['following']) - int(prev['following'])
                deltaEngagement = float(curr['avgEngagement']) - float(prev['avgEngagement'])
        
                if deltaFollowers > 0: 
                    deltaFollowers = '+' + str(deltaFollowers)
                if deltaFollowings > 0: 
                    deltaFollowings = '+' + str(deltaFollowings)
                if deltaEngagement > 0: 
                    deltaEngagement = '+' + str(deltaEngagement)

                deltaEngagement = str(deltaEngagement) + '%'

                csvWriter.writerow([curr['date'], curr['followers'], deltaFollowers, curr['following'], deltaFollowings, curr['avgEngagement'], deltaEngagement])

        pprint('Saved the statistics csv file for: ' + userName)

def createUsersPredictionsCsv(userName, userData):
    deltasSum = 0
    for idx, curr in enumerate(userData):
        if idx != 0:
            prev = userData[idx - 1]
            deltasSum += int(curr['followers']) - int(prev['followers'])

    avg = int(deltasSum / (len(userData) - 1))

    with open(userName + '/' + userName + '_predictions.csv', mode='w') as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(['Time', 'Followers'])
        
        csvWriter.writerow(['30 days', 30 * avg])
        csvWriter.writerow(['60 days', 60 * avg])
        csvWriter.writerow(['3 month', 90 * avg])
        csvWriter.writerow(['6 month', 183 * avg])
        csvWriter.writerow(['9 month', 276 * avg])
        csvWriter.writerow(['1 year', 365 * avg])
        csvWriter.writerow(['1 year and a half', 548 * avg])
        csvWriter.writerow(['2 years', 730 * avg])
            
        pprint('Saved the predictions csv file for: ' + userName)


with open('data.json') as f:
    data = json.load(f)

for user in userNames:  
    if not os.path.exists(user):
        os.makedirs(user)

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
        i['date'] = date
        x.append(date)

    createUsersHistoryCsv(user, data[user])
    createUsersPredictionsCsv(user, data[user])

    df=pd.DataFrame({'x': x, 'y': y, 'y1': y1, 'y2': y2})

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    plt.ylabel('followers')
    plt.plot( 'x', 'y', data=df, marker='', color='royalblue', linewidth=2)
    plt.gcf().autofmt_xdate()
    plt.savefig(user + '/' + user + '_followers.png')
    plt.clf()

    plt.ylabel('following')
    plt.plot( 'x', 'y1', data=df, marker='', color='mediumorchid', linewidth=2)
    plt.gcf().autofmt_xdate()
    plt.savefig(user + '/' + user + '_following.png')
    plt.clf()

    plt.ylabel('average engagement')
    plt.plot( 'x', 'y2', data=df, marker='', color='mediumseagreen', linewidth=2)
    plt.gcf().autofmt_xdate()
    plt.savefig(user + '/' + user + '_avgEngagement.png')
    plt.clf()
    
    pprint('Saved all 3 files for: ' + user)