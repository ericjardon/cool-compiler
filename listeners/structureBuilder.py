from copy import deepcopy
from pprint import pprint
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

from util.exceptions import dupformals, missingclass, redefinedclass, selftypebadreturn, attroverride
from util.structure import *
from util.structure import _allClasses as classDict
from antlr4.tree.Tree import ParseTree
# Expression node's can store a .dataType attribute for their "runtime evaluation" type. This is compared to the stated type.

class structureBuilder(coolListener):
    '''
    Responsible for populating the _allClasses global dictionary,
    building the class inheritance tree.
    Excludes definitions of attributes and methods.
    We do this before we begin defining methods and attributes
    '''

    basicTypes = set(['Int','String','Bool'])

    def __init__(self) -> None:
        classDict.clear()
        self.deferredInherits = {}  # maps class name to parent class name
        setBaseKlasses() 

    def getDefinedClasses():
        return deepcopy(classDict)
    
    def enterKlass(self, ctx: coolParser.KlassContext):
       
        name = ctx.TYPE(0).getText()

        if name in classDict:
            raise redefinedclass()

        inheritance = None

        if (ctx.TYPE(1)):
            inheritance = ctx.TYPE(1).getText()
            self.deferredInherits[name] = inheritance
            k = Klass(name=name)
            # Defer checking parent class existence
            # So we can define child classes before parent ones in the source code

        else:            
            k = Klass(name=name)

        ctx.activeClass = k
        for feature in ctx.feature():  # children nodes should know the class to add to
            feature.activeClass = k


    def exitProgram(self, ctx:coolParser.ProgramContext):
        # Check that all parent classes are defined
        for child, parent in self.deferredInherits.items():
            try:
                lookupClass(parent)

            except KeyError as e:
                raise missingclass("Undefined parent class", parent)

            childKlass = lookupClass(child)            
            childKlass.setInherits(parent)