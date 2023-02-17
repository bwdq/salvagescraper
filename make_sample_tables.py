import time
import requests
import mysql.connector

def addState(id, abbr, name, country):
    cnx = mysql.connector.connect(host='localhost', user='root', password='password', database='', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("INSERT INTO states VALUES ({}, '{}', '{}', '{}')".format(id, abbr, name, country))
    cursor.execute(query)
    cursor.close()
    cnx.commit()
    cnx.close()

def readStates():
    f = open("states.txt", "r")
    states = f.read().split('\n')
    f.close()
    try:
        for state in states:
            id_st = state.split(',')
            addState(id_st[0], id_st[1], id_st[2], id_st[3])

    except IndexError:
        print('end file')

def addLocation(yardNum, yardName, stateId, city, gmManager, areaCode, phoneNum, address1, zipcode, latitude, longitude):
    cnx = mysql.connector.connect(host='localhost', user='root', password='password', database='', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("INSERT INTO location VALUES ({}, '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', {}, {})".format(yardNum, yardName, stateId, city, gmManager, areaCode, phoneNum, address1, zipcode, latitude, longitude))
    cursor.execute(query)
    cursor.close()
    cnx.commit()
    cnx.close()

def readLocations():
    f = open("locations.csv", "r")
    locations = f.read().split('\n')
    f.close()
    try:
        for location in locations:
            id_loc = location.split(',')
            addLocation(id_loc[0], id_loc[1], id_loc[2], id_loc[3], id_loc[4], id_loc[5], id_loc[6], id_loc[7], id_loc[8], id_loc[9], id_loc[10])

    except IndexError:
        print('end file')

def addOther(tableName, id_attr, name):
    cnx = mysql.connector.connect(host='localhost', user='root', password='', database='', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("INSERT INTO {} VALUES ({}, '{}')".format(tableName, id_attr, name))
    cursor.execute(query)
    cursor.close()
    cnx.commit()
    cnx.close()

def readOther(fileName, tableName):
    f = open(fileName, "r")
    items = f.read().split('\n')
    f.close()
    try:
        for item in items:
            id_item = item.split(',')
            addOther(tableName, id_item[0], id_item[1])

    except IndexError:
        print('end file')

def addLot(lotId, litVin, yardNum, makeId, modelId, lmodelId):
    cnx = mysql.connector.connect(host='localhost', user='root', password='password', database='', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("INSERT INTO lots VALUES ({}, '{}', {}, {}, {}, {})".format(lotId, litVin, yardNum, makeId, modelId, lmodelId))
    cursor.execute(query)
    cursor.close()
    cnx.commit()
    cnx.close()

def readLots():
    f = open("sample-lots.csv", "r")
    lots = f.read().split('\n')
    f.close()
    try:
        for lot in lots:
            id_lot = lot.split(',')
            addLot(id_lot[0], id_lot[1], id_lot[2], id_lot[3], id_lot[4], id_lot[5])

    except IndexError:
        print('end file')

if __name__ == '__main__':
    readStates()
    print("states populated")
    readLocations()
    print("locations populated")
    readOther("sample-lmodels.csv", "lmodel")
    print("lmodels populated")
    readOther("sample-models.csv", "model")
    print("models populated")
    readOther("sample-makes.csv", "make")
    print("makes populated")
    readLots()
    print("lots populated")
