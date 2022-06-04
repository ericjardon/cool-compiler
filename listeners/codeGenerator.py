from util import asm
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import _allClasses as classesDict, lookupClass
import util.asm_text as asm
class codeGenerator(coolListener):
    def __init__(self, registered_ints: dict[int,int], registered_strings:dict[str,int]) -> None:
        super().__init__()
        self.registered_ints=registered_ints
        self.registered_strings=registered_strings

    def addClassInitMethods(self):
        '''
        Appends to result the definitions for _init methods of every
        class in the program. Every class must call its parent class' initializer
        '''
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
        self.result += asm.tpl_global_methods
        # Init methods
        self.addClassInitMethods()
    
    def exitPrimary(self, ctx: coolParser.PrimaryContext):
        if ctx.INTEGER():
            int_value = int(ctx.INTEGER.getText())
            ctx.code = asm.tpl_primary_int.substitute(
                int_const_name=self.registered_ints[int_value],
                int_value=int_value
            )
        elif ctx.STRING():
            raise NotImplementedError()
        elif ctx.TRUE():
            ctx.code = asm.tpl_primary_true
        elif ctx.FALSE():
            ctx.code = asm.tpl_primary_false

        elif ctx.ID():  # is a variable name, assign type from scope
            # Is in stack?'
            raise NotImplementedError()

    def exitFeature_function(self, ctx:coolParser.Feature_functionContext):
        # Generate the code for this method.
        pass
