import json
import sqlite3
import os
import sys

def json_to_sqlite(root_directory, output_file):
    # データベース作成
    conn = sqlite3.connect(output_file)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timetable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT,
        system TEXT NOT NULL,
        destinations TEXT NOT NULL,
        weekday TEXT,
        saturday TEXT,
        holiday TEXT
    )
    """)
    sub_directories = os.listdir(root_directory)
    for sub_directory in sub_directories:
        sub_directory_with_path = os.path.join(root_directory, sub_directory)
        files = os.listdir(sub_directory_with_path)
        for file in files:
            file_with_path = os.path.join(root_directory, sub_directory, file)
            if (file != "route.json"):
                try:
                    with open(file_with_path, "r", encoding="utf-8") as file_json:
                        data = json.load(file_json)
                        cursor.execute("INSERT INTO timetable (name, position, system, destinations, weekday, saturday, holiday) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (data["name"], data["position"], data["system"], json.dumps(data["destinations"]),
                        json.dumps(data["weekday"]), json.dumps(data["saturday"]), json.dumps(data["holiday"])))
                except json.JSONDecodeError:
                    print(f"JSON read error: {file_with_path}")
                    continue
    conn.commit()
    conn.close()

if __name__ == '__main__':
    root_directory = sys.argv[1]
    output_file = sys.argv[2]
    json_to_sqlite(root_directory, output_file)
