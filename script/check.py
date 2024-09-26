import os
import json

def get_company_list(rootdir):
    print("get_company_list")
    companies_text = open(rootdir + '/companies.json', 'r', encoding='utf-8')
    companies_json = json.load(companies_text)
    print(" " + companies_json)
    return companies_json

def check_company(rootdir, companies_json):
    print("check_company")
    for company in companies_json['companies']:
        if (os.path.isdir(rootdir + '/' + company['directory']) != True):
            print (" Error")
            return -1
    print (" OK")
    return 0

def check_all(rootdir):
    companies_json = get_company_list(rootdir)
    result = check_company(rootdir, companies_json)
    if (result != 0):
        print ("check_all: Error")
        return result
    print("check_all: OK")
    return 0
