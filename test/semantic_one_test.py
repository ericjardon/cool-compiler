import pytest

from main import dummy
from main import compile
from util.exceptions import *

def test_dummy():
    with pytest.raises(SystemExit):
        dummy()

def test_anattributenamedself():
    with pytest.raises(anattributenamedself):
        compile('resources/semantic/input/anattributenamedself.cool')

def test_badredefineint():
    with pytest.raises(badredefineint):
        compile('resources/semantic/input/badredefineint.cool')

def test_inheritsbool():
    with pytest.raises(inheritsbool):
        compile('resources/semantic/input/inheritsbool.cool')

def test_inheritsselftype():
    with pytest.raises(inheritsselftype):
        compile('resources/semantic/input/inheritsselftype.cool')

def test_inheritsstring():
    with pytest.raises(inheritsstring):
        compile('resources/semantic/input/inheritsstring.cool')

def test_letself():
    with pytest.raises(letself):
        compile('resources/semantic/input/letself.cool')

def test_nomain():
    with pytest.raises(nomain):
        compile('resources/semantic/input/nomain.cool')

def test_redefinedobject():
    with pytest.raises(redefinedobject):
        compile('resources/semantic/input/redefinedobject.cool')

def test_selfassignment():
    with pytest.raises(selfassignment):
        compile('resources/semantic/input/self-assignment.cool')

def test_selfinformalparameter():
    with pytest.raises(selfinformalparameter):
        compile('resources/semantic/input/selfinformalparameter.cool')

def test_selftypeparameterposition():
    with pytest.raises(selftypeparameterposition):
        compile('resources/semantic/input/selftypeparameterposition.cool')

def test_selftyperedeclared():
    with pytest.raises(selftyperedeclared):
        compile('resources/semantic/input/selftyperedeclared.cool')

