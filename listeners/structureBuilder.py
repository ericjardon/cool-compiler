from ctypes import util
from mimetypes import init
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.exceptions import missingclass, redefinedclass, returntypenoexist, selftypebadreturn
from util.structure import *
from util.structure import _allClasses as classDict

valid_self_type_returns = ["SELF_TYPE", "self"]

class structureBuilder(coolListener):

    
    objectClass = Klass("Object", None)
    setBaseKlasses()
    
    def enterKlass(self, ctx: coolParser.KlassContext):
        
        name = ctx.TYPE(0).getText()

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
            if checkClass not in valid_self_type_returns:
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
        
