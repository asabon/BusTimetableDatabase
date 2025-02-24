import requests

def generate(filepath):
    url = 'https://www.kanachu.co.jp/dia/diagram/timetable01_js/course:0000803215-11/node:00129495/kt:0/lname:/dts:1740420000'
    response = requests.get(url)

    if response.status_code == 200:
        print("Success!")
        print(response.content)
    else:
        print("Failed to retrieve the page")
        print(f"Status code: {response.status_code}")

if __name__ == '__main__':
    generate()
