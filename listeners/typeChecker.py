from typing import Tuple, List
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

from util.exceptions import assignnoconform, attrbadinit, attroverride, badargs1, badarith, baddispatch, badwhilebody, badwhilecond, caseidenticalbranch, dupformals, letbadinit, missingclass, outofscope, redefinedclass, returntypenoexist, selftypebadreturn, badequalitytest, badequalitytest2, trickyatdispatch2
from util.structure import *
from antlr4.tree.Tree import ParseTree
from util.structure import _allClasses as classDict

# Expression node's can store a .dataType attribute for their "runtime evaluation" type. This is compared to the stated type.

def getCurrentScope(ctx: ParseTree) -> Tuple[SymbolTableWithScopes, Klass]:
    p = ctx.parentCtx
    while (p and not hasattr(p, 'objectEnv') and not hasattr(p, 'activeClass')):
        p = p.parentCtx
    
    return p.objectEnv, p.activeClass


class typeChecker(coolListener):
    '''
    This listener should be instantiated AFTER structureBuilder.
    It assumes all classes in the program are in the classDict dictionary.
    '''

    basicTypes = set(['Int','String','Bool'])

    def checkArgsParams(self, args: List[coolParser.ExprContext], method: Method, methodName:str):
        if len(args) != len(method.params):
            raise Exception(f"Bad call to {methodName}: {len(args)} arguments provided, {len(method.params)} expected")

        # Check arguments against their type
        param_names = list(method.params)
        for i, arg in enumerate(args):
            if lookupClass(arg.dataType).conformsTo(lookupClass(method.params[param_names[i]])):
                continue
            else:
                raise badargs1(f"Incorrect argument {arg.getText()} for parameter {param_names[i]}")

    def __init__(self) -> None:
        print("Classes of Program")
        print(list(classDict.keys()))
        
    def enterKlass(self, ctx: coolParser.KlassContext):
       
        name = ctx.TYPE(0).getText()
        k = lookupClass(name)

        objectEnv = SymbolTableWithScopes(k)  # Object environment in a class

        for feature in ctx.feature():  # children nodes should know the class and Object environment
            feature.activeClass = k
            feature.objectEnv = objectEnv

    def enterFeature_function(self, ctx: coolParser.Feature_functionContext):
        name = ctx.ID().getText()
        method = ctx.activeClass.lookupMethod(name)

        if (method.type != "SELF_TYPE"):
            try:
                lookupClass(method.type)
            except KeyError:
                raise returntypenoexist()

        parameters = list(method.params.items())
        print(f"METHOD {name}({parameters})")

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
        # Look up the atribute in the class hierarchy, if it is found, raise attroverride, otherwise add it to current active class
        try:
            ctx.activeClass.lookupAttribute(name)
            raise attroverride()
        except KeyError:
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

    def exitPrimary(self, ctx:coolParser.PrimaryContext):
        if ctx.INTEGER():
            ctx.dataType = 'Int'
        elif ctx.STRING():
            ctx.dataType = 'String'
        elif ctx.TRUE() or ctx.FALSE():
            ctx.dataType = 'Bool'
        elif ctx.ID():  # is a variable name, assign type from scope
            objectEnv, activeClass = getCurrentScope(ctx)
            # Check self keyword
            if ctx.ID().getText() == 'self':
                ctx.dataType = activeClass.name
                return
            # Look for variable in parent classes, if it doesn't exist, raise attrbadinit
            try:
                name = ctx.ID().getText()
                activeClass.lookupAttribute(name)
            except KeyError:
                raise attrbadinit()
            # Look for variable in this scope, if it doesn't exist, raise out of scope exception
            try :
                ctx.dataType = objectEnv[ctx.ID().getText()]
            except KeyError:
                raise outofscope()
        else:
            # is a subexpression, implement type checking for generic expressions
            print("subexpression <",ctx.expr().getText(),">")
            ctx.dataType = ctx.expr().dataType


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
        
        print("caller: <",caller,">")
        methodName = ctx.ID().getText()
        print("method name:", methodName)
        try:
            method = k.lookupMethod(methodName)
            # then compare formal params
        except KeyError:
            if caller == 'Int':
                raise badwhilebody()
            else: 
                raise baddispatch(f"{caller} object does not have method '{methodName}'")
        
        self.checkArgsParams(args=ctx.params, method=method, methodName=methodName)

    def exitStatic_dispatch(self, ctx:coolParser.Static_dispatchContext):
        caller = ctx.getChild(0).dataType 
        k = lookupClass(caller)
        
        print("caller: <",caller,">")
        methodName = ctx.ID().getText()
        print("method name:", methodName)

        if ctx.TYPE():
            # check if conforms to parent type after @
            parent = lookupClass(ctx.TYPE().getText())
            if not lookupClass(caller).conformsTo(parent):
                raise trickyatdispatch2()

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
        identifier = ctx.ID().getText()
        declaredType = ctx.TYPE().getText()
        objectEnv[identifier] = declaredType

    def exitLet_decl(self, ctx:coolParser.Let_declContext):
        declaredType = ctx.TYPE().getText()
        if ctx.expr():  # has initialization
            try:
                dataType = ctx.expr().dataType
                if not lookupClass(dataType).conformsTo(lookupClass(declaredType)):
                    raise letbadinit(f"Provided {dataType} does not conform to {declaredType}")

            except AttributeError:
                print(f"{ctx.expr().getText()} expression has no dataType") 


    def enterNew(self, ctx:coolParser.NewContext):
        # Store the TYPE and return it to parent
        ctx.dataType = ctx.TYPE().getText()

    def exitAssignment(self, ctx:coolParser.AssignmentContext):
        # receive the dataType from the child node
        objectEnv, _ = getCurrentScope(ctx)
        id = ctx.ID().getText()
        leftSide = objectEnv[id]
        rightSide = ctx.expr().dataType

        try:
            rightKlass = lookupClass(rightSide)
            leftKlass = lookupClass(leftSide)
        except Exception as e:
            missing = []
            existing = classDict.keys()
            if rightSide not in existing:
                missing += [rightSide]
            if leftSide not in existing:
                missing += [leftSide]
            msg = ','.join(missing)
            raise missingclass(msg)

        # rightSide must conform to leftSide        
        if not rightKlass.conformsTo(leftKlass):
            raise assignnoconform
