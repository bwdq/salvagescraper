from random import randrange
from webbrowser import Chrome
import requests
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import copy
import time

payload_base_all = {
    "draw": "1",
    "columns[0][data]": "0",
    "columns[0][name]": "",
    "columns[0][searchable]": "true",
    "columns[0][orderable]": "false",
    "columns[0][search][value]": "",
    "columns[0][search][regex]": "false",
    "columns[1][data]": "1",
    "columns[1][name]": "",
    "columns[1][searchable]": "true",
    "columns[1][orderable]": "false",
    "columns[1][search][value]": "",
    "columns[1][search][regex]": "false",
    "columns[2][data]": "2",
    "columns[2][name]": "",
    "columns[2][searchable]": "true",
    "columns[2][orderable]": "true",
    "columns[2][search][value]": "",
    "columns[2][search][regex]": "false",
    "columns[3][data]": "3",
    "columns[3][name]": "",
    "columns[3][searchable]": "true",
    "columns[3][orderable]": "true",
    "columns[3][search][value]": "",
    "columns[3][search][regex]": "false",
    "columns[4][data]": "4",
    "columns[4][name]": "",
    "columns[4][searchable]": "true",
    "columns[4][orderable]": "true",
    "columns[4][search][value]": "",
    "columns[4][search][regex]": "false",
    "columns[5][data]": "5",
    "columns[5][name]": "",
    "columns[5][searchable]": "true",
    "columns[5][orderable]": "true",
    "columns[5][search][value]": "",
    "columns[5][search][regex]": "false",
    "columns[6][data]": "6",
    "columns[6][name]": "",
    "columns[6][searchable]": "true",
    "columns[6][orderable]": "true",
    "columns[6][search][value]": "",
    "columns[6][search][regex]": "false",
    "columns[7][data]": "7",
    "columns[7][name]": "",
    "columns[7][searchable]": "true",
    "columns[7][orderable]": "true",
    "columns[7][search][value]": "",
    "columns[7][search][regex]": "false",
    "columns[8][data]": "8",
    "columns[8][name]": "",
    "columns[8][searchable]": "true",
    "columns[8][orderable]": "true",
    "columns[8][search][value]": "",
    "columns[8][search][regex]": "false",
    "columns[9][data]": "9",
    "columns[9][name]": "",
    "columns[9][searchable]": "true",
    "columns[9][orderable]": "true",
    "columns[9][search][value]": "",
    "columns[9][search][regex]": "false",
    "columns[10][data]": "10",
    "columns[10][name]": "",
    "columns[10][searchable]": "true",
    "columns[10][orderable]": "true",
    "columns[10][search][value]": "",
    "columns[10][search][regex]": "false",
    "columns[11][data]": "11",
    "columns[11][name]": "",
    "columns[11][searchable]": "true",
    "columns[11][orderable]": "true",
    "columns[11][search][value]": "",
    "columns[11][search][regex]": "false",
    "columns[12][data]": "12",
    "columns[12][name]": "",
    "columns[12][searchable]": "true",
    "columns[12][orderable]": "true",
    "columns[12][search][value]": "",
    "columns[12][search][regex]": "false",
    "columns[13][data]": "13",
    "columns[13][name]": "",
    "columns[13][searchable]": "true",
    "columns[13][orderable]": "true",
    "columns[13][search][value]": "",
    "columns[13][search][regex]": "false",
    "columns[14][data]": "14",
    "columns[14][name]": "",
    "columns[14][searchable]": "true",
    "columns[14][orderable]": "false",
    "columns[14][search][value]": "",
    "columns[14][search][regex]": "false",
    "columns[15][data]": "15",
    "columns[15][name]": "",
    "columns[15][searchable]": "true",
    "columns[15][orderable]": "false",
    "columns[15][search][value]": "",
    "columns[15][search][regex]": "false",
    "start": "0",
    "length": "20",
    "search[value]": "",
    "search[regex]": "false",
    "query": "*",
    "watchListOnly": "false",
    "freeFormSearch": "true",
    "page": "0",
    "size": "100"
}


def check_if_lotId_exist(lotId):
    cnx = mysql.connector.connect(host='localhost', user='root', password='my-secret-pw', database='copart1',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("SELECT * FROM lots WHERE lotId='{}'".format(lotId))
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


def add_lot_VIN(lotId, VIN):
    cnx = mysql.connector.connect(host='localhost', user='root', password='my-secret-pw', database='copart1',
                                  auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("INSERT INTO lots (lotId, VIN) VALUES ({}, '{}')".format(lotId, VIN))
    print(query)
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()


def getNumPages():
    return getTotalNumLots() / 100


def getTotalNumLots():
    s = requests.Session()
    headers = {
        "Host": "www.copart.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-XSRF-TOKEN": "a3979937-4ebb-40b7-ad1c-d9af76f3ae43",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Length": "3488",
        "Origin": "https://www.copart.com",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://www.copart.com/lotSearchResults/?free=true&query=*",
        "Cookie": "s_ppvl=%5B%5BB%5D%5D; s_ppv=public%253AsearchResults%2C37%2C37%2C961%2C1534%2C855%2C3072%2C1728%2C1.25%2CP; g2usersessionid=7d90a88ea25ffafd5ad77a7459772725; G2JSESSIONID=DB40C5C0CF4D4156E1E86C52EEDFE6A7-n1; userLang=en; visid_incap_242093=zykTC/CcSIu1y4YxWhCdiwL8MWAAAAAAQUIPAAAAAADds7qGBYXFKFqZfqAX9ReH; incap_ses_207_242093=50bVGrXceiQBgkB0r2nfAgL8MWAAAAAACHzUWGBWWNHVOwPQXOBRFg==; copartTimezonePref=%7B%22displayStr%22%3A%22PST%22%2C%22offset%22%3A-8%2C%22dst%22%3Afalse%2C%22windowsTz%22%3A%22America%2FLos_Angeles%22%7D; timezone=America%2FLos_Angeles; g2app.locationInfo=%7B%22countryCode%22%3A%22USA%22%2C%22countryName%22%3A%22United%20States%22%2C%22stateName%22%3A%22Washington%22%2C%22stateCode%22%3A%22WA%22%2C%22cityName%22%3A%22Seattle%22%2C%22latitude%22%3A47.60621%2C%22longitude%22%3A-122.33207%2C%22zipCode%22%3A%2298101%22%7D",
        "TE": "Trailers"
    }
    r = s.post('https://www.copart.com/public/lots/search', headers=headers, data=get_payload(0))
    # r Response type object
    if r.text.__contains__('incapsula'):
        print('fail')
    else:
        j = r.json()  # j is dict type
        data = j['data']
        results = data['results']
        totalElements = results['totalElements']
        return int(totalElements)

def searchPageNum(page_num):
    s = requests.Session()
    headers = {
        "Host": "www.copart.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-XSRF-TOKEN": "a3979937-4ebb-40b7-ad1c-d9af76f3ae43",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Length": "3488",
        "Origin": "https://www.copart.com",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://www.copart.com/lotSearchResults/?free=true&query=*",
        "Cookie": "s_ppvl=%5B%5BB%5D%5D; s_ppv=public%253AsearchResults%2C37%2C37%2C961%2C1534%2C855%2C3072%2C1728%2C1.25%2CP; g2usersessionid=7d90a88ea25ffafd5ad77a7459772725; G2JSESSIONID=DB40C5C0CF4D4156E1E86C52EEDFE6A7-n1; userLang=en; visid_incap_242093=zykTC/CcSIu1y4YxWhCdiwL8MWAAAAAAQUIPAAAAAADds7qGBYXFKFqZfqAX9ReH; incap_ses_207_242093=50bVGrXceiQBgkB0r2nfAgL8MWAAAAAACHzUWGBWWNHVOwPQXOBRFg==; copartTimezonePref=%7B%22displayStr%22%3A%22PST%22%2C%22offset%22%3A-8%2C%22dst%22%3Afalse%2C%22windowsTz%22%3A%22America%2FLos_Angeles%22%7D; timezone=America%2FLos_Angeles; g2app.locationInfo=%7B%22countryCode%22%3A%22USA%22%2C%22countryName%22%3A%22United%20States%22%2C%22stateName%22%3A%22Washington%22%2C%22stateCode%22%3A%22WA%22%2C%22cityName%22%3A%22Seattle%22%2C%22latitude%22%3A47.60621%2C%22longitude%22%3A-122.33207%2C%22zipCode%22%3A%2298101%22%7D",
        "TE": "Trailers"
    }
    r = s.post('https://www.copart.com/public/lots/search', headers=headers, data=get_payload(page_num))
    # r Response type object
    if r.text.__contains__('incapsula'):
        print('fail')
    else:
        j = r.json()  # j is dict type
        data = j['data']
        results = data['results']
        content = results['content']
        for lot in content:
            try:
                ldu = lot['ldu']
                print(lot['ln'], " ", lot['fv'])
                if not check_if_lotId_exist(lot['ln']):
                    add_lot_VIN(lot['ln'], lot['fv'])
                print(lot)
            except KeyError:
                print('bad fv')


def getLotDetails(lotId):
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
        j = r.json()  # j is dict type
        data = j['data']
        lot_details = data['lotDetails']
        make = lot_details['mkn']#this is how to get a field from the json response
        print(lot_details)


def get_payload(page_num):
    payload = copy.deepcopy(payload_base_all)
    payload["draw"] = int(payload["draw"]) + 1 * page_num
    payload["start"] = int(payload["start"]) + 20 * page_num
    payload["page"] = int(payload["page"]) + 1 * page_num
    return payload


def get_last_page_num():
    f = open("lastpage.txt", "r")
    last_page = f.read()
    f.close()
    return int(last_page)


def save_last_page(last_page):
    f = open("lastpage.txt", "w")
    f.write(str(last_page))
    f.close


if __name__ == '__main__':
    # for i in range(0, 10000):
    last_page = get_last_page_num()
    for i in range(last_page, 2000):
        searchPageNum(i)
        save_last_page(i)
        time.sleep(5 + randrange(6))
    #getLotDetails(21431747)
    # connectSQL()
    # testselenium()
