from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import *
from util.structure import _allClasses as classDict
from antlr4.tree.Tree import ParseTree

def getCurrentMethod(ctx: ParseTree) -> ParseTree:
    parent = ctx.parentCtx
    while (parent and not hasattr(parent, 'locals_count')):
        parent = parent.parentCtx
    print("Current method is", type(parent))
    return parent

class frameSize(coolListener):
    '''
    Responsible for traversing methods' bodies and counting
    number of local variables (let) to determine necessary space for 
    locals for every method
    '''

    def __init__(self) -> None:
        print("===FRAME SIZE LISTENER")
    
    # Enter a parse tree produced by coolParser#let_expr.
    def enterLet_expr(self, ctx:coolParser.Let_exprContext):
        method = getCurrentMethod(ctx)
        method.locals_count += len(ctx.let_decl())

    # Exit a parse tree produced by coolParser#let_expr.
    def exitLet_expr(self, ctx:coolParser.Let_exprContext):
        pass

    # Enter a parse tree produced by coolParser#method_call.
    def enterMethod_call(self, ctx:coolParser.Method_callContext):
        ctx.locals_count = 0

    # Exit a parse tree produced by coolParser#method_call.
    def exitMethod_call(self, ctx:coolParser.Method_callContext):
        print("Method locals_count=", ctx.locals_count)