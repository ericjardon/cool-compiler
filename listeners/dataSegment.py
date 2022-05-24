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

    def enterProgram(self, ctx: coolParser.ProgramContext):
        self.result += asm.tpl_start_data

        # Add classes protObjs
        self.appendGlobalLabels()

    # On enter literal value, add it to str or int stack

    """ def enterPrimaria_string(self, ctx: coolParser.Primaria_stringContext):
        self.constants = self.constants + 1
        ctx.label = "const{}".format(self.constants)
        self.result += asm.tpl_string_const_decl.substitute(
            name = ctx.label, content = ctx.getText()
        ) """


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
            asm.tpl_class_tag.substitute(
                name=classname
            )
        )
    return substitution