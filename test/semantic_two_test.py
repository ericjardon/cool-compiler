import pytest

from main import dummy
from main import compile
from util.exceptions import *

def test_badarith():
    with pytest.raises(badarith):
        compile('resources/semantic/input/badarith.cool')

def test_baddispatch():
    with pytest.raises(baddispatch):
        compile('resources/semantic/input/baddispatch.cool')

def test_badequalitytest():
    with pytest.raises(badequalitytest):
        compile('resources/semantic/input/badequalitytest.cool')

def test_badequalitytest2():
    with pytest.raises(badequalitytest2):
        compile('resources/semantic/input/badequalitytest2.cool')

def test_badwhilebody():
    with pytest.raises(badwhilebody):
        compile('resources/semantic/input/badwhilebody.cool')

def test_badwhilecond():
    with pytest.raises(badwhilecond):
        compile('resources/semantic/input/badwhilecond.cool')

def test_caseidenticalbranch():
    with pytest.raises(caseidenticalbranch):
        compile('resources/semantic/input/caseidenticalbranch.cool')

def test_missingclass():
    with pytest.raises(missingclass):
        compile('resources/semantic/input/missingclass.cool')

def test_outofscope():
    with pytest.raises(outofscope):
        compile('resources/semantic/input/outofscope.cool')

def test_redefinedclass():
    with pytest.raises(redefinedclass):
        compile('resources/semantic/input/redefinedclass.cool')

def test_returntypenoexist():
    with pytest.raises(returntypenoexist):
        compile('resources/semantic/input/returntypenoexist.cool')

def test_selftypebadreturn():
    with pytest.raises(selftypebadreturn):
        compile('resources/semantic/input/selftypebadreturn.cool')