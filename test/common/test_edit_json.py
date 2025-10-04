import os
import tempfile
import pytest
from script.common.edit_json import (
    read_json_file,
    write_json_file,
    get_value_from_json_file,
    get_value_from_json,
    set_value_in_json,
    update_json_file
)

def test_write_and_read_json_file():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    temp_file.close()  # ファイルを閉じてから使う
    try:
        data = {"key": "value"}
        write_json_file(temp_file.name, data)
        loaded = read_json_file(temp_file.name)
        assert loaded == data
    finally:
        os.remove(temp_file.name)

def test_get_value_from_json():
    data = {"foo": "bar"}
    assert get_value_from_json(data, "foo") == "bar"
    assert get_value_from_json(data, "notfound") == ""

def test_set_value_in_json():
    data = {}
    result = set_value_in_json(data, "key", "val")
    assert result["key"] == "val"

def test_update_json_file_and_get_value_from_json_file():
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    temp_file.close()  # ファイルを閉じてから使う
    try:
        update_json_file(temp_file.name, "hello", "world")
        loaded = read_json_file(temp_file.name)
        assert loaded["hello"] == "world"
    finally:
        os.remove(temp_file.name)