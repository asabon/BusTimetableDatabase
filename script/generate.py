import requests
import certifi


def get_dummy_data():
    return "head 2024/07/08 0 0 0 0 0 0 0 0 0 0 0 0 - 42 0 6 39 0 0 0 39 0 0 0 0 0 0 0 0 heso 6 49 1 0 0 49 0 0 0 0 0 0 0 0 heso 6 49 2 0 0 49 0 0 0 0 0 0 0 0 heso 7 34 0 0 0 34 0 0 0 0 0 0 0 0 heso 7 54 2 0 0 54 0 0 0 0 0 0 0 0 heso 8 44 0 0 0 44 0 0 0 0 0 0 0 0 heso 8 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 9 58 0 0 0 58 0 0 0 0 0 0 0 0 heso 9 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 9 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 10 58 0 0 0 58 0 0 0 0 0 0 0 0 heso 10 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 10 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 11 39 0 0 0 39 0 0 0 0 0 0 0 0 heso 11 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 11 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 12 44 0 0 0 44 0 0 0 0 0 0 0 0 heso 12 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 12 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 13 44 0 0 0 44 0 0 0 0 0 0 0 0 heso 13 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 13 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 14 44 0 0 0 44 0 0 0 0 0 0 0 0 heso 14 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 14 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 15 44 0 0 0 44 0 0 0 0 0 0 0 0 heso 15 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 15 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 16 58 0 0 0 58 0 0 0 0 0 0 0 0 heso 16 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 16 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 17 54 0 0 0 54 0 0 0 0 0 0 0 0 heso 17 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 17 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 18 58 0 0 0 58 0 0 0 0 0 0 0 0 heso 18 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 18 6 2 0 0 06 0 0 0 0 0 0 0 0 heso 19 18 0 0 0 18 0 0 0 0 0 0 0 0 heso 19 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 19 3 2 0 0 03 0 0 0 0 0 0 0 0 heso 20 3 1 0 0 03 0 0 0 0 0 0 0 0 heso 20 3 2 0 0 03 0 0 0 0 0 0 0 0 heso end"


def get_data(url):
    url_dummy = 'https://www.kanachu.co.jp/dia/diagram/timetable01_js/course:0000803215-11/node:00129495/kt:0/lname:/dts:1740420000'
    response = requests.get(url_dummy, verify=certifi.where())
    if response.status_code == 200:
        print("Success!")
        print(response.content)
        return response.content
    else:
        print("Failed to retrieve the page")
        print(f"Status code: {response.status_code}")
        return None


def generate(filepath):
    data_string = get_dummy_data()
    data_list = data_string.split()
    update_date = data_list[1]
    num =  data_list[15]
    timetable_weekday = []
    timetable_saturday = []
    timetable_holiday = []
    print("update: " + update_date)
    for i in num:
        timetable_item = str(data_list[19 + (i * 15)]) + ":" + str(data_list[19 + ((i * 15) + 5)])
        day_type = data_list[19 + ((i * 15) + 2)]
        print("type: " + day_type + ", item : " + timetable_item)
        if day_type == 0:
            timetable_weekday.append(timetable_item)
        elif day_type == 1:
            timetable_saturday.append(timetable_item)
        elif day_type == 2:
            timetable_holiday.append(timetable_item)
        else:
            # error
            print("error")


if __name__ == '__main__':
    generate("")
