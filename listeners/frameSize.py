from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import *
from util.structure import _allClasses as classDict
from antlr4.tree.Tree import ParseTree
from collections import defaultdict
from pprint import pprint


def getCurrentMethod(ctx: ParseTree) -> ParseTree:
    parent = ctx.parentCtx
    while (parent and not hasattr(parent, 'locals_count')):
        parent = parent.parentCtx
    return parent

class frameSize(coolListener):
    '''
    Responsible for traversing methods' bodies and counting
    number of local variables (let) to determine necessary space for 
    locals for every method
    '''
    method_locals = None  

    def __init__(self) -> None:
        print("===FRAME SIZE LISTENER")
        self.method_locals = {} # C.m -> locals count

    def enterKlass(self, ctx:coolParser.KlassContext):
        k = classDict[ctx.TYPE(0).getText()]
        ctx.activeClass = k
        # feature nodes know the class they belong to
        for feature in ctx.feature():  
            feature.activeClass = k  
    
    # Enter a parse tree produced by coolParser#let_expr.
    def enterLet_expr(self, ctx:coolParser.Let_exprContext):
        method = getCurrentMethod(ctx)
        method.locals_count += len(ctx.let_decl())

    # Exit a parse tree produced by coolParser#let_expr.
    def exitLet_expr(self, ctx:coolParser.Let_exprContext):
        pass

    def enterFeature_function(self, ctx:coolParser.Feature_functionContext):
        ctx.method_name = ctx.activeClass.name + '.' + ctx.ID().getText()
        ctx.locals_count = 0

    def exitFeature_function(self, ctx:coolParser.Feature_functionContext):
        self.method_locals[ctx.method_name] = ctx.locals_count
    
    def exitProgram(self, ctx:coolParser.ProgramContext):
        # print("Function locals")
        # pprint(self.method_locals)
        pass

    def getMethodLocalsCount(self) -> dict[str,int]:
        return self.method_locals