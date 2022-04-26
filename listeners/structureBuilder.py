from ctypes import util
from pprint import pprint
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.exceptions import badwhilebody, badwhilecond, missingclass, redefinedclass, returntypenoexist, selftypebadreturn, badequalitytest, badequalitytest2
from util.structure import *
from util.structure import _allClasses as classDict
from antlr4.tree.Tree import ParseTree
# Expression node's can store a .dataType attribute for their "runtime evaluation" type. This is compared to the stated type.

def getCurrentScope(ctx: ParseTree) -> SymbolTableWithScopes:
    p = ctx.parentCtx
    while (p and not hasattr(p, 'objectEnv') and not hasattr(p, 'activeClass')):
        p = p.parentCtx
    
    return p.objectEnv, p.activeClass

class structureBuilder(coolListener):

    basicTypes = set(['Int','String','Bool'])

    def __init__(self) -> None:
        classDict.clear()          
        Klass("Object", None)
        setBaseKlasses()  # Int, Bool, String, IO
    
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

        objectEnv = SymbolTableWithScopes(k)  # Object environment in a class

        for feature in ctx.feature():  # children nodes should know the class and Object environment
            feature.activeClass = k
            feature.objectEnv = objectEnv


    def enterFeature_function(self, ctx: coolParser.Feature_functionContext):
        name = ctx.ID().getText()

        parameters = []

        for param in ctx.params:
            parameters.append((param.ID().getText(), param.TYPE().getText()))
        
        return_type = ctx.TYPE().getText()

        if (return_type == "SELF_TYPE"):
            checkClass = ctx.expr().TYPE().getText()
            if checkClass != "SELF_TYPE":
                raise selftypebadreturn()

        if (return_type != "SELF_TYPE"):
            try:
                lookupClass(return_type)
            except KeyError:
            
                raise returntypenoexist()

        if len(parameters) == 0 :
            newMethod = Method(return_type)
        else:
            newMethod = Method(return_type, parameters)
        
        ctx.activeClass.addMethod(name, newMethod)

        # Add parameter type bindings in the object scope
        ctx.objectEnv.openScope()
        for id, type in parameters:
            ctx.objectEnv[id] = type

        body = ctx.expr()
        print("Body of method <", body.getText(),'>')
        body.objectEnv = ctx.objectEnv
        body.activeClass = ctx.activeClass

    def exitFeature_function(self, ctx:coolParser.Feature_functionContext):
        ctx.objectEnv.closeScope() # remove parameter bindings on exit


    def enterFeature_attribute(self, ctx: coolParser.Feature_attributeContext):
        name = ctx.ID().getText()
        type = ctx.TYPE().getText()
        ctx.activeClass.addAttribute(name, type)

    def exitPrimary_expr(self, ctx:coolParser.Primary_exprContext):
         # Has a single Primary child node. fetch its dataType and pass on to parent
        primary = ctx.getChild(0)
        try:
            ctx.dataType = primary.dataType
        except AttributeError:
            print(primary.__dict__)
            print(f"Primary expression {ctx.getText()} has no datatype")

    
    def enterPrimary(self, ctx: coolParser.PrimaryContext):
        if ctx.INTEGER():
            ctx.dataType = 'Int'
        elif ctx.STRING():
            ctx.dataType = 'String'
        elif ctx.TRUE() or ctx.FALSE():
            ctx.dataType = 'Bool'
        elif ctx.ID():  # is a variable name, assign type from scope
            objectEnv, activeClass = getCurrentScope(ctx)
            
            # print(f"primary expr !! {ctx.ID()} in class:", activeClass.name)
            # print("var bindings here:")
            # pprint(objectEnv)
            ctx.dataType = objectEnv[ctx.ID().getText()]
            print('ID datatype', ctx.dataType)

        else:
            # is a subexpression, implement type checking for generic expressions
            pass

    def exitEquals(self, ctx: coolParser.EqualsContext):
        typeOne = ctx.children[0].dataType
        typeTwo = ctx.children[2].dataType
        print("Types to compare", typeOne, typeTwo)

        if typeOne in self.basicTypes and typeTwo in self.basicTypes:
            if typeOne != typeTwo:
                if typeOne == "Int" and typeTwo == "String":
                    raise badequalitytest()
                if typeOne == "Int" and typeTwo == "Bool":
                    raise badequalitytest2()
                else:
                    raise badequalitytest()  # any type discrepancy should throw error
    
    def exitDispatch(self, ctx:coolParser.DispatchContext):
        # Check validity of the dispatch: method must be defined, types must conform
        caller = ctx.getChild(0).dataType # get type of calling expression
        k = lookupClass(caller)
        
        print("calling object <",caller,">")
        methodName = ctx.ID().getText()
        print("method name", methodName)
        try:
            method = k.lookupMethod(methodName)
            # then compare formal params
        except KeyError:
            if caller == 'Int':
                raise badwhilebody()
            else: 
                raise Exception(f"{caller} object does not have a method {methodName}")

    
    def exitWhile(self, ctx:coolParser.WhileContext):
        # all subexpressions of while have been evaluated.

        # check that condition evaluates to a boolean
        predicate = ctx.expr()[0]
        if predicate.dataType != 'Bool':
            raise badwhilecond("While predicate must evaluate to a Bool value")
        






