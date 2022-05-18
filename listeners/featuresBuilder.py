from copy import deepcopy
from pprint import pprint
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

from util.exceptions import dupformals, missingclass, redefinedclass, selftypebadreturn, attroverride
from util.structure import *
from util.structure import _allClasses as classDict
from antlr4.tree.Tree import ParseTree

def getActiveClass(ctx: ParseTree) -> Klass:
    p = ctx.parentCtx
    while (p and not hasattr(p, 'activeClass')):
        p = p.parentCtx
    
    return p.activeClass

valid_self_type_returns = ["SELF_TYPE", "self"]


class featuresBuilder(coolListener):
    '''
    Responsible for adding attributes and methods to classes
    and throwing exceptions for illegal overrides.
    We do this before we begin type-checking
    '''
    def enterKlass(self, ctx: coolParser.KlassContext):
        k = classDict[ctx.TYPE(0).getText()]
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
            try:
                checkClass = ctx.expr().TYPE().getText()
                if checkClass not in valid_self_type_returns:
                    raise selftypebadreturn()
            except AttributeError:
                pass

        if len(parameters) == 0 :
            newMethod = Method(return_type)
        else:
            newMethod = Method(return_type, parameters)
        
        ctx.activeClass.addMethod(name, newMethod)

        # Next listener ``typeChecker is who inserts parameter bindings to a new, extended scope.


    def enterFeature_attribute(self, ctx: coolParser.Feature_attributeContext):
        # Add attribute
        name = ctx.ID().getText()
        type = ctx.TYPE().getText()
        # If attr exists, raise attroverride
        try:
            ctx.activeClass.lookupAttribute(name)
            raise attroverride()
        except KeyError:
            ctx.activeClass.addAttribute(name, type)