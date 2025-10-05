import os
import tempfile
import json
import pytest
from script.v2.json_editor import JsonEditor

def test_set_and_get_value_dict():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        tmp.write(json.dumps({}).encode('utf-8'))
        tmp_path = tmp.name

    editor = JsonEditor(tmp_path)
    editor.set_value("parent.child.name", "foo")
    assert editor.get_value("parent.child.name") == "foo"
    editor.save()

    # 再ロードして確認
    editor2 = JsonEditor(tmp_path)
    assert editor2.get_value("parent.child.name") == "foo"
    os.remove(tmp_path)

def test_set_and_get_value_list():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        tmp.write(json.dumps({}).encode('utf-8'))
        tmp_path = tmp.name

    editor = JsonEditor(tmp_path)
    editor.set_value("parent.child.0.name", "bar")
    assert editor.get_value("parent.child.0.name") == "bar"
    editor.set_value("parent.child.1.name", "baz")
    assert editor.get_value("parent.child.1.name") == "baz"
    editor.save()

    # 再ロードして確認
    editor2 = JsonEditor(tmp_path)
    assert editor2.get_value("parent.child.0.name") == "bar"
    assert editor2.get_value("parent.child.1.name") == "baz"
    os.remove(tmp_path)

def test_get_value_not_found():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
        tmp.write(json.dumps({"a": {"b": 1}}).encode('utf-8'))
        tmp_path = tmp.name

    editor = JsonEditor(tmp_path)
    assert editor.get_value("a.c") == ""
    assert editor.get_value("a.b.c") == ""
    os.remove(tmp_path)