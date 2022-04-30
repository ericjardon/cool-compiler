from copy import deepcopy
from ctypes import util
from pprint import pprint
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

from util.exceptions import assignnoconform, badarith, baddispatch, badwhilebody, badwhilecond, caseidenticalbranch, dupformals, missingclass, outofscope, redefinedclass, returntypenoexist, selftypebadreturn, badequalitytest, badequalitytest2
from util.structure import *
from util.structure import _allClasses as classDict
from antlr4.tree.Tree import ParseTree
# Expression node's can store a .dataType attribute for their "runtime evaluation" type. This is compared to the stated type.

valid_self_type_returns = ["SELF_TYPE", "self"]

def getActiveClass(ctx: ParseTree) -> Klass:
    p = ctx.parentCtx
    while (p and not hasattr(p, 'activeClass')):
        p = p.parentCtx
    
    return p.activeClass

class structureBuilder(coolListener):
    '''
    Responsible for adding all classes to the _allClasses global dictionary,
    including definitions of attributes and methods.
    We do this before we begin type-checking
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
            print("Name exists:", name)
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
    
    def enterFeature_function(self, ctx: coolParser.Feature_functionContext):
        '''
        Adds the method to the current active Klass instance
        and performs self_type return checks
        '''
        name = ctx.ID().getText()
        parameters = []
        names = []

        for param in ctx.params:
            if param.ID().getText() in names:
                raise dupformals()
            names.append(param.ID().getText())
            parameters.append((param.ID().getText(), param.TYPE().getText()))
        
        return_type = ctx.TYPE().getText()

        if (return_type == "SELF_TYPE"):
            # Check that class conforms to this class
            checkClass = ctx.expr().TYPE().getText()
            if checkClass not in valid_self_type_returns:
                raise selftypebadreturn()

        if len(parameters) == 0 :
            newMethod = Method(return_type)
        else:
            newMethod = Method(return_type, parameters)
        
        ctx.activeClass.addMethod(name, newMethod)

        # Next listener ``typeChecker is who inserts parameter bindings to a new, extended scope.
        

    def exitProgram(self, ctx:coolParser.ProgramContext):
        # Check that all parent classes are defined
        for child, parent in self.deferredInherits.items():
            try:
                lookupClass(parent)

            except KeyError as e:
                print("undefined parent class", e)
                raise missingclass("Undefined parent class", parent)

            childKlass = lookupClass(child)            
            childKlass.setInherits(parent)