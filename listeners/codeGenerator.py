from util import asm
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import _allClasses as classesDict, lookupClass
import util.asm_text as asm
class codeGenerator(coolListener):

    def addClassInitMethods(self):
        init_methods_string = ""

        for class_name, klass in classesDict.items():

            if class_name=="Object":
                parent_init = None
            else:
                parent_init = asm.tpl_parent_init.substitute(
                    parent_name=klass.inherits
                )

            init_methods_string += asm.tpl_object_init.substitute(
                class_name=class_name,
                inherits_init=parent_init if parent_init else ""
            )
        
        self.result += init_methods_string


    def __init__(self):
        self.result = ''
        self.stack = []
        self.labels = 0
    
    def enterProgram(self, ctx:coolParser.ProgramContext):
        self.result += asm.tpl_start_text
        # Init methods
        self.addClassInitMethods()
        
    
    def exitProgram(self, ctx: coolParser.ProgramContext):
        for c in ctx.getChildren():
            self.result += c.code
        self.result += asm.tpl_end

    def exitPrimary(self, ctx: coolParser.PrimaryContext):
        self.stack.append(
            asm.tpl_immediate.substitute(immediate=ctx.getText())
            )
        
        if ctx.STRING:
            self.stack.append(
                asm.tpl_string_const.substitute(
                    name = ctx.label
                )
            )

    def exitAddition(self, ctx: coolParser.AdditionContext):
        self.stack.append(
            asm.tpl_suma.substitute(
                right=self.stack.pop(), 
                left=self.stack.pop()
                )
            )   

    def exitSubtraction(self, ctx: coolParser.SubtractionContext):
        self.stack.append(
            asm.tpl_resta.substitute(
                right=self.stack.pop(), 
                left=self.stack.pop()
                )
            )
        
    def exitLess_than(self, ctx: coolParser.Less_thanContext):
        self.labels = self.labels = self.labels + 1
        self.stack.append(
            asm.tpl_menorque.substitute(
                right=self.stack.pop(),
                left=self.stack.pop(),
                n=self.labels
            )
        )

    def exitAssignment(self, ctx: coolParser.AssignmentContext):
        ctx.code = asm.tpl_asignacion_from_stack.substitute(
             prev = self.stack.pop(),
             name = ctx.getChild(0).getText(),
             offset = ctx.getChild(0).offset
        )
        

    def exitIf_else(self, ctx: coolParser.If_elseContext):
        self.labels = self.labels = self.labels + 1
        ctx.code = asm.tpl_if_else.substitute(
            prev = self.stack.pop(),
            n = self.labels, 
            stmt_true = ctx.statement(0).code, 
            stmt_false = ctx.statement(1).code
        )

    def exitBlock(self, ctx: coolParser.BlockContext):
        ctx.code = ''
        for c in ctx.statement():
            ctx.code += c.code
    
    def exitWhile(self, ctx: coolParser.WhileContext):
        self.labels = self.labels + 1
        ctx.code = asm.tpl_while.substitute(
            test = self.stack.pop(),
            n = self.labels,
            stmt = ctx.statement().code
        )

    def exitFeature_function(self, ctx: coolParser.Feature_functionContext):
        ctx.code = asm.tpl_procedure.substitute(
            name = ctx.name.text,
            code = ctx.statement().code,
            stack_size = (2 + ctx.params + ctx.locals) * 4,
            frame_size = (2 + ctx.locals) * 4
        )

    def exitDispatch(self, ctx: coolParser.DispatchContext):
        result = ''
        params = 0
        for c in ctx.expression():
            result += self.stack.pop()
            result += asm.tpl_push_arg
        
        self.stack.append(
            asm.tpl_call.substitute(
                push_arguments = result,
                name = ctx.Variable()
            )
        )        
    