import math

from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import _allClasses as classesDict
import util.asm as asm

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
    'String': 4,
    'Main': 3,
}


class dataSegment(coolListener):
    def __init__(self):
        self.result = ''  # string builder
        self.str_constants_text = ''
        self.str_constants_count = 0
        self.int_constants_text = ''
        self.int_constants_count = 0
        self.bool_constants_text = ''
        self.bool_constants_count = 0
        self.registered_ints = {} # number to name mapping (1 to int_const1)
        self.registered_strings = {} # string to name mapping ("Int to str_const1")
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
        pass

    def appendBasePrototypes(self):
        # Object, IO, Int, Bool, String, Main
        self.result += asm.tpl_non_init_prototype_object.substitute(
            name="Object",
            class_id=self.class_id["Object"],
            size=KNOWN_SIZES["Object"],
            dispatch="Object_dispTab"
        )
        # continue...
    
    def appendHeapStart(self):
        self.result += asm.tpl_heap_start

    def MemMgrBoilerPlate(self):
        self.result += asm.tpl_data_MemMgr

    def addClassNames(self):
        for name in classesDict.keys():
            self.addStringConst(name)

    def appendConstantsText(self):
        self.result += self.str_constants_text
        self.result += self.int_constants_text
        self.result += self.bool_constants_text
    
    def addClassTagIDs(self):
        for name in classesDict.keys():
            self.result += asm.tpl_class_tag.substitute(
                name=name.lower(),
                n=self.class_id[name]
            )

    def addClassNameTable(self):
        names = ''
        for key, value in self.registered_strings.items():
            
            if key in classesDict:
                names += asm.tpl_class_name.substitute(
                    name=value
                )
            
        self.result += asm.tpl_class_name_table.substitute(names=names)

    def addObjectTable(self):
        objects = ''
        for name in classesDict.keys():
            objects += asm.tpl_object_info.substitute(name=name)
            
            
        self.result += asm.tpl_object_table.substitute(objects=objects)

    
    
    def enterProgram(self, ctx: coolParser.ProgramContext):
        self.result += asm.tpl_start_data

        # Add classes protObjs -- Eric
        self.appendGlobalLabels()
        self.addClassTagIDs()
        self.MemMgrBoilerPlate()
        self.addClassNames()
        self.addBoolConstants()
    
    def exitProgram(self, ctx: coolParser.ProgramContext):
        # we know about all constants in the program.

        self.appendConstantsText()
        self.addClassNameTable()
        self.addObjectTable()
        # dispatch Table (ya están hechas) -- Eric
        self.appendDispatchTables()
        self.appendBasePrototypes()
        # prototypes -- Eric
        self.appendHeapStart()

    # On enter literal value, add it to str or int stack
    def addStringConst(self, text):
        byte_size = len(text)
        if byte_size not in self.registered_ints:
            self.addIntConst(byte_size)

        attribute = asm.tpl_string_atr.substitute(
            len_name=self.registered_ints[byte_size],
            content=f'\"{text}\"'
        )
        self.str_constants_text += asm.tpl_const_obj_start.substitute(
            name='str_const'+str(self.str_constants_count),
            class_id=self.class_id['String'],
            size=KNOWN_SIZES['String'] + math.ceil((byte_size+1)/4),
            dispatch="String_dispTab",
            attributes=attribute
        )
        self.registered_strings[text] = 'str_const'+str(self.str_constants_count)
        self.str_constants_count += 1

    def addIntConst(self, content):
        if content in self.registered_ints:
            return
        attribute = asm.tpl_int_atr.substitute (
                content=content
            )
        self.int_constants_text += asm.tpl_const_obj_start.substitute(
            name='int_const'+str(self.int_constants_count),
            class_id=self.class_id['Int'],
            size=KNOWN_SIZES['Int'],
            dispatch="Int_dispTab",
            attributes=attribute
            )
        self.int_constants_count += 1
        self.registered_ints[content] = 'int_const'+str(self.int_constants_count)
    
    def addBoolConstants(self):
        attribute = asm.tpl_int_atr.substitute (
            content=0
        )
        self.bool_constants_text += asm.tpl_const_obj_start.substitute(
            name='bool_const'+str(self.bool_constants_count),
            class_id=self.class_id['Bool'],
            size=KNOWN_SIZES['Bool'],
            dispatch="Bool_dispTab",
            attributes=attribute
        )
        self.bool_constants_count += 1

        attribute = asm.tpl_int_atr.substitute (
            content=1
        )
        self.bool_constants_text += asm.tpl_const_obj_start.substitute(
            name='bool_const'+str(self.bool_constants_count),
            class_id=self.class_id['Bool'],
            size=KNOWN_SIZES['Bool'],
            dispatch="Bool_dispTab",
            attributes=attribute
        )
        self.bool_constants_count += 1



    def enterPrimary(self, ctx: coolParser.PrimaryContext):
        if ctx.INTEGER():
            self.addIntConst(ctx.INTEGER().getText())
            return
        if ctx.STRING():
            text = ctx.STRING().getText()
            self.addStringConst(text)
            return
            
            

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

