import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from task1 import say_hello

def test_say_hello(capsys):
    say_hello()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello, World!"