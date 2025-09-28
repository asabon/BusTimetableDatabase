import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from script.common.convert import to_half_width, to_safe_half_width

def test_to_half_width():
    assert to_half_width('アイウＡＢＣ１２３！＃＄％（）／') == 'アイウABC123!#$%()/'

def test_to_safe_half_width():
    assert to_safe_half_width('ＡＢＣ１２３') == 'ABC123'
