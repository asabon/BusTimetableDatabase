@echo off
chcp 65001 > nul

python .\script\create_template.py .\database\神奈川中央交通 .\work\busstops.json
python .\script\update_route.py .\database\神奈川中央交通 .\work\busstops.json
python script/generate.py "database/神奈川中央交通" False
