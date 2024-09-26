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

def get_route_dirs(company_dir):
    print("get_route_dirs(" + company_dir + ")")
    print(glob.glob(company_dir + '/**/route.json', recursive=True))

def check_result(result):
    if (result == 0):
        print("OK")
    else:
        print("NG")
        sys.exit(1)

def check_all(rootdir):
    companies_json = get_company_list(rootdir)
    result = check_company(rootdir, companies_json)
    check_result(result)
    for company in companies_json['companies']:
        get_route_dirs(rootdir + '/' + company['directory'])
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check.py <rootdir>")
        sys.exit(1)
    check_all(sys.argv[1])
