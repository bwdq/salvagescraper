import time
from random import randrange

import mysql
import requests
import mysql.connector


def getTableId(table, attribColumn, attrib):
    #if not found create record and rerun to get id num
    #else return id num
    cnx = mysql.connector.connect(host='localhost', user='root', password='my-secret-pw', database='test',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("SELECT * FROM {} WHERE {} = '{}'".format(table, attribColumn, attrib))
    cursor.execute(query)
    all = cursor.fetchall()
    if len(all) > 0:
        item = all[0]
        id = item[0]
        cursor.close()
        cnx.close()
        return id
    else:
        query = ("INSERT INTO {} VALUES (DEFAULT, '{}')".format(table, attrib))
        cursor.execute(query)
        cursor.close()
        cnx.commit()
        cnx.close()
        id = getTableId(table, attribColumn, attrib)
        return id

def getLocationId(long, lat):
    cnx = mysql.connector.connect(host='localhost', user='root', password='my-secret-pw', database='test',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("SELECT * FROM location WHERE yardLongitude = {} AND yardLatitude = {}".format(long, lat))
    cursor.execute(query)
    all = cursor.fetchall()
    if len(all) > 0:
        item = all[0]
        id = item[0]
        cursor.close()
        cnx.close()
        return id
    else:
        print('Location not found')

def updateLot(lotId, VIN, modelVal, makeVal, lmodelVal, long, lat):
    cnx = mysql.connector.connect(host='localhost', user='root', password='my-secret-pw', database='test',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    makeId = getTableId("make", "name", makeVal)
    modelId = getTableId("model", "name", modelVal)
    lmodelId = getTableId("lmodel", "name", lmodelVal)
    yardNum = getLocationId(long, lat)
    query = ("UPDATE lots SET makeId = {}, modelId = {}, lmodelId = {}, yardNumber = {}  WHERE lotId = {} AND VIN = '{}'".format(makeId, modelId, lmodelId, yardNum, lotId, VIN))
    print(query)
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def add_bid(lotId, bidAmt):
    cnx = mysql.connector.connect(host='localhost', user='root', password='my-secret-pw', database='test',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("INSERT INTO bid VALUES (DEFAULT, {}, {}, CURRENT_TIMESTAMP() ) ".format(lotId, bidAmt))
    print(query)
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()

def getLotDetails(lotId, vin):
    s = requests.Session()
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Access-Control-Allow-Headers": "Content-Type, X-XSRF-TOKEN",
        "Cache-Control": "no-cache, max-age=0",
        "Connection": "keep-alive",
        #"Cookie": "s_ppvl=public%253Alotdetails%2C44%2C44%2C1042%2C2048%2C1042%2C2048%2C1152%2C1.25%2CP; s_ppv=public%253AsearchResults%2C43%2C43%2C1042%2C2048%2C1042%2C2048%2C1152%2C1.25%2CP; g2usersessionid=12863a5a8f22c4bc666d76b0ca01d386; G2JSESSIONID=0F273BE28E044B684EC9F3F414097AB9-n2; userLang=en; visid_incap_242093=Naahr7RBSz6NQrvHUfpuhwDDNmAAAAAAQkIPAAAAAACA+8uaAUusc4x6o2cPKEocqtYJJpQGLsEU; incap_ses_207_242093=41cWQuFWcUk89GZttmnfAkTZS2AAAAAAXK6Riz/YQgiRvzHco8pQjQ==; copartTimezonePref=%7B%22displayStr%22%3A%22PST%22%2C%22offset%22%3A-8%2C%22dst%22%3Afalse%2C%22windowsTz%22%3A%22America%2FLos_Angeles%22%7D; timezone=America%2FLos_Angeles; g2app.locationInfo=%7B%22countryCode%22%3A%22USA%22%2C%22countryName%22%3A%22United%20States%22%2C%22stateName%22%3A%22Washington%22%2C%22stateCode%22%3A%22WA%22%2C%22cityName%22%3A%22Seattle%22%2C%22latitude%22%3A47.60621%2C%22longitude%22%3A-122.33207%2C%22zipCode%22%3A%2298101%22%7D; s_fid=14B85D2E0837EEB1-34FD50132B5CBCED; s_nr=1615586448285-Repeat; s_vnum=1616793601528%26vn%3D15; s_lv=1615586448286; s_cc=true; incap_ses_725_242093=UJFGO/uImQ0iaeGJpvACA1nkS2AAAAAAMLEhzeVWL9SxDdBmkRJqsg==; s_pv=public%3Alotdetails; s_invisit=true; s_lv_s=Less%20than%201%20day; s_sq=%5B%5BB%5D%5D; incap_ses_235_242093=41cWQuFWcUk89GZttmnfAkTZS2AAAAAAXK6Riz/YQgiRvzHco8pQjQ==; s_depth=1",
        "Cookie": "s_ppvl=public%253Alotdetails%2C29%2C29%2C670%2C1535%2C496%2C3072%2C1728%2C1.25%2CP; s_ppv=public%253AsearchResults%2C39%2C39%2C1024%2C1535%2C496%2C3072%2C1728%2C1.25%2CP; visid_incap_242093=pA2P5Zj6R9Sy11CXCOeEUnPUTmAAAAAAQUIPAAAAAADkvwYHL5rIRXmTJl3hi8l0; incap_ses_207_242093=zcqEDzAArlpjfq5xtmnfAnPUTmAAAAAA3QgZj3Qr87Tl3Uk+pYa87A==; g2usersessionid=0b4f61da6613900ecce840bc5d774668; G2JSESSIONID=E45F1D243EE0FB4340D13BDBB82CE67B-n2; userLang=en; copartTimezonePref=%7B%22displayStr%22%3A%22PDT%22%2C%22offset%22%3A-7%2C%22dst%22%3Atrue%2C%22windowsTz%22%3A%22America%2FLos_Angeles%22%7D; timezone=America%2FLos_Angeles",
        "DNT": "1",
        "Host": "www.copart.com",
        "If-Modified-Since": "Mon, 26 Jul 1997 05:00:00 GMT",
        "Pragma": "no-cache",
        #"Referer": "https://www.copart.com/lot/20881167/salvage-2011-nissan-armada-sv-tn-memphis",
        "Referer": "https://www.copart.com/lot/{}/".format(lotId),
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
        "X-Requested-With": "XMLHttpRequest",
        "X-XSRF-TOKEN": "54004c88-0493-469e-887e-5bd278bca8f5"
    }
    #headers['Referer'] = "https://www.copart.com/lot/{}/".format(lotId)
    r = s.get('https://www.copart.com/public/data/lotdetails/solr/{}'.format(lotId), headers=headers)
    # r Response type object
    print(lotId + r.text)
    if r.text.__contains__('Incapsula') or r.text.__contains__('Error'):
        print('fail')
    else:
        j = r.json()  # j is dict type
        data = j['data']
        lot_details = data['lotDetails']
        model = lot_details['lmg']
        lmodel = lot_details['lm']
        make = lot_details['mkn']#this is how to get a field from the json response
        longitude = lot_details['long']
        latitude = lot_details['lat']
        bidAmt = lot_details['hb']
        add_bid(lotId, bidAmt)
        print(lotId, vin, model, make, lmodel, longitude, latitude)
        updateLot(lotId, vin, model, make, lmodel, longitude, latitude)
        #print(make)
        #print(lot_details)

def lotExists(lotId):
    cnx = mysql.connector.connect(host='localhost', user='root', password='my-secret-pw', database='test',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("SELECT * FROM lots WHERE lotId = {}".format(lotId))
    cursor.execute(query)
    all = cursor.fetchall()
    if len(all) > 0:
        item = all[0]
        yard = item[3]
        cursor.close()
        cnx.close()
        # assume if yard is None then data for lot doesn't exist
        if yard is None:
            return False
        else:
            return True
    else:
        #lot isn't in table
        return False


def readLots():
    f = open("lot_vins4.csv", "r")
    lots = f.read().split('\n')
    f.close()
    try:
        for lot in lots:
            print(lot)
            id_vin = lot.split(',')
            # if it already exists skip getting it
            if lotExists(id_vin[0]):
                print("already exists")
            else:
                getLotDetails(id_vin[0], id_vin[1])
                time.sleep(1 + randrange(2))
            #print(id_vin[0])
            #print(id_vin[1])
    except IndexError:
        print('end file')


if __name__ == '__main__':
    readLots()
