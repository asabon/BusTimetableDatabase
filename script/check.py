import os
import json

def get_company_list(rootdir):
    companies_text = open(rootdir + '/companies.json', 'r', encoding='utf-8')
    companies_json = json.load(companies_text)
    return companies_json

def check_company(rootdir, companies_json):
    for company in companies_json['companies']:
        if (os.path.isdir(rootdir + '/' + company['directory']) != True):
            # Company のディレクトリが存在しなかったらエラー
            return -1

def check_all(rootdir):
    companies_json = get_company_list('database')
    result = check_company('database', companies_json)
    if (result != 0):
        return result
    return 0
