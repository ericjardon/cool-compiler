from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import _allClasses as classesDict
import util.asm as asm
from collections import deque

CONSTANT_CLASSES = [
    'int',
    'bool',
    'string'
]

BUILTIN_STRINGS = [
    '"--filename--"',
    '"\\n"',
    '"<basic_class>"'
]

BUILTIN_INTS = [0, 1]


class dataSegment(coolListener):
    def __init__(self):
        self.result = ''  # string builder
        self.str_constants_count = 0
        self.int_constants_count = 0

    
    def appendGlobalLabels(self):
        prototype_tags = getPrototypeTags()
        class_tags = getClassTags()

        self.result += asm.tpl_global_tags_start.substitute(
            prototype_tags=prototype_tags,
            class_tags = class_tags
        )

    def MemMgrBoilerPlate(self):
        self.result += asm.tpl_data_MemMgr

    def enterProgram(self, ctx: coolParser.ProgramContext):
        self.result += asm.tpl_start_data

        # Add classes protObjs
        self.appendGlobalLabels()
        # self.appendClassTagIDs() # counter at 2 -- JC
        self.MemMgrBoilerPlate()
    
    def exitProgram(self, ctx: coolParser.ProgramContext):
        # we know about all constants in the program.

        # print constants -- JC
        # name Table -- Eric
        # object Table -- Eric
        # dispatch Table (ya están hechas) -- Eric
        # prototypes -- Eric
        # heap -- JC
        pass

    # On enter literal value, add it to str or int stack

    """ def enterPrimaria_string(self, ctx: coolParser.Primaria_stringContext):
        self.constants = self.constants + 1
        ctx.label = "const{}".format(self.constants)
        self.result += asm.tpl_string_const_decl.substitute(
            name = ctx.label, content = ctx.getText()
        ) """
# Write printMyShit function  

def getPrototypeTags() -> str:
    substitution = ''
    for classname in classesDict.keys():
        if classname == 'Object' or classname == 'Bool':
            continue
        substitution += (
            asm.tpl_prototype_tag.substitute(
                name=classname
            )
        )
    return substitution

def getClassTags() -> str:
    substitution = ''
    for classname in CONSTANT_CLASSES:
        substitution += (
            asm.tpl_global_class_tag.substitute(
                name=classname
            )
        )
    return substitution