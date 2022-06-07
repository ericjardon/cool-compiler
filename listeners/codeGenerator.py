from enum import Enum
from util import asm
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import _allClasses as classesDict, lookupClass
import util.asm_text as asm
from util.structure import *
from antlr4.tree.Tree import ParseTree
from typing import Tuple

# User a SymbolTableWithScopes to map a local variable name
# to its offset


class NS(Enum):
    LOCALS = 1
    FORMALS = 2
    ATTRIBUTES = 3


def getActiveClass(ctx: ParseTree) -> Klass:
    p = ctx.parentCtx
    while (p and not hasattr(p, 'activeClass')):
        p = p.parentCtx

    return p.activeClass


def getCurrentMethodContext(ctx: ParseTree) -> ParseTree:
    p = ctx.parentCtx
    while (p and not hasattr(p, 'method_name')):
        p = p.parentCtx
    return p


def getAttrOffset(name: str, attr_list: list[str]) -> int:
    return attr_list.index(name)


def search(varname: str, methodCtx: ParseTree, klass: Klass) -> NS:
    # First look into locals
    print('Search name', varname)
    try:
        methodCtx.locals[varname]
        return NS.LOCALS
    except KeyError as e:
        print('not a local')
        pass
    # Second look into params
    try:
        params = klass.lookupMethod(methodCtx.method_name).params
        if varname in params:
            return NS.FORMALS
    except:
        print('not a param')
        pass
    
    # Last, look into klass
    try:
        klass.lookupAttribute(varname)
        return NS.ATTRIBUTES
    except KeyError:
        print('not an attribute')
        pass

    raise Exception(f"Name {varname} in method {methodCtx.method_name} not found")



class codeGenerator(coolListener):
    def __init__(self,
                 registered_ints: dict[int, int],
                 registered_strings: dict[str, int],
                 method_locals: dict[str, int]) -> None:

        self.registered_ints = registered_ints
        self.registered_strings = registered_strings
        self.method_locals = method_locals  # name -> number of local vars
        # method_name -> current index by method name
        self.method_locals_index = {}
        self.result = ''
        self.stack = []  # maybe not needed
        self.labels = 0
        self.program_classes = {}  # klass name -> klass ParseTree

    def enterKlass(self, ctx: coolParser.KlassContext):
        k = classesDict[ctx.TYPE(0).getText()]

        ctx.activeClass = k

        for feature in ctx.feature():
            feature.activeClass = k

    def addClassInitMethods(self):
        '''
        Appends the definitions for Klass_init methods of every
        class in the program. Every class should call its parent class' initializer
        except Object
        '''
        init_methods_string = ''

        for class_name, klass in classesDict.items():
            if class_name == "Object":
                parent_init = None
            else:
                parent_init = asm.tpl_parent_init.substitute(
                    parent_name=klass.inherits
                )

            if class_name in self.program_classes:
                init_code = self.program_classes[class_name].init_code
            else:
                init_code = ''

            init_methods_string += asm.tpl_object_init.substitute(
                class_name=class_name,
                inherits_init=parent_init if parent_init else "",
                init_code=init_code
            )

        self.result += init_methods_string

    def addClassMethods(self):
        '''
        For every class append the code of its methods
        '''
        for klass_node in self.program_classes.values():
            self.result += klass_node.code

    def enterProgram(self, ctx: coolParser.ProgramContext):
        self.result += asm.tpl_start_text
        self.result += asm.tpl_global_methods

    def exitPrimary(self, ctx: coolParser.PrimaryContext):
        if ctx.INTEGER():
            int_value = int(ctx.INTEGER().getText())
            ctx.code = asm.tpl_primary_int.substitute(
                int_const_name=self.registered_ints[int_value],
                int_value=int_value
            )
        elif ctx.STRING():
            ctx.code='NotImplementedError("String primary")'
        elif ctx.TRUE():
            ctx.code = asm.tpl_primary_true
        elif ctx.FALSE():
            ctx.code = asm.tpl_primary_false

        elif ctx.ID():
            # Search for name:

            var_name = ctx.ID().getText()
            klass = getActiveClass(ctx)
            method = getCurrentMethodContext(ctx)
            print(f"Var {var_name} in {method.method_name}?")
            
            # checks if name is in locals, then params, then attributes
            ns = search(var_name, method, klass)

            if ns==NS.ATTRIBUTES:
                pass
            elif ns==NS.FORMALS:
                pass
            else:  # ns==NS.LOCALS
                pass
            ctx.code='MISSING CODE FOR ID IN NS' + str(ns)

    def exitPrimary_expr(self, ctx: coolParser.Primary_exprContext):
        primary = ctx.getChild(0)
        try:
            ctx.code = primary.code
        except AttributeError:
            print(f"Primary expression {ctx.getText()} has no generated code")

    def exitBlock(self, ctx: coolParser.BlockContext):
        inner_code = [expr.code for expr in ctx.expr()
                      if hasattr(expr, 'code')]
        ctx.code = ''.join(inner_code)

    def enterFeature_function(self, ctx: coolParser.Feature_functionContext):
        ctx.method_name = ctx.activeClass.name + '.' + ctx.ID().getText()

        num_locals = self.method_locals[ctx.method_name]
        ctx.frame_size_bytes = 12 + num_locals * 4  # 12 for fp, s0 and ra

        # Each local variable name corresponds to an offset in stack.
        # For every method keep an index to keep track of offset
        # Use a symboltablewith scopes to map name->offset
        ctx.locals_index = 0
        
        ctx.locals = SymbolTableForLocals()  # maps local var name -> offset (bytes)

        ctx.code = asm.tpl_on_enter_callee.substitute(
            class_method_name=ctx.method_name,
            frame_size_bytes=str(ctx.frame_size_bytes),
            frame_size_bytes_minus_4=str(ctx.frame_size_bytes - 4),
            frame_size_bytes_minus_8=str(ctx.frame_size_bytes - 8),
        )

    def exitFeature_function(self, ctx: coolParser.Feature_functionContext):
        # Code of Body
        body = ctx.expr()
        ctx.code += body.code  # all nodes should generate code

        name = ctx.ID().getText()
        num_formals = len(ctx.activeClass.lookupMethod(name).params)
        formals_bytes = num_formals * 4

        # Return to caller
        ctx.code += asm.tpl_return_to_caller.substitute(
            frame_size_bytes=str(ctx.frame_size_bytes),
            frame_size_bytes_minus_4=str(ctx.frame_size_bytes - 4),
            frame_size_bytes_minus_8=str(ctx.frame_size_bytes - 8),
            formals_bytes=formals_bytes,
            frame_and_formals_bytes=str(ctx.frame_size_bytes + formals_bytes)
        )

    def exitFeature_attribute(self, ctx: coolParser.Feature_attributeContext):

        subexpr = ctx.expr()  # initialization subexpression
        if subexpr:
            # Get offset of attribute
            k = getActiveClass(ctx)
            attrs = k.getAllAttributeNames()
            name = ctx.ID().getText()
            attr_offset = getAttrOffset(name, attrs)

            try:
                ctx.code = asm.tpl_attribute.substitute(
                    attribute_subexpr_code=subexpr.code,
                    attr_offset=attr_offset
                )
            except AttributeError:
                print(
                    f"Init expression <{ctx.getText()}> has no generated code")

    def exitKlass(self, ctx: coolParser.KlassContext):
        ctx.init_code = ''      # code of init attributes
        ctx.code = ''           # code of method bodies

        for feature in ctx.feature():
            # If method, add to methods code.
            if hasattr(feature, 'params'):
                ctx.code += feature.code
            # If attribute, add to init code if present.
            elif hasattr(feature, 'code'):
                ctx.init_code += feature.code

        # For appending init code later
        self.program_classes[ctx.TYPE(0).getText()] = ctx

    def enterLet_expr(self, ctx: coolParser.Let_exprContext):
        # For every let var, add to current methods locals, increase number
        method = getCurrentMethodContext(ctx)
        method.locals.openScope()

        for var in ctx.let_decl():
            name = var.ID().getText()
            # * 4 gives offset in bytes
            method.locals[name] = method.locals_index
            method.locals_index += 1

    def exitLet_expr(self, ctx: coolParser.Let_exprContext):
        # load default or init values for locals
        method = getCurrentMethodContext(ctx)

        let_code = ''

        for var in ctx.let_decl():
            name = var.ID().getText()
            offset = method.locals[name] * 4
            if var.expr():
                let_code += asm.tpl_single_let_decl_init.substitute(
                    let_var_subexpr=var.expr().code,
                    ith_local_offset=str(offset)
                )
            else:
                # Load default value in Data Segment
                let_code += asm.tpl_single_let_decl_default.substitute(
                    default_obj="MISSING: get default for" + var.TYPE().getText(),
                    ith_local_offset=str(offset)
                )

        method.locals.closeScope()
        ctx.code = let_code

    def exitProgram(self, ctx: coolParser.ProgramContext):
        # Init methods
        self.addClassInitMethods()  # for every class add .init_code
        self.addClassMethods()      # for every class add .code

    def exitAssignment(self, ctx: coolParser.AssignmentContext):
        ctx.code = '\nMISSING'

    def exitNot(self, ctx: coolParser.NotContext):
        ctx.code = '\nMISSING'

    def exitEquals(self, ctx: coolParser.EqualsContext):
        ctx.code = '\nMISSING'

    def exitLess_than(self, ctx: coolParser.Less_thanContext):
        ctx.code = '\nMISSING'

    def exitLess_or_equal(self, ctx: coolParser.Less_or_equalContext):
        ctx.code = '\nMISSING'

    def exitCase_stat(self, ctx: coolParser.Case_statContext):
        ctx.code = '\nMISSING'

    def exitSubtraction(self, ctx: coolParser.SubtractionContext):
        ctx.code = '\nMISSING'

    def exitMultiplication(self, ctx: coolParser.MultiplicationContext):
        ctx.code = '\nMISSING'

    def exitDivision(self, ctx: coolParser.DivisionContext):
        ctx.code = '\nMISSING'

    def exitStatic_dispatch(self, ctx: coolParser.Static_dispatchContext):
        ctx.code = '\nMISSING'

    def exitWhile(self, ctx: coolParser.WhileContext):
        ctx.code = '\nMISSING'

    def exitMethod_call(self, ctx: coolParser.Method_callContext):
        ctx.code = '\nMISSING'
