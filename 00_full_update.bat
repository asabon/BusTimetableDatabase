@echo off

python .\script\create_template.py .\database\_“Şì’†‰›Œğ’Ê .\work\busstops.json
python .\script\update_route.py .\database\_“Şì’†‰›Œğ’Ê .\work\busstops.json
python script/generate.py "database/_“Şì’†‰›Œğ’Ê" False
