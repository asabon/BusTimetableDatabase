import json

def check_companies(dirName):
    companies_json_open = open(dirName + '/companies.json', 'r')
    companies_json_load = json.load(companies_json_open)
    for v in companies_json_load.values():
        print(v)
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
