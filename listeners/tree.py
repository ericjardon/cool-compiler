from antlr.coolListener import coolListener
from antlr.coolListener import TerminalNode

class TreePrinter(coolListener):
    def __init__(self, types={}):
        self.depth = 0
        self.types = types

    def enterEveryRule(self, ctx):
        self.depth = self.depth + 1
        s = ''

        for i in range(self.depth-1):
            s += " "        

        try:
            # Modificar aquí el nombre del atributo que contiene el tipo de dato, para imprimirlo en donde exista en cada
            # nodo del árbol, si es una clase, debe de tener una manera de convertirse a string
            # def __str__(self):
            #     return "foo"
            # si no encuentra el atributo simplement va a escribir el nombre del nodo
            print ("{}{}:{}".format(s, type(ctx).__name__[:-7], ctx.dataType))
        except:
            print ("{}{} UNTYPED".format(s, type(ctx).__name__[:-7]))


    def exitEveryRule(self, ctx):
        self.depth = self.depth - 1

