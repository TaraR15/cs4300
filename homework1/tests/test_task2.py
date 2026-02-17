import sys
import os
import pytest
import task2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


@pytest.mark.parametrize("func, expected_type", [
    (task2.get_integer, int),
    (task2.get_float, float),
    (task2.get_string, str),
    (task2.get_boolean, bool),
])
def test_types(func, expected_type):
    assert isinstance(func(), expected_type)