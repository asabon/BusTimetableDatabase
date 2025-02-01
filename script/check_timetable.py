import json

def strtoint(string):
    return int(string.replace(":", ""))

# timetable.json をチェックする。
def check_timetable(filePath):
    with open(filePath, 'r') as file:
        data = json.load(file)
        # 空欄ではないかチェック
        if (data['date'] == ""):
            return -1
        if (data['name'] == ""):
            return -1
        if (data['position'] == ""):
            return -1
        if (data['system'] == ""):
            return -1
        # 時刻の順番チェック (weekday)
        for i in range (1, len(data["weekday"])):
            before = strtoint(data["weekday"][i-1])
            after  = strtoint(data["weekday"][i])
            if before >= after:
                return -1
        # 時刻の順番チェック (saturday)
        for i in range (1, len(data["saturday"])):
            before = strtoint(data["saturday"][i-1])
            after  = strtoint(data["saturday"][i])
            if before >= after:
                return -1
        # 時刻の順番チェック (holiday)
        for i in range (1, len(data["holiday"])):
            before = strtoint(data["holiday"][i-1])
            after  = strtoint(data["holiday"][i])
            if before >= after:
                return -1
    return 0
