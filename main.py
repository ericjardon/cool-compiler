from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser

from listeners.basicSemanticCheck import basicSemanticListener
from listeners.structureBuilder import structureBuilder
from listeners.featuresBuilder import featuresBuilder
from listeners.typeChecker import typeChecker
from listeners.tree import TreePrinter
from listeners.dataSegment import dataSegment
from listeners.frameSize import frameSize
from listeners.codeGenerator import codeGenerator

OUT_FILE = lambda x : f'out{x}.asm'
test_counter = 0

def compile(file, treeprinter=False):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()
    
    walker.walk(basicSemanticListener(), tree)
    
    walker.walk(structureBuilder(), tree)  # build the allClasses dict, sets inheritance

    walker.walk(featuresBuilder(), tree)  # add feature methods and attributes

    walker.walk(typeChecker(), tree)
    
    if treeprinter:
        walker.walk(TreePrinter(), tree)

    dotData = dataSegment()
    dotText = codeGenerator()
    walker.walk(dotData, tree)
    #walker.walk(frameSize(), tree) determine frame size in every procedure call
    walker.walk(dotText, tree)

    with open(OUT_FILE(test_counter), "w") as writer:
        writer.write(dotData.result)
        writer.write(dotText.result)
    writer.close()

def dummy():
    raise SystemExit(1)

if __name__ == '__main__':
    compile('./resources/codegen/input/example.cl') 
