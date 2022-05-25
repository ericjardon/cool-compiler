from antlr.marzoListener import marzoListener
from antlr.marzoParser import marzoParser

class Addressing(marzoListener):
    def __init__(self):
        self.symbolTable = {}
        self.locals = 0
        self.params = 0

    def exitVar(self, ctx: marzoParser.VarContext):
        if not self.symbolTable.__contains__(ctx.getText()):
            self.symbolTable[ctx.getText()] = self.locals
            self.locals = self.locals - 1
            
        ctx.offset = self.symbolTable[ctx.getText()] * 4
    
    def enterProcedure(self, ctx: marzoParser.ProcedureContext):
        for c in ctx.Variable()[1::]:
            if not self.symbolTable.__contains__(c.getText()):
                self.params = self.params + 1
                self.symbolTable[c.getText()] = self.params

    def exitProcedure(self, ctx: marzoParser.ProcedureContext):
        ctx.params = self.params
        ctx.locals = abs(self.locals)

        self.params = 0
        self.locals = 0
        self.symbolTable = {}
    
    def exitAsignacion(self, ctx: marzoParser.AsignacionContext):
        var = ctx.getChild(0)
        if not self.symbolTable.__contains__(var.getText()):            
            self.symbolTable[var.getText()] = self.locals
            self.locals = self.locals - 1

        var.offset = self.symbolTable[var.getText()] * 4