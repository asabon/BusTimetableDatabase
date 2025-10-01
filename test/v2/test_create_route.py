import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from script.v2.create_route_json2 import parse_route_html

def test_create_route_json():
    input_file = 'test/data/v2/create_route_json/cache/014bf45b02b224dbc925ede1cd844fb4.txt'
    expected_file = 'test/data/v2/create_route_json/expected.json'
    output_file = 'test/data/v2/create_route_json/output.json'
    with open(input_file, encoding='utf-8') as f:
        input_data = f.read()
    busstops = parse_route_html(input_data)
    print(len(busstops))
    print(busstops)
