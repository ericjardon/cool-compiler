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

KNOWN_SIZES = {
    'Object':3,
    'IO':3,
    'Int':4,
    'Bool':4,
    'String': 5, ## why?
    'Main': 3,
}


class dataSegment(coolListener):
    def __init__(self):
        self.result = ''  # string builder
        self.str_constants_count = 0
        self.int_constants_count = 0
        self.class_id = {}  # name to tag mapping
        for tag, name in enumerate(classesDict.keys()):
            self.class_id[name] = tag
    
    def appendGlobalLabels(self):
        prototype_tags = getPrototypeTags()
        class_tags = getClassTags()

        self.result += asm.tpl_global_tags_start.substitute(
            prototype_tags=prototype_tags,
            class_tags = class_tags
        )

    def appendDispatchTables(self):
        # Object, IO, Int, Bool, String, Main
        self.result += asm.tpl_obj_dispatch_table
        self.result += asm.tpl_io_dispatch_table
        self.result += asm.tpl_int_dispatch_table
        self.result += asm.tpl_string_dispatch_table
        self.result += asm.tpl_main_dispatch_table

    def appendBasePrototypes(self):
        # Object, IO, Int, Bool, String, Main
        self.result += asm.tpl_non_init_prototype_object.substitute(
            name="Object",
            class_id=self.class_id["Object"],
            size=KNOWN_SIZES["Object"],
            dispatch="Object_dispTab"
        )
        # continue...


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
        self.appendDispatchTables()
        self.appendBasePrototypes()
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