import os
import json

def check_companies(dirName):
    print("[check_companies]")
    text_data = open(dirName + '/companies.json', 'r', encoding='utf-8')
    json_data = json.load(text_data)
    for company in json_data['companies']:
        print("  " + company['name'])
        print("  " + company['directory'])
        if(os.path.isdrir(company['directory']) != True):
            return -1
    return 0

def check_systems(dirName):
    return 0

def check_timetable():
    return 0

def check_all(rootdir):
    result_companies = check_companies(rootdir)
    if result_companies != 0:
        return result_companies
    return 0
