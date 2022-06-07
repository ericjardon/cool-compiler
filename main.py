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
from pprint import pprint
import traceback
import sys

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
    walker.walk(dotData, tree)

    frameSizeListener = frameSize()
    walker.walk(frameSizeListener, tree) 

    print("--registered ints--")
    pprint(dotData.registered_ints)
    print("--registered strings--")
    pprint(dotData.registered_strings)
    print("--method locals--")
    pprint(frameSizeListener.method_locals)
    
    dotText = codeGenerator(
        registered_ints=dotData.registered_ints,
        registered_strings=dotData.registered_strings,
        method_locals=frameSizeListener.method_locals
    )
    try:
        walker.walk(dotText, tree)
    except AttributeError as e:
        print(traceback.format_exc())
        raise AttributeError

    with open(OUT_FILE(test_counter), "w") as writer:
        writer.write(dotData.result)
        writer.write(dotText.result)
    writer.close()

def dummy():
    raise SystemExit(1)

if __name__ == '__main__':
    compile('./resources/codegen/input/example.cl') 
