@echo off

python .\script\create_template.py .\database\�_�ސ쒆����� .\work\busstops.json
python .\script\update_route.py .\database\�_�ސ쒆����� .\work\busstops.json
python script/generate.py "database/�_�ސ쒆�����" False
