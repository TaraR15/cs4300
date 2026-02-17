import pytest
from task4 import calculate_discount
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

@pytest.mark.parametrize("price, discount, expected", [
    (100, 10, 90),
    (50.0, 20, 40.0),
    (200, 25.0, 150.0),
])
def test_discount(price, discount, expected):
    assert calculate_discount(price, discount) == expected

def test_invalid_type():
    with pytest.raises(TypeError):
        calculate_discount("100", 10)