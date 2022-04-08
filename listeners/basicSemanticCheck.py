from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class basicSemanticListener(coolListener):

    def __init__(self):
        self.main = False

    def enterKlass(self, ctx:coolParser.KlassContext):
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True

    def exitKlass(self, ctx:coolParser.KlassContext):
        if (not self.main):
            raise nomain("You need to define a Main class")

    def enterFeature(self, ctx: coolParser.FeatureContext):
        if(ctx.ID().getText() == "self"):
            raise anattributenamedself("Self is a reserved keyword")


