import json
import sqlite3
import os
import sys

def create_database(filename):
    conn = sqlite3.connect(filename)
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
    return cursor

def json_to_sqlite(root_directory, output_file):

    print("root_directory = " + root_directory)
    print("output_file    = " + output_file)

    # データベース作成
    # cursor = create_database(output_file)

    sub_directories = os.listdir(root_directory)
    for sub_directory in sub_directories:
        print("sub_directory: " + sub_directory)
        files = os.listdir(sub_directory)
        for file in files:
            print("file: " + file)
            #with open("a.json", "r", encoding="utf-8") as file:
            #    data = json.load(file)

if __name__ == '__main__':
    root_directory = sys.argv[1]
    output_file = sys.argv[2]
    json_to_sqlite(root_directory, output_file)
