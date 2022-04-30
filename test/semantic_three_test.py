import pytest

from main import dummy
from main import compile
from util.exceptions import *

def test_assignnoconform():
     with pytest.raises(assignnoconform):
         compile('resources/semantic/input/assignnoconform.cool')

def test_attrbadinit():
     with pytest.raises(attrbadinit):
         compile('resources/semantic/input/attrbadinit.cool')

def test_attroverride():
    with pytest.raises(attroverride):
        compile('resources/semantic/input/attroverride.cool')

def test_badargs1():
    with pytest.raises(badargs1):
        compile('resources/semantic/input/badargs1.cool')

def test_badmethodcallsitself():
    with pytest.raises(badmethodcallsitself):
        compile('resources/semantic/input/badmethodcallsitself.cool')

def test_badstaticdispatch():
    with pytest.raises(badstaticdispatch):
        compile('resources/semantic/input/badstaticdispatch.cool')

def test_dupformals():
    with pytest.raises(dupformals):
        compile('resources/semantic/input/dupformals.cool')

def test_letbadinit():
    with pytest.raises(letbadinit):
        compile('resources/semantic/input/letbadinit.cool')

def test_lubtest():
    with pytest.raises(lubtest):
        compile('resources/semantic/input/lubtest.cool')

def test_overridingmethod4():
    with pytest.raises(overridingmethod4):
        compile('resources/semantic/input/overridingmethod4.cool')

def test_signaturechange():
    with pytest.raises(signaturechange):
        compile('resources/semantic/input/signaturechange.cool')

def test_trickyatdispatch2():
    with pytest.raises(trickyatdispatch2):
        compile('resources/semantic/input/trickyatdispatch2.cool')