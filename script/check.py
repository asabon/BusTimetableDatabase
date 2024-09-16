import os
import json

def check_all(rootdir):
    company_text = open(rootdir + '/companies.json', 'r', encoding='utf-8')
    company_json = json.load(company_text)
    for company in company_json['companies']:
        # Company のディレクトリが存在しなかったらエラー
        if(os.path.isdir(rootdir + '/' + company['directory']) != True):
            return -1
        system_text = open(rootdir + '/' + company['directory'] + '/' + 'systems.json', 'r', encoding='utf-8')
        system_json = json.load(system_text)
        for system in system_json['systems']:
            # System のディレクトリが存在しなかったらエラー
            if(os.path.isdir(rootdir + '/' + company['directory'] + '/' + system['directory']) != True):
                return -1
    return 0
