from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from .semantic_utils import KEYWORDS

prohibitedClassRedefinitions = {
    'Int':badredefineint,
    'Object':redefinedobject,
    'SELF_TYPE':selftyperedeclared,
}
class basicSemanticListener(coolListener):

    def __init__(self):
        self.main = False

    def enterKlass(self, ctx:coolParser.KlassContext):
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True
        
        classname = ctx.TYPE(0).getText()
        if classname in prohibitedClassRedefinitions:
            raise prohibitedClassRedefinitions[classname]()


    

    def exitKlass(self, ctx:coolParser.KlassContext):
        if (not self.main):
            raise nomain("You need to define a Main class")

    def enterFeature(self, ctx: coolParser.FeatureContext):
        if(ctx.ID().getText() == "self"):
            raise anattributenamedself("Self is a reserved keyword")

    def enterLet_decl(self, ctx: coolParser.Let_declContext):
        # For every ID check that it is not == 'self'
        for token in ctx.getTokens(42):
            if token.getText() == 'self':
                raise letself()

