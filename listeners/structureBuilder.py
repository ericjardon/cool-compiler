from ctypes import util
from mimetypes import init
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.exceptions import missingclass, redefinedclass, returntypenoexist, selftypebadreturn, badequalitytest, badequalitytest2
from util.structure import *
from util.structure import _allClasses as classDict
class structureBuilder(coolListener):

    basicTypes = set(['Int','String','Bool'])

    def __init__(self) -> None:
        classDict.clear()          
        Klass("Object", None)
        setBaseKlasses()  # Int, Bool, String, IO
    
    def enterKlass(self, ctx: coolParser.KlassContext):
       
        name = ctx.TYPE(0).getText()
        print("Enter class", name)
        print(list(classDict.keys())) 
        if name in classDict:
            print("Name exists:", name)
            raise redefinedclass()

        inheritance = None

        if (ctx.TYPE(1)):
            inheritance = ctx.TYPE(1).getText()
            try:
                inherit = lookupClass(inheritance)
                k = Klass(name, inherit.name)
            except KeyError as error:
                raise missingclass()

        else:            
            k = Klass(name=name)

        for feature in ctx.feature():
            feature.activeClass = k

    def enterFeature_function(self, ctx: coolParser.Feature_functionContext):
        name = ctx.ID().getText()

        parameters = []

        for param in ctx.params:
            parameters.append((param.ID().getText(), param.TYPE().getText()))
        
        return_type = ctx.TYPE().getText()

        if (return_type == "SELF_TYPE"):
            checkClass = ctx.expr().TYPE().getText()
            if checkClass != "SELF_TYPE":
                raise selftypebadreturn()

        if (return_type != "SELF_TYPE"):
            try:
                lookupClass(return_type)
            except KeyError:
            
                raise returntypenoexist()

        if len(parameters) == 0 :
            newMethod = Method(return_type)
        else:
            newMethod = Method(return_type, parameters)
        
        ctx.activeClass.addMethod(name, newMethod)
        
         

    def enterFeature_attribute(self, ctx: coolParser.Feature_attributeContext):
        name = ctx.ID().getText()
        type = ctx.TYPE().getText()
        ctx.activeClass.addAttribute(name, type)

    def enterPrimary(self, ctx: coolParser.PrimaryContext):
        if ctx.INTEGER():
            ctx.dataType = 'Int'
        if ctx.STRING():
            ctx.dataType = 'String'
        if ctx.TRUE() or ctx.FALSE():
            ctx.dataType = 'Bool'
        else:
            pass

    def exitEquals(self, ctx: coolParser.EqualsContext):
        typeOne = ctx.children[0].dataType
        typeTwo = ctx.children[2].dataType

        if typeOne in self.basicTypes and typeTwo in self.basicTypes:
            if typeOne != typeTwo:
                if typeOne == "Int" and typeOne == "String":
                    raise badequalitytest()
                if typeOne == "Int" and typeOne == "Bool":
                    raise badequalitytest2()
                else:
                    pass





