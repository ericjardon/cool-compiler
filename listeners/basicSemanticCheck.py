from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from .semantic_utils import KEYWORDS

prohibitedClassRedefinitions = {
    'Int':badredefineint,
    'Object':redefinedobject,
    'SELF_TYPE':selftyperedeclared,
}

prohibitedInheritance = {'Bool': inheritsbool, 'String': inheritsstring, 'SELF_TYPE': inheritsselftype}

class basicSemanticListener(coolListener):

    def __init__(self):
        self.main = False

    def enterKlass(self, ctx:coolParser.KlassContext):
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True
        
        classname = ctx.TYPE(0).getText()
        if classname in prohibitedClassRedefinitions:
            raise prohibitedClassRedefinitions[classname]()

        if ctx.TYPE(1):
            inheritance = ctx.TYPE(1).getText()
            if inheritance in prohibitedInheritance:
                raise prohibitedInheritance[inheritance]()
                    

    def exitKlass(self, ctx:coolParser.KlassContext):
        if (not self.main):
            raise nomain("You need to define a Main class")

    def enterFeature_attribute(self, ctx: coolParser.Feature_attributeContext):
        if(ctx.ID().getText() == "self"):
            raise anattributenamedself("Self is a reserved keyword")
        if ctx.expr():
            if ctx.expr().primary():
                if ctx.expr().primary().getText() == 'self':
                    raise selfassignment()

    def enterLet_decl(self, ctx: coolParser.Let_declContext):
        # For every ID check that it is not == 'self'
        for token in ctx.getTokens(42):
            if token.getText() == 'self':
                raise letself()
        
    def enterFeature_function(self, ctx: coolParser.Feature_functionContext):
        for param in ctx.params:
            if param.TYPE().getText() == 'SELF_TYPE':
                raise selftypeparameterposition()
            if param.ID().getText() == "self":
                raise selfinformalparameter()