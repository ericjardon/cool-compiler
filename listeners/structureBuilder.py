from ctypes import util
from pprint import pprint
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
<<<<<<< HEAD
from util.exceptions import badarith, baddispatch, badwhilebody, badwhilecond, caseidenticalbranch, dupformals, missingclass, outofscope, redefinedclass, returntypenoexist, selftypebadreturn, badequalitytest, badequalitytest2
=======
from util.exceptions import assignnoconform, badarith, baddispatch, badwhilebody, badwhilecond, caseidenticalbranch, missingclass, outofscope, redefinedclass, returntypenoexist, selftypebadreturn, badequalitytest, badequalitytest2
>>>>>>> 9429bab97c63920941f15d677d824f7dc23f313d
from util.structure import *
from util.structure import _allClasses as classDict
from antlr4.tree.Tree import ParseTree
# Expression node's can store a .dataType attribute for their "runtime evaluation" type. This is compared to the stated type.

def getCurrentScope(ctx: ParseTree) -> SymbolTableWithScopes:
    p = ctx.parentCtx
    while (p and not hasattr(p, 'objectEnv') and not hasattr(p, 'activeClass')):
        p = p.parentCtx
    
    return p.objectEnv, p.activeClass

valid_self_type_returns = ["SELF_TYPE", "self"]

class structureBuilder(coolListener):


    
    objectClass = Klass("Object", None)
    setBaseKlasses()

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
        names = []

        for param in ctx.params:
            if param.ID().getText() in names:
                raise dupformals()
            names.append(param.ID().getText())
            parameters.append((param.ID().getText(), param.TYPE().getText()))
        
        return_type = ctx.TYPE().getText()

        if (return_type == "SELF_TYPE"):
            checkClass = ctx.expr().TYPE().getText()
            if checkClass not in valid_self_type_returns:
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
        ctx.activeClass.addAttribute(name, type)  # we can call lookupAttribute later


    def enterCase_expr(self, ctx: coolParser.Case_exprContext):
        cases = ctx.case_stat()
        present_types = []

        for case in cases:
            case_type = case.TYPE().getText()
            if case_type in present_types:
                raise caseidenticalbranch()
            present_types.append(case_type)

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

            # Look for variable in this scope, if it doesn't exist, raise out of scope exception
            try :
                ctx.dataType = objectEnv[ctx.ID().getText()]
            except KeyError:
                raise outofscope()
            

        else:
            # is a subexpression, implement type checking for generic expressions
            pass

    def exitEquals(self, ctx: coolParser.EqualsContext):
        typeOne = ctx.children[0].dataType
        typeTwo = ctx.children[2].dataType

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
                raise baddispatch(f"{caller} object does not have method '{methodName}'")

    def exitAddition(self, ctx: coolParser.AdditionContext):
        left_type = ctx.expr(0).dataType
        right_type = ctx.expr(1).dataType

        if left_type != "Int" or right_type != "Int":
            raise badarith()

    def exitSubtraction(self, ctx: coolParser.SubtractionContext):
        left_type = ctx.expr(0).dataType
        right_type = ctx.expr(1).dataType

        if left_type != "Int" or right_type != "Int":
            raise badarith()
    
    def exitDivision(self, ctx: coolParser.DivisionContext):
        left_type = ctx.expr(0).dataType
        right_type = ctx.expr(1).dataType

        if left_type != "Int" or right_type != "Int":
            raise badarith()
    
    def exitMultiplication(self, ctx: coolParser.MultiplicationContext):
        left_type = ctx.expr(0).dataType
        right_type = ctx.expr(1).dataType

        if left_type != "Int" or right_type != "Int":
            raise badarith()

    def exitWhile(self, ctx:coolParser.WhileContext):
        # all subexpressions of while have been evaluated.

        # check that condition evaluates to a boolean
        predicate = ctx.expr()[0]
        if predicate.dataType != 'Bool':
            raise badwhilecond("While predicate must evaluate to a Bool value")
        
    def enterLet_expr(self, ctx:coolParser.Let_exprContext):
        # Parent node to Let_decl
        object_env, active_class = getCurrentScope(ctx)
        object_env.openScope()
        body = ctx.expr()

    def exitLet_expr(self, ctx: coolParser.Let_exprContext):
        object_env, active_class = getCurrentScope(ctx)
        object_env.closeScope()

    def enterLet_decl(self, ctx:coolParser.Let_declContext):
        # Store the variable in current Scope
        objectEnv, activeClass = getCurrentScope(ctx)
        objectEnv[ctx.ID().getText()] = ctx.TYPE().getText()

<<<<<<< HEAD
     
=======


    def enterNew(self, ctx:coolParser.NewContext):
        # Store the TYPE and return it to parent
        ctx.dataType == ctx.TYPE()

    def exitAssignment(self, ctx:coolParser.AssignmentContext):
        # receive the dataType from the child node
        value = ctx.expr().dataType
        variable = ctx.ID().getText()

        # value tiene que ser un hijo o una instancia de value,
        # es decir, value must conform to variable
        try:
            lookupClass(value).conformsTo(lookupClass(variable))
        except:
            raise assignnoconform()
>>>>>>> 9429bab97c63920941f15d677d824f7dc23f313d
