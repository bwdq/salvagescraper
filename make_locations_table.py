import time
import requests
import mysql.connector


def add_location(location): #tuple
    cnx = mysql.connector.connect(host='localhost', user='root', password='my-secret-pw', database='test',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("INSERT INTO location VALUES ({}, '{}', '{}', '{}', '{}', '{}','{}', '{}', '{}', '{}',{}, {})"
             .format(location[0], location[1], location[2], location[3],
                     location[4], location[5], location[6], location[7],
                     location[8], location[9], location[10], location[11]))
    print(query)
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()


def getLocationDetails(yardNum):
    print(yardNum + " getting")
    s = requests.Session()
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Access-Control-Allow-Headers": "Content-Type, X-XSRF-TOKEN",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        #"Cookie": "s_ppvl=public%253Alotdetails%2C31%2C31%2C855%2C1534%2C855%2C3072%2C1728%2C1.25%2CP; s_ppv=public%253AsearchResults%2C38%2C38%2C961%2C1534%2C855%2C3072%2C1728%2C1.25%2CP; g2usersessionid=7d90a88ea25ffafd5ad77a7459772725; G2JSESSIONID=547FCBC6F82DCAD757FB9363073C63E6-n1; userLang=en; visid_incap_242093=zykTC/CcSIu1y4YxWhCdiwL8MWAAAAAAQUIPAAAAAADds7qGBYXFKFqZfqAX9ReH; incap_ses_207_242093=p6RlczpNo12c72Z2r2nfAtqMM2AAAAAAYEyFSFP2O0FIZM1ZDQB1yQ==; copartTimezonePref=%7B%22displayStr%22%3A%22PST%22%2C%22offset%22%3A-8%2C%22dst%22%3Afalse%2C%22windowsTz%22%3A%22America%2FLos_Angeles%22%7D; timezone=America%2FLos_Angeles; g2app.locationInfo=%7B%22countryCode%22%3A%22USA%22%2C%22countryName%22%3A%22United%20States%22%2C%22stateName%22%3A%22Washington%22%2C%22stateCode%22%3A%22WA%22%2C%22cityName%22%3A%22Seattle%22%2C%22latitude%22%3A47.60621%2C%22longitude%22%3A-122.33207%2C%22zipCode%22%3A%2298101%22%7D; s_fid=5376A70C38122672-2C9C8EB8203360C9; s_nr=1613993530204-Repeat; s_vnum=1616480517566%26vn%3D2; s_lv=1613993530204; s_cc=true; incap_ses_725_242093=q4+2Q0FMvl6OdJfZ97cPCh1dM2AAAAAAyvHKC4imuf6p+Qis45qY5A==; s_pv=public%3Alotdetails; s_invisit=true; s_lv_s=Less%20than%207%20days; s_sq=%5B%5BB%5D%5D; incap_ses_524_242093=y9u4TalqAXsReIx0j59FB9mVM2AAAAAAUpLuPNW67iVak/elhIiXTQ==; s_depth=2",
        "Cookie": "s_ppv=public%253Alocations_st.-louis-mo-20%2C71%2C71%2C855%2C1534%2C855%2C3072%2C1728%2C1.25%2CP; s_ppvl=public%253Alocations%2C48%2C48%2C855%2C1534%2C855%2C3072%2C1728%2C1.25%2CP; visid_incap_242093=zlRbINB7TdO1iV1varpYGi8KOmAAAAAAQUIPAAAAAADyz7zFDAUS9vT7gB5u4eHu; incap_ses_207_242093=lo65PTY1Yk6DvZy/sWnfAi8KOmAAAAAA5q7xRym3nZXBId6tQTiKMw==; g2usersessionid=713bc97ef3fb607e35728bb615a1ad66; G2JSESSIONID=C7C154213BC3C0EEF9F9EB01EE48EFDB-n1; userLang=en; copartTimezonePref=%7B%22displayStr%22%3A%22PST%22%2C%22offset%22%3A-8%2C%22dst%22%3Afalse%2C%22windowsTz%22%3A%22America%2FLos_Angeles%22%7D; timezone=America%2FLos_Angeles; g2app.locationInfo=%7B%22countryCode%22%3A%22USA%22%2C%22countryName%22%3A%22United%20States%22%2C%22stateName%22%3A%22Washington%22%2C%22stateCode%22%3A%22WA%22%2C%22cityName%22%3A%22Seattle%22%2C%22latitude%22%3A47.60621%2C%22longitude%22%3A-122.33207%2C%22zipCode%22%3A%2298101%22%7D; s_fid=7113D9189E05F7F8-0DE62D83A8365A00; s_depth=4; s_pv=public%3Alocations_st.-louis-mo-20; s_nr=1614416490367-New; s_vnum=1617008455972%26vn%3D1; s_invisit=true; s_lv=1614416490368; s_lv_s=First%20Visit; s_cc=true; s_sq=%5B%5BB%5D%5D",
        "DNT": "1",
        "Host": "www.copart.com",
        "If-Modified-Since": "Mon, 26 Jul 1997 05:00:00 GMT",
        "Pragma": "no-cache",
        #"Referer": "https://www.copart.com/lot/20881167/salvage-2011-nissan-armada-sv-tn-memphis",
        "Referer": "https://www.copart.com/lot/20881167/",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
        "X-Requested-With": "XMLHttpRequest",
        "X-XSRF-TOKEN": "1337a1ef-f4a0-41cd-8ea8-1636002f04ac"
    }
    r = s.get('https://www.copart.com/public/data/locations/retrieveLocationDetail?yardNumber={}'.format(yardNum), headers=headers)
    # r Response type object
    if r.text.__contains__('Incapsula') or r.text.__contains__('error'):
        print('fail: ' + r.text)
    else:
        print(r.text)
        j = r.json()  # j is dict type
        data = j['data']
        if data is not None:
            yardName = data['yardName']
            yardStateName = data['yardStateName']
            yardStateCode = data['yardStateCode']
            yardCity = data['yardCity']
            gmFullName = data['gmFullName']
            yardPhoneAreaCode = data['yardPhoneAreaCode']
            yardPhoneNumber = data['yardPhoneNumber']
            yardAddress1 = data['yardAddress1']
            yardZip = data['yardZip']
            yardLatitude = data['yardLatitude']
            yardLongitude = data['yardLongitude']
            location = (yardNum, yardName, yardStateName, yardStateCode, yardCity,
                    gmFullName, yardPhoneAreaCode, yardPhoneNumber, yardAddress1, yardZip, yardLatitude, yardLongitude)
            add_location(location)


def check_if_location_exist(yardNum):
    cnx = mysql.connector.connect(host='localhost', user='root', password='my-secret-pw', database='MySQL_Proj08',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("SELECT * FROM location WHERE yardNumber={}".format(yardNum))
    cursor.execute(query)
    all = cursor.fetchall()
    if len(all) > 0:
        cursor.close()
        cnx.close()
        return True
    else:
        cursor.close()
        cnx.close()
        return False


def getYardNums():
    f = open("yardNums.txt", "r")
    all = f.read()
    yardNums = all.splitlines()
    f.close()
    return yardNums


if __name__ == '__main__':

    print(getYardNums())
    print(type(getYardNums()))
    for num in getYardNums():
        if check_if_location_exist(num):
            print(num + "already exists")
        else:
            getLocationDetails(num)
            time.sleep(1)
