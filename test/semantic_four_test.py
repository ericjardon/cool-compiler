import pytest

from main import dummy
from main import compile
from util.exceptions import *

def test_assignment():
     with pytest.raises(Exception):
         compile('resources/semantic/input/assignment.cool')

def test_basic():
     with pytest.raises(Exception):
         compile('resources/semantic/input/basic.cool')

def test_basicclassestree():
    with pytest.raises(Exception):
        compile('resources/semantic/input/basicclassestree.cool')

def test_cells():
    with pytest.raises(Exception):
        compile('resources/semantic/input/cells.cool')

def test_classes():
    with pytest.raises(Exception):
        compile('resources/semantic/input/classes.cool')

def test_compare():
    with pytest.raises(Exception):
        compile('resources/semantic/input/compare.cool')

def test_comparisons():
    with pytest.raises(Exception):
        compile('resources/semantic/input/comparisons.cool')

def test_cycleinmethods():
    with pytest.raises(Exception):
        compile('resources/semantic/input/cycleinmethods.cool')

def test_dispatch():
    with pytest.raises(Exception):
        compile('resources/semantic/input/dispatch.cool')

def test_expressionblock():
    with pytest.raises(Exception):
        compile('resources/semantic/input/expressionblock.cool')

def test_forwardinherits():
    with pytest.raises(Exception):
        compile('resources/semantic/input/forwardinherits.cool')


def test_hairyscary():
    with pytest.raises(Exception):
        compile('resources/semantic/input/hairyscary.cool')

def test_if():
    with pytest.raises(Exception):
        compile('resources/semantic/input/if.cool')

def test_inheritsObject():
    with pytest.raises(Exception):
        compile('resources/semantic/input/inheritsObject.cool')

def test_initwithself():
    with pytest.raises(Exception):
        compile('resources/semantic/input/initwithself.cool')


def test_io():
    with pytest.raises(Exception):
        compile('resources/semantic/input/io.cool')


def test_isvoid():
    with pytest.raises(Exception):
        compile('resources/semantic/input/isvoid.cool')

def test_letinit():
    with pytest.raises(Exception):
        compile('resources/semantic/input/letinit.cool')

###
'''letnoinit.cool
letselftype.cool
letshadows.cool
list.cool
methodcallsitself.cool
methodnameclash.cool
neg.cool
newselftype.cool
objectdispatchabort.cool
overriderenamearg.cool
overridingmethod.cool
overridingmethod2.cool
overridingmethod3.cool
scopes.cool
simplearith.cool
simplecase.cool
staticdispatch.cool
stringtest.cool
subtypemethodreturn.cool
trickyatdispatch.cool'''

