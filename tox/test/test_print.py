from __future__ import print_function

import pytest


def test_print():
    with pytest.raises(SyntaxError):
        eval("print 'test'")
    print('test')
