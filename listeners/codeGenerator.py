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

def getAttrOffset(name:str, attr_list:list[str]) -> int:
    return attr_list.index(name)

class codeGenerator(coolListener):
    def __init__(self,
                 registered_ints: dict[int, int],
                 registered_strings: dict[str, int],
                 method_locals: dict[str, int]) -> None:
        
        self.registered_ints = registered_ints
        self.registered_strings = registered_strings
        self.method_locals = method_locals
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
            raise NotImplementedError("String primary")
        elif ctx.TRUE():
            ctx.code = asm.tpl_primary_true
        elif ctx.FALSE():
            ctx.code = asm.tpl_primary_false

        elif ctx.ID():
            # If Attribute, fetch from offset(self)
            # If local, fetch from
            raise NotImplementedError("ID eval")
    
    def exitPrimary_expr(self, ctx: coolParser.Primary_exprContext):
        primary = ctx.getChild(0)
        try:
            ctx.code = primary.code
        except AttributeError:
            print(f"Primary expression {ctx.getText()} has no generated code")


    def exitBlock(self, ctx:coolParser.BlockContext):
        inner_code = [expr.code for expr in ctx.expr()]
        ctx.code = ''.join(inner_code)


    def enterFeature_function(self, ctx: coolParser.Feature_functionContext):
        ctx.method_name = ctx.activeClass.name + '.' + ctx.ID().getText()

        num_locals = self.method_locals[ctx.method_name]
        ctx.frame_size_bytes = 12 + num_locals * 4  # 12 for fp, s0 and ra
        
        # Each local variable name corresponds to an offset in stack.
        # For every method keep an index to keep track of offset
        # Use a symboltablewith scopes to map name->offset
        ctx.locals_index = 0
        ctx.objectEnv = SymbolTableWithScopes(ctx.activeClass)  # for names

        ctx.code = asm.tpl_on_enter_callee.substitute(
            class_method_name=ctx.method_name,
            frame_size_bytes=str(ctx.frame_size_bytes),
            frame_size_bytes_minus_4=str(ctx.frame_size_bytes - 4),
            frame_size_bytes_minus_8=str(ctx.frame_size_bytes - 8),
        )
        # CONTINUE: TRY PRINTING METHOD'S DECLARATIONS


    def exitFeature_function(self, ctx: coolParser.Feature_functionContext):

        # Generated code of Body
        body = ctx.expr()        
        ctx.code += body.code  # all nodes should generate code

        name = ctx.ID().getText()
        num_formals = len(ctx.activeClass.lookupMethod(name).params)
        formals_bytes = num_formals * 4

        # Return to caller 
        ctx.code += asm.tpl_return_to_caller.substitute(
            formals_bytes=formals_bytes,
            frame_bytes=str(ctx.frame_size_bytes),
            frame_and_formals_bytes=str(ctx.frame_size_bytes + formals_bytes)
        )


    def exitFeature_attribute(self, ctx:coolParser.Feature_attributeContext):

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
                print(f"Init expression <{ctx.getText()}> has no generated code")

    def exitKlass(self, ctx: coolParser.KlassContext):
        ctx.init_code = ''      # code of init attributes
        ctx.code = ''           # code of method bodies

        for feature in ctx.feature():
            # If method, add to methods code.
            if hasattr(feature, 'params'):
                ctx.code += feature.code
            # If attribute, add to init code.
            else:
                ctx.init_code += feature.code
        
        # For appending init code later
        self.program_classes[ctx.TYPE(0).getText()] = ctx



    def exitProgram(self, ctx:coolParser.ProgramContext):
        # Init methods
        self.addClassInitMethods()  # for every class add .init_code
        self.addClassMethods()      # for every class add .code

    