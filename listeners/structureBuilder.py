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
            try:
                inherit = lookupClass(inheritance)
                k = Klass(name, inherit.name)
            except KeyError as error:
                raise missingclass()

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

        # Job of typeChecker now:
        # Add parameter type bindings in the object scope
        # ctx.objectEnv.openScope()
        # for id, type in parameters:
        #     ctx.objectEnv[id] = type

        # body = ctx.expr()
        # print("Body of method <", body.getText(),'>')
        # body.objectEnv = ctx.objectEnv
        # body.activeClass = ctx.activeClass