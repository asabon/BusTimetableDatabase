import sys
import os
from check_timetable import check_timetable

def check_all(rootdir):
    error_flag = 0
    for subdir, _, files in os.walk(rootdir):
        for file in files:
            if file != "busstops.json" and file != "route.json" and file.endswith('.json'):
                file_path = os.path.join(subdir, file)
                result = check_timetable(file_path)
                if result != 0:
                    error_flag = 1
    if error_flag != 0:
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check.py <rootdir>")
        sys.exit(1)
    result = check_all(sys.argv[1])
    sys.exit(result)
