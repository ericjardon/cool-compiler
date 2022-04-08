# Generated from /Users/jc/Documents/Compiladores/Proyecto/cool-compiler/antlr/cool.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .coolParser import coolParser
else:
    from coolParser import coolParser

# This class defines a complete listener for a parse tree produced by coolParser.
class coolListener(ParseTreeListener):

    # Enter a parse tree produced by coolParser#program.
    def enterProgram(self, ctx:coolParser.ProgramContext):
        pass

    # Exit a parse tree produced by coolParser#program.
    def exitProgram(self, ctx:coolParser.ProgramContext):
        pass


    # Enter a parse tree produced by coolParser#klass.
    def enterKlass(self, ctx:coolParser.KlassContext):
        pass

    # Exit a parse tree produced by coolParser#klass.
    def exitKlass(self, ctx:coolParser.KlassContext):
        pass


    # Enter a parse tree produced by coolParser#feature.
    def enterFeature(self, ctx:coolParser.FeatureContext):
        pass

    # Exit a parse tree produced by coolParser#feature.
    def exitFeature(self, ctx:coolParser.FeatureContext):
        pass


    # Enter a parse tree produced by coolParser#formal.
    def enterFormal(self, ctx:coolParser.FormalContext):
        pass

    # Exit a parse tree produced by coolParser#formal.
    def exitFormal(self, ctx:coolParser.FormalContext):
        pass


    # Enter a parse tree produced by coolParser#expr.
    def enterExpr(self, ctx:coolParser.ExprContext):
        pass

    # Exit a parse tree produced by coolParser#expr.
    def exitExpr(self, ctx:coolParser.ExprContext):
        pass


    # Enter a parse tree produced by coolParser#case_stat.
    def enterCase_stat(self, ctx:coolParser.Case_statContext):
        pass

    # Exit a parse tree produced by coolParser#case_stat.
    def exitCase_stat(self, ctx:coolParser.Case_statContext):
        pass


    # Enter a parse tree produced by coolParser#let_decl.
    def enterLet_decl(self, ctx:coolParser.Let_declContext):
        pass

    # Exit a parse tree produced by coolParser#let_decl.
    def exitLet_decl(self, ctx:coolParser.Let_declContext):
        pass


    # Enter a parse tree produced by coolParser#primary.
    def enterPrimary(self, ctx:coolParser.PrimaryContext):
        pass

    # Exit a parse tree produced by coolParser#primary.
    def exitPrimary(self, ctx:coolParser.PrimaryContext):
        pass



del coolParser