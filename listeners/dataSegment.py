from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import _allClasses as classesDict

import util.asm as asm

class DataGenerator(coolListener):
    def __init__(self):
        self.result = ''
        self.constants = 0

    def enterProgram(self, ctx: coolParser.ProgramContext):
        self.result += asm.tpl_start_data

    def enterDeclaracion(self, ctx: coolParser.DeclaracionContext):
        # No more variables in data segment in this version!
        # self.result += asm.tpl_var_decl.substitute(
        #     varname = ctx.getChild(1).getText()
        # )
        # ctx.co                                                                                                                                                                                                                                                                    de = ''
        ctx.code = ''

    def enterPrimaria_string(self, ctx: coolParser.Primaria_stringContext):
        self.constants = self.constants + 1
        ctx.label = "const{}".format(self.constants)
        self.result += asm.tpl_string_const_decl.substitute(
            name = ctx.label, content = ctx.getText()
        )