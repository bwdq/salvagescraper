import mysql
import requests


def getTableId(table, attribColumn, attrib):
    #if not found return -1
    #else return id num
    cnx = mysql.connector.connect(host='localhost', user='root', password='my-secret-pw', database='copart1',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("SELECT * FROM {} WHERE {} = '{}'".format(table, attribColumn, attrib))
    print(query)
    cursor.execute(query)
    all = cursor.fetchall()
    if len(all) > 0:
        id = all[0]
        cursor.close()
        cnx.close()
        return id
    else:
        cursor.close()
        cnx.close()
        return -1




def updateLot(lotId, VIN,colName, value):
    cnx = mysql.connector.connect(host='localhost', user='root', password='my-secret-pw', database='copart1',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("UPDATE lots (colName) VALUES ({}) WHERE lotId = {} AND VIN = '{}'".format(value, lotId, VIN))
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
        "Cookie": "s_ppvl=public%253Alotdetails%2C31%2C31%2C855%2C1534%2C855%2C3072%2C1728%2C1.25%2CP; s_ppv=public%253AsearchResults%2C38%2C38%2C961%2C1534%2C855%2C3072%2C1728%2C1.25%2CP; g2usersessionid=7d90a88ea25ffafd5ad77a7459772725; G2JSESSIONID=547FCBC6F82DCAD757FB9363073C63E6-n1; userLang=en; visid_incap_242093=zykTC/CcSIu1y4YxWhCdiwL8MWAAAAAAQUIPAAAAAADds7qGBYXFKFqZfqAX9ReH; incap_ses_207_242093=p6RlczpMo12c72Z2r2nfAtqMM2AAAAAAYEyFSFP2O0FIZM1ZDQB1yQ==; copartTimezonePref=%7B%22displayStr%22%3A%22PST%22%2C%22offset%22%3A-8%2C%22dst%22%3Afalse%2C%22windowsTz%22%3A%22America%2FLos_Angeles%22%7D; timezone=America%2FLos_Angeles; g2app.locationInfo=%7B%22countryCode%22%3A%22USA%22%2C%22countryName%22%3A%22United%20States%22%2C%22stateName%22%3A%22Washington%22%2C%22stateCode%22%3A%22WA%22%2C%22cityName%22%3A%22Seattle%22%2C%22latitude%22%3A47.60621%2C%22longitude%22%3A-122.33207%2C%22zipCode%22%3A%2298101%22%7D; s_fid=5376A70C38122672-2C9C8EB8203360C9; s_nr=1613993530204-Repeat; s_vnum=1616480517566%26vn%3D2; s_lv=1613993530204; s_cc=true; incap_ses_725_242093=q4+2Q0FMvl6OdJfZ97cPCh1dM2AAAAAAyvHKC4imuf6p+Qis45qY5A==; s_pv=public%3Alotdetails; s_invisit=true; s_lv_s=Less%20than%207%20days; s_sq=%5B%5BB%5D%5D; incap_ses_524_242093=y9u4TalqAXsReIx0j59FB9mVM2AAAAAAUpLuPNW67iVak/elhIiXTQ==; s_depth=2",
        "DNT": "1",
        "Host": "www.copart.com", "If-Modified-Since": "Mon, 26 Jul 1997 05:00:00 GMT", "Pragma": "no-cache",
        #"Referer": "https://www.copart.com/lot/20881167/salvage-2011-nissan-armada-sv-tn-memphis",
        "Referer": "https://www.copart.com/lot/20881167/",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
        "X-Requested-With": "XMLHttpRequest",
        "X-XSRF-TOKEN": "8b924180-d85b-4182-9cdf-5fefc4c416e2"
    }
    r = s.get('https://www.copart.com/public/data/lotdetails/solr/{}'.format(lotId), headers=headers)
    # r Response type object
    if r.text.__contains__('incapsula'):
        print('fail')
    else:
        print(r.text)
        j = r.json()  # j is dict type
        data = j['data']
        lot_details = data['lotDetails']
        make = lot_details['mkn']#this is how to get a field from the json response
        print(lot_details)

def readLots():
    f = open("lot_vins.csv", "r")
    lots = f.read().split('\n')
    f.close()
    try:
        for lot in lots:
            id_vin = lot.split(',')
            getLotDetails(id_vin[0], id_vin[1])
            print(id_vin[0])
            print(id_vin[1])
    except IndexError:
        print('end file')


if __name__ == '__main__':
    readLots()