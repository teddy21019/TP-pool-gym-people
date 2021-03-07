import requests
import json
from datetime import datetime
import time
import pytz
import os

# configuration
c = ['date_time','swPeopleNum','gymPeopleNum','LID']
sc_url = 'http://booking.tpsc.sporetrofit.com/Home/loadLocationPeopleNum'
ntu_sc_url = 'https://ntusportscenter.ntu.edu.tw/counter.txt'
dir = os.path.dirname(os.path.abspath(__file__))

# df = resetDataFrame()

def getCount():

    #better write try catch
    sc = requests.post(sc_url).content
    ntu = requests.get(ntu_sc_url).content
    
    return sc, ntu


def newData():
    with open(dir+'/data.csv','a') as datafile:
            
        data_sportscenter_json, data_NTU_json = getCount()

        # time stamp
        tz = pytz.timezone('Asia/Taipei') 
        t = datetime.now(tz)
        t_string = t.strftime("%Y-%m-%d %H:%M")


        # Sports Center

        sc_data = json.loads(data_sportscenter_json)
        sc_data = sc_data['locationPeopleNums']

        for item in sc_data:
            to_write_txt = ','.join([t_string, item['swPeopleNum'], item['gymPeopleNum'], item['LID']])+"\n"
            datafile.write(to_write_txt)



        # NTU
        ntu_data = json.loads(data_NTU_json)
        ntu_data = ntu_data['CounterData'][0]['innerCount'].split(';')

        to_write_txt = ','.join([t_string, ntu_data[1], ntu_data[0], 'NTU'])+"\n"
        datafile.write(to_write_txt)


if __name__ == '__main__':

    if not os.path.exists(dir+'/data.csv'):
        with open(dir+'/data.csv', 'a') as datafile:
            datafile.write(','.join(c)+'\n')

    newData()
