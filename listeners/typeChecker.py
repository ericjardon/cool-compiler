from cgitb import lookup
from subprocess import call
from typing import Tuple, List
from antlr4.tree.Tree import ParseTree
from pytest import param
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.exceptions import *
from util.structure import *
from util.structure import _allClasses as classDict

# Expression node's can store a .dataType attribute for their "runtime evaluation" type. This is compared to the stated type.

def getKlass(name:str, ctx: ParseTree) -> Klass:
    if name == "SELF_TYPE":
        _, activeClass = getCurrentScope(ctx)
        return activeClass
    else:
        return lookupClass(name)

def getCurrentScope(ctx: ParseTree) -> Tuple[SymbolTableWithScopes, Klass]:
    p = ctx.parentCtx
    while p and not hasattr(p, "objectEnv") and not hasattr(p, "activeClass"):
        p = p.parentCtx
    return p.objectEnv, p.activeClass

def equalMethodParamTypes(params1: SymbolTable, params2: SymbolTable):
    # Assumed both are equal length. Check if return types are equal
    for argname1, argname2 in zip(params1.keys(), params2.keys()):
        if params1[argname1] != params2[argname2]:
            return False
    return True

class typeChecker(coolListener):
    """
    This listener should be instantiated AFTER structureBuilder.
    It assumes all classes in the program are in the classDict dictionary.
    """

    basicTypes = set(["Int", "String", "Bool"])

    def checkArgsParams(
        self, ctx: ParseTree, method: Method, methodName: str
    ):
        args = ctx.params # List[coolParser.ExprContext]
        if len(args) != len(method.params):
            raise Exception(
                f"Bad call to {methodName}: {len(args)} arguments provided, {len(method.params)} expected"
            )

        # Check arguments against their type
        param_names = list(method.params)
        for i, arg in enumerate(args):
            if getKlass(arg.dataType, ctx).conformsTo(
                getKlass(method.params[param_names[i]], ctx)
            ):
                continue
            else:
                raise badargs1(
                    f"Incorrect argument {arg.getText()} for parameter {param_names[i]}"
                )

    def __init__(self) -> None:
        print("Classes of Program")
        print(list(classDict.keys()))

    def enterKlass(self, ctx: coolParser.KlassContext):
        name = ctx.TYPE(0).getText()
        k = lookupClass(name)
        objectEnv = SymbolTableWithScopes(k)  # Object environment in a class

        for (
            feature
        ) in (
            ctx.feature()
        ):  # children nodes should know the class and Object environment
            feature.activeClass = k
            feature.objectEnv = objectEnv

    def enterFeature_function(self, ctx: coolParser.Feature_functionContext):
        name = ctx.ID().getText()
        method = ctx.activeClass.lookupMethod(name)
        parentClass = lookupClass(ctx.activeClass.inherits)
        if parentClass.name != "Object":
            try:
                parentMethod = parentClass.lookupMethod(name)
                if len(parentMethod.params) != len(method.params) \
                    or parentMethod.type != method.type:
                    raise signaturechange()
                # Param names can be overriden
                if not equalMethodParamTypes(parentMethod.params, method.params):
                    raise overridingmethod4()
            except KeyError:
                pass

        if method.type != "SELF_TYPE":
            try:
                lookupClass(method.type)
            except KeyError:
                raise returntypenoexist()

        parameters = list(method.params.items())

        # Add parameter type bindings in the object scope
        ctx.objectEnv.openScope()
        for id, type in parameters:
            ctx.objectEnv[id] = type

        body = ctx.expr()
        body.objectEnv = ctx.objectEnv
        body.activeClass = ctx.activeClass

    def exitFeature_function(self, ctx: coolParser.Feature_functionContext):
        ctx.objectEnv.closeScope()  # remove parameter bindings on exit
        try:
            expression_type = getKlass(ctx.expr().dataType, ctx)
            
            returnTypeName = ctx.TYPE().getText()
            if returnTypeName == 'SELF_TYPE':
                return_type = ctx.activeClass
            else: 
                return_type = lookupClass(ctx.TYPE().getText())

            if not expression_type.conformsTo(return_type):
                raise lubtest("Expression type: ", expression_type.name, "must conform to return type: ", return_type.name)
        except AttributeError:
            pass

    def enterFeature_attribute(self, ctx: coolParser.Feature_attributeContext):

        # Type checking
        if ctx.expr():
            try: 
                subexpr = ctx.expr().primary()
                if subexpr.ID():  # assigning a primary
                    if subexpr.ID().getText() == 'self':
                        # check conforms to static type
                        _, activeClass = getCurrentScope(ctx)
                        static_type = lookupClass(ctx.TYPE().getText())
                        if not activeClass.conformsTo(static_type):
                            raise attrbadinit(f"'self' does not conform to stated type: {static_type.name}")
                        return
                    try:
                        ctx.objectEnv[subexpr.getText()]
                    except KeyError as e:
                        print(e)
                        raise attrbadinit(e.__repr__())
                else:
                    # Is a literal value
                    pass
            except AttributeError:
                # Solve expression 
                print(type(ctx.expr()))
                pass

                

    def enterCase_expr(self, ctx: coolParser.Case_exprContext):
        cases = ctx.case_stat()
        present_types = []

        for case in cases:
            case_type = case.TYPE().getText()
            if case_type in present_types:
                raise caseidenticalbranch()
            present_types.append(case_type)
        # The type is the join of the types of its branches. 
        # All present_types should be distinct
        lca = getLCA(present_types)
        ctx.dataType = lca.name
        

    def exitPrimary_expr(self, ctx: coolParser.Primary_exprContext):
        # Has a single Primary child node. fetch its dataType and pass on to parent
        primary = ctx.getChild(0)
        try:
            ctx.dataType = primary.dataType
        except AttributeError:
            print(f"Primary expression {ctx.getText()} has no datatype")

    def exitPrimary(self, ctx: coolParser.PrimaryContext):
        if ctx.INTEGER():
            ctx.dataType = "Int"
        elif ctx.STRING():
            ctx.dataType = "String"
        elif ctx.TRUE() or ctx.FALSE():
            ctx.dataType = "Bool"
        elif ctx.ID():  # is a variable name, assign type from scope
            object_env, active_class = getCurrentScope(ctx)
            identifier = ctx.ID().getText()
            # Check self keyword
            if identifier == "self":
                ctx.dataType = active_class.name
                return
            # Look for variable in this scope, if it doesn't exist, raise out of scope exception
            try:
                # try object scope
                ctx.dataType = object_env[identifier]
            except KeyError:
                # try class scope
                try: 
                    ctx.dataType = active_class.lookupAttribute(identifier)
                except KeyError as e:
                    print(e)
                    raise outofscope(f"Variable '{identifier}' is out of scope")
        else:
            # is a subexpression, implement type checking for generic expressions
            ctx.dataType = ctx.expr().dataType

    def exitEquals(self, ctx: coolParser.EqualsContext):
        type_one = ctx.children[0].dataType
        type_two = ctx.children[2].dataType

        if type_one in self.basicTypes and type_two in self.basicTypes:
            if type_one != type_two:
                if type_one == "Int" and type_two == "String":
                    raise badequalitytest()
                if type_one == "Int" and type_two == "Bool":
                    raise badequalitytest2()
                else:
                    raise badequalitytest()  # any type discrepancy should throw error
        ctx.dataType = 'Bool'

    def exitDispatch(self, ctx: coolParser.DispatchContext):
        # Check validity of the dispatch: method must be defined, types must conform
        caller = ctx.getChild(0).dataType  # get type of calling expression
        k = lookupClass(caller)

        method_name = ctx.ID().getText()
        try:
            method = k.lookupMethod(method_name)
            # then compare formal params
        except KeyError:
            if caller == "Int":
                raise badwhilebody()
            else:
                raise baddispatch(
                    f"{caller} object does not have method '{method_name}'"
                )
        self.checkArgsParams(ctx=ctx, method=method, methodName=method_name)
        # Return type, enforce SELF_TYPE rules
        if method.type == 'SELF_TYPE' :
            ctx.dataType = k.name # class of caller
        else:
            ctx.dataType = method.type

    def enterMethod_call(self, ctx: coolParser.Method_callContext):
        object_env, active_class = getCurrentScope(ctx)
        method_name = ctx.ID().getText()
        method = active_class.lookupMethod(method_name)
        ctx.dataType = method.type

    def exitMethod_call(self, ctx: coolParser.Method_callContext):
        object_env, active_class = getCurrentScope(ctx)
        methond_name = ctx.ID().getText()
        method = active_class.lookupMethod(methond_name)
       
        try:
            self.checkArgsParams(ctx, method=method, methodName=methond_name)
        except badargs1:
            raise badmethodcallsitself()

    def exitStatic_dispatch(self, ctx: coolParser.Static_dispatchContext):
        caller = ctx.getChild(0).dataType
        k = lookupClass(caller)

        methodName = ctx.ID().getText()

        if ctx.TYPE():
            # check if conforms to parent type after @
            parent = lookupClass(ctx.TYPE().getText())
            caller_class = lookupClass(caller)
            if not caller_class.conformsTo(parent) :
                if parent.conformsTo(caller_class):
                    raise badstaticdispatch()
                raise trickyatdispatch2() 

        try:
            method = k.lookupMethod(methodName)
            ctx.dataType = method.type
            # then compare formal params
        except KeyError:
            if caller == "Int":
                raise badwhilebody()
            else:
                raise baddispatch(
                    f"{caller} object does not have method '{methodName}'"
                )

        # Return type, enforce SELF_TYPE rules
        if method.type == 'SELF_TYPE' :
            ctx.dataType = k.name # class of caller
        else:
            ctx.dataType = method.type  

    def exitAddition(self, ctx: coolParser.AdditionContext):
        left_type = ctx.expr(0).dataType
        right_type = ctx.expr(1).dataType

        if left_type != "Int" or right_type != "Int":
            raise badarith()
        ctx.dataType = 'Int'

    def exitSubtraction(self, ctx: coolParser.SubtractionContext):
        left_type = ctx.expr(0).dataType
        right_type = ctx.expr(1).dataType

        if left_type != "Int" or right_type != "Int":
            raise badarith()

        ctx.dataType = 'Int'

    def exitDivision(self, ctx: coolParser.DivisionContext):
        left_type = ctx.expr(0).dataType
        right_type = ctx.expr(1).dataType

        if left_type != "Int" or right_type != "Int":
            raise badarith()
        ctx.dataType = 'Int'

    def exitMultiplication(self, ctx: coolParser.MultiplicationContext):
        left_type = ctx.expr(0).dataType
        right_type = ctx.expr(1).dataType

        if left_type != "Int" or right_type != "Int":
            raise badarith()
        
        ctx.dataType = 'Int'

    def exitWhile(self, ctx: coolParser.WhileContext):
        # all subexpressions of while have been evaluated.

        # check that condition evaluates to a boolean
        predicate = ctx.expr()[0]
        if predicate.dataType != "Bool":
            raise badwhilecond("While predicate must evaluate to a Bool value")

        ctx.dataType = 'Object'  # always

    def enterLet_expr(self, ctx: coolParser.Let_exprContext):
        # Parent node to Let_decl
        object_env, active_class = getCurrentScope(ctx)
        object_env.openScope()
        body = ctx.expr()

    def exitLet_expr(self, ctx: coolParser.Let_exprContext):
        object_env, active_class = getCurrentScope(ctx)
        object_env.closeScope()
        if ctx.expr().dataType == 'SELF_TYPE':
            ctx.dataType = active_class.name
        else:
            ctx.dataType = ctx.expr().dataType

    def enterLet_decl(self, ctx: coolParser.Let_declContext):
        # Store the variable in current Scope
        object_env, active_class = getCurrentScope(ctx)
        identifier = ctx.ID().getText()
        declared_type = ctx.TYPE().getText()
        object_env[identifier] = declared_type

    def exitLet_decl(self, ctx: coolParser.Let_declContext):
        declared_type = ctx.TYPE().getText()
        if ctx.expr():  # has initialization
            try:
                data_type = ctx.expr().dataType
                if declared_type == 'SELF_TYPE':
                    _, left_klass = getCurrentScope(ctx)
                else:
                    left_klass = lookupClass(declared_type)
                right_klass = lookupClass(data_type)

                if not right_klass.conformsTo(left_klass):
                    raise letbadinit(
                        f"Provided {data_type} does not conform to {declared_type}"
                    )

            except AttributeError:
                print(f"{ctx.expr().getText()} expression has no dataType")
            except KeyError as e:
                print("Let declaration error", e)
                raise Exception()

    def enterNew(self, ctx: coolParser.NewContext):
        # Store the TYPE and return it to parent
        ctx.dataType = ctx.TYPE().getText()

    def exitAssignment(self, ctx: coolParser.AssignmentContext):
        # receive the dataType from the child node
        object_env, active_class = getCurrentScope(ctx)
        id = ctx.ID().getText()
        if id == 'self':
            left_side = active_class.name
        else:
            left_side = object_env[id]
        right_side = ctx.expr().dataType

        try:
            if right_side == 'SELF_TYPE':
                right_klass = active_class
            else:
                right_klass = lookupClass(right_side)
            left_klass = lookupClass(left_side)
        
        except Exception as _e:
            missing = []
            existing = classDict.keys()
            if right_side not in existing:
                missing += [right_side]
            if left_side not in existing:
                missing += [left_side]
            msg = ",".join(missing)
            raise missingclass(msg)

        # right_side must conform to left_side
        if not right_klass.conformsTo(left_klass):
            raise assignnoconform
        
        ctx.dataType = ctx.expr().dataType

    def exitIf_else(self, ctx: coolParser.If_elseContext):
        data_type_if = getKlass(ctx.expr(1).dataType, ctx)
        data_type_else = getKlass(ctx.expr(2).dataType, ctx)

        least_common_ancestor = getLeastCommonAncestor(data_type_if, data_type_else)
        ctx.dataType = least_common_ancestor

    
    def exitBlock(self, ctx:coolParser.BlockContext):
        # Return type is last expression's return type
        exprs = ctx.expr()
        ctx.dataType = exprs[-1].dataType

    def exitLess_than(self, ctx:coolParser.Less_thanContext):
        ctx.dataType = 'Bool'

    def exitLess_or_equal(self, ctx:coolParser.Less_or_equalContext):
        ctx.dataType = 'Bool'

    def exitNot(self, ctx:coolParser.NotContext):
        if ctx.expr().dataType == 'Bool':
            ctx.dataType = 'Bool'
        else:
            raise Exception("Type Error: argument of 'not' must be Bool")


    def enterCase_stat(self, ctx:coolParser.Case_statContext):
        objectEnv, _ = getCurrentScope(ctx)

        objectEnv.openScope()
        objectEnv[ctx.ID().getText()] = ctx.TYPE().getText()


    def exitCase_stat(self, ctx:coolParser.Case_statContext):
        objectEnv, _ = getCurrentScope(ctx)
        objectEnv.closeScope()

    def exitIsvoid(self, ctx:coolParser.IsvoidContext):
        ctx.dataType = 'Bool'