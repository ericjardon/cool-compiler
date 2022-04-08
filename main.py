from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser

from listeners.dummy import dummyListener

def compile(file):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()
    
    walker.walk(dummyListener(), tree)


def dummy():
    raise SystemExit(1)

if __name__ == '__main__':
    compile('semantic/input/anattributenamedself.cool')
