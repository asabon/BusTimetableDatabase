import sys
import os
import json
import glob

def get_company_list(rootdir):
    print("get_company_list")
    companies_text = open(rootdir + '/companies.json', 'r', encoding='utf-8')
    companies_json = json.load(companies_text)
    return companies_json

def check_company(rootdir, companies_json):
    print("check_company")
    for company in companies_json['companies']:
        print (" company['directory'] = " + company['directory'])
        if (os.path.isdir(rootdir + '/' + company['directory']) != True):
            print (" Error")
            return -1
    print (" OK")
    return 0

def get_route_files(company_dir):
    print("get_route_dirs(" + company_dir + ")")
    route_files = glob.glob(company_dir + '/**/route.json', recursive=True)
    return route_files

def get_route_dir(route_file):
    return os.path.split(route_file)[0]

def check_route_file(route_dir):
    route_text = open(route_dir + '/route.json', 'r', encoding='utf-8')
    route_json = json.load(route_text)
    # route.json に記載されている *.json が存在するか確認
    for station in route_json['stations']:
        if station['file'] != "":
            station_file = route_dir + '/' + station['file']
            if (os.path.isfile(station_file) != True):
                print(' ' + station_file + ' is NOT exist. ERROR')
                return -1
    # *.json が、route.json に記載されているか確認
    station_files = glob.glob(route_dir + '/*.json')
    for station_file in station_files:
        if os.path.split(station_file)[1] != 'route.json':
            isExist = False
            for station in route_json['stations']:
                if os.path.split(station_file)[1] == station['file']:
                    isExist = True
            if isExist == False:
                print(station_file + " is NOT written in route.json")
                return -1    
    return 0

def check_result(result):
    if (result != 0):
        print("NG")
        sys.exit(1)

def check_all(rootdir):
    companies_json = get_company_list(rootdir)
    result = check_company(rootdir, companies_json)
    check_result(result)
    for company in companies_json['companies']:
        route_files = get_route_files(rootdir + '/' + company['directory'])
        for route_file in route_files:
            result = check_route_file(get_route_dir(route_file))
            check_result(result)
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check.py <rootdir>")
        sys.exit(1)
    check_all(sys.argv[1])
