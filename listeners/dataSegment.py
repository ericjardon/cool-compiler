import math

from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import _allClasses as classesDict, lookupClass
import util.asm as asm

CONSTANT_CLASSES = [
    'Int',
    'Bool',
    'String'
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
    'String': 4,  # is variable
} # Main class size is variable, as well as string


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
        self.DEFAULTS = {}

        for tag, name in enumerate(classesDict.keys()):
            self.class_id[name] = tag
        
        # Register 0, 1 Ints
        for integer in BUILTIN_INTS:
            self.addIntConst(integer)

    def populateDefaultObjectNames(self):
        self.DEFAULTS['Int'] = self.registered_ints[0]
        self.DEFAULTS['String'] = self.registered_strings[0]
        self.DEFAULTS['Bool'] = 'bool_const0'
        return

    def addGlobalLabels(self):
        prototype_tags = getPrototypeTags()
        class_tags = getClassTags()

        self.result += asm.tpl_global_tags_start.substitute(
            prototype_tags=prototype_tags,
            class_tags = class_tags
        )

    def addDispatchTables(self):
        for class_name in classesDict.keys():
            methods = getDispTabMethods(class_name)
            self.result += asm.tpl_dispatch_table.substitute(
                class_name=class_name,
                methods=methods
            )

    def addPrototypes(self):

        for class_name in classesDict:
            class_id = self.class_id[class_name]
            dispatch = f"{class_name}_dispTab"
            size = getPrototypeSize(class_name)
            
            if class_name == "String":
                len_name = self.registered_ints[0]
                self.result += asm.tpl_string_prototype_string.substitute(
                    len_name=len_name,
                    name=class_name,
                    class_id=class_id,
                    size=size,
                    dispatch=dispatch
                )
            else:
                self.result += asm.tpl_init_prototype_object.substitute(
                    name=class_name,
                    class_id=class_id,
                    size=size,
                    dispatch=dispatch
                )
                # Initialize default attributes (Object size gte 4)
                remaining = size
                
                attributes = classesDict[class_name].getAvailableAttributes(deque([]))

                while attributes:
                    a_type = attributes.pop()
                    if a_type in self.DEFAULTS:  # base attribute, init accordingly
                        self.result += asm.tpl_single_default_attribute.substitute(
                            default=self.DEFAULTS[a_type]
                        )
                    else:  # Non-base attribute
                        self.result += asm.tpl_single_default_attribute.substitute(
                            default='0'
                        )
                    remaining -= 1

                # Assembly-only attributes
                for _ in range(3, remaining):
                    self.result += asm.tpl_single_default_attribute.substitute(
                        default='0'
                    )

    def addBuiltinStrings(self):
        for string in BUILTIN_STRINGS:
            self.addStringConst(string)

    def addHeapStart(self):
        self.result += asm.tpl_heap_start

    def MemMgrBoilerPlate(self):
        self.result += asm.tpl_data_MemMgr

    def addClassNames(self):
        for name in classesDict.keys():
            self.addStringConst('"'+name+'"')

    def addConstantsText(self):
        self.result += self.str_constants_text
        self.result += self.int_constants_text
        self.result += self.bool_constants_text
    
    def addClassTagIDs(self):
        for name in CONSTANT_CLASSES:
            self.result += asm.tpl_class_tag.substitute(
                name=name.lower(),
                n=self.class_id[name]
            )

    def addClassNameTable(self):
        from pprint import pprint
        names = ''

        for key, value in self.registered_strings.items():
            # Key includes double-quotes
            if key!=0 and key[1:-1] in classesDict:
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
        self.addGlobalLabels()
        self.addClassTagIDs()
        self.MemMgrBoilerPlate()
        self.addClassNames()
        self.addBoolConstants() 
        self.addBuiltinStrings()
    
    def exitProgram(self, ctx: coolParser.ProgramContext):
        # from pprint import pprint
        # print("string constants")
        # pprint(self.registered_strings)
        self.addNullStringConst()
        self.populateDefaultObjectNames()

        # Generation
        self.addConstantsText()
        self.addClassNameTable()
        self.addObjectTable()
        self.addDispatchTables()
        self.addPrototypes()
        self.addHeapStart()

    # On enter literal value, add it to str or int stack
    def addStringConst(self, text):
        byte_size = len(text) - 2 if text.startswith('\"') else len(text)
        if byte_size not in self.registered_ints:
            self.addIntConst(byte_size)

        attribute = asm.tpl_string_atr.substitute(
            len_name=self.registered_ints[byte_size],
            content=f'{text}'  # including double-quotes !!!
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
    
    def addNullStringConst(self):
        # call once
        name = 'str_const'+str(self.str_constants_count)
        self.str_constants_text += asm.tpl_null_string_const.substitute(
            name=name,
            zero_int = self.registered_ints[0]
        )
        self.registered_strings[0] = 'str_const'+str(self.str_constants_count)
        self.str_constants_count += 1


    def addIntConst(self, content:int):
        if content in self.registered_ints:
            return
        self.registered_ints[content] = f"int_const{self.int_constants_count}"
        attribute = asm.tpl_int_atr.substitute (
                content=content
            )
        self.int_constants_text += asm.tpl_const_obj_start.substitute(
            name=f"int_const{self.int_constants_count}",
            class_id=self.class_id['Int'],
            size=KNOWN_SIZES['Int'],
            dispatch="Int_dispTab",
            attributes=attribute
            )
        self.int_constants_count += 1
    
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
            self.addIntConst(int(ctx.INTEGER().getText()))
            return
        if ctx.STRING():
            text = ctx.STRING().getText()
            self.addStringConst(text)
            return
        
        

def getPrototypeTags() -> str:
    substitution = ''
    global_prototypes = [
        'Main',
        'Int',
        'String',
    ]
    for classname in global_prototypes:
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
                name=classname.lower()
            )
        )
    return substitution

from collections import deque
def getDispTabMethods(class_name) -> list[str]:
    entries = ''

    methods_stack = classesDict[class_name].getAvailableMethods(deque([]))
    while methods_stack:
        entries += asm.tpl_method_name.substitute(
            method_disp = methods_stack.pop()
        )
    
    return entries

def getPrototypeSize(class_name) -> list[str]:
    # Go up the inheritance tree until we reach a 'Known Size' class
    # Add all traversed attributes to the known size.
    size_words = 0 
    c = classesDict[class_name]

    while c.name not in KNOWN_SIZES:
        size_words += len(c.attributes)
        c = classesDict[c.inherits]
    
    size_words += KNOWN_SIZES[c.name]

    return size_words
    
