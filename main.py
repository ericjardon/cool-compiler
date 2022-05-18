from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser

from listeners.basicSemanticCheck import basicSemanticListener
from listeners.structureBuilder import structureBuilder
from listeners.featuresBuilder import featuresBuilder
from listeners.typeChecker import typeChecker
from listeners.tree import TreePrinter

def compile(file):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()
    
    walker.walk(basicSemanticListener(), tree)
    
    walker.walk(structureBuilder(), tree)  # build the allClasses dict, sets inheritance

    walker.walk(featuresBuilder(), tree)  # add feature methods and attributes

    walker.walk(typeChecker(), tree)
    
        
    walker.walk(TreePrinter(), tree)

def dummy():
    raise SystemExit(1)

if __name__ == '__main__':
    compile('resources/semantic/input/hairyscary.cool')
