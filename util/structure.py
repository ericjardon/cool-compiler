from _collections_abc import MutableMapping
from collections import OrderedDict
import unittest
from pprint import pprint
from typing import List, Tuple

_allClasses = {}

class HierarchyException(Exception):
    pass

def lookupClass(name):
    return _allClasses[name]


class Method():
    """
    Se usa una tabla de símbolos lineal para
    almacenar los tipos de los parámetros.
    """
    def __init__(self, type, params=None):
        self.type = type
        self.params = SymbolTable()
        if params:
            for x, y in params:
                self.params[x] = y
    # TODO: Maybe add a compareTo method, so it is not limited to object reference.

class Klass():
    """
    Agrupación de features (atributos y métodos).
    """

    # Ojo, variable de clase no de instancia
    # para encontrar la clase de la que hereda

    def __init__(self, name, inherits="Object"):

        self.name = name
        self.inherits = inherits
        if self.name != "Object":
            self.validHierarchy()

        self.attributes = SymbolTable()  # nombre -> tipo, strings
        self.methods = SymbolTable()  # nombre -> Method()
        _allClasses[name] = self

    def setInherits(self, inherits):
        self.inherits = inherits
        if self.name != "Object":
            self.validHierarchy()

    def validHierarchy(self):
        up = self.inherits
        # Buscar hacia arriba hasta llegar a object
        while up != "Object":
            # Si encuentro la clase que estoy definiendo -> ciclo
            if up == self.name:
                raise HierarchyException
            up = _allClasses[up].inherits

    def addAttribute(self, name, type=None):
        try:
            # Busco el atributo, si no está (excepción), puedo agregarlo
            self.lookupAttribute(name)
            raise KeyError(name)
        except KeyError:
            self.attributes[name] = type

    def addMethod(self, name, method):
        self.methods[name] = method

    def lookupAttribute(self, name):
        """
        Buscar un atributo en una clase, si no se encuentra, resolver
        por herencia (hasta Object donde da error si no está el attributo)
        """
        if name in self.attributes:
            return self.attributes[name]
        elif self.name == "Object":
            raise KeyError(name)
        else:
            return _allClasses[self.inherits].lookupAttribute(name)

    def lookupMethod(self, name: str) -> Method:
        if name in self.methods:
            return self.methods[name]
        elif self.name == "Object":
            raise KeyError(name)
        else:
            return _allClasses[self.inherits].lookupMethod(name)

    def getAvailableMethods(self, stack) -> list[str]:
        """
        Returns a stack containing the names of all methods including
        inherited ones in "Class.method" format
        Popping until emtpy gives the sequence of declared
        methods in top-down order.
        """
        for method in self.methods.keys():
                stack.append(self.name+"."+method)
        if self.name == "Object":
            return stack
        else:
            return _allClasses[self.inherits].getAvailableMethods(stack)
    
    def getavailableAttributes(self, stack) -> list[str]:
        """
        Returns a stack containing the types of all attributes including
        inherited ones. Popping until emtpy gives the sequence of declared
        attributes in top-down order.
        """
        for attr_type in self.attributes.values():
            stack.append(attr_type)
        if self.name=="Object":
            return stack
        else:
            return _allClasses[self.inherits].getAvailableAttributes(stack) 

    def getBaseAttributesCount(self, count=None):
        """
        Returns a dictionary of the counts of attributes of each Base Class type,
        including inherited ones.
        """
        if count is None:
            count = {
                'Int':0,
                'String':0,
                'Bool':0
            }
        
        for a in self.attributes.values():
            if a in count:
                count[a] += 1
        
        if self.name == "Object":
            return count

        return _allClasses[self.inherits].getBaseAttributesCount(count)


    def conforms(self, B):
        """
        Return True if B conforms to this class, False otherwise.
        If B conforms to this (B <= self), then we can assign an instance of B to a variable of this class type.
        tldr; checks if this class is an ancestor of B
        """
        if B.name == self.name:  # any class conforms to itself
            return True
        if B.name == 'Object':
            return False
        else:
            return self.conforms(lookupClass(B.inherits))
    
    def conformsTo(self, B):
        """
        Return True if this class conforms to B, False otherwise.
        If this class conforms to B, we can assign an instance of this class to a variable of type B.
        tldr; checks if B is an ancestor of this class.
        """
        if self.name == B.name:
            return True
        if self.name == 'Object':
            return False
        
        # Recursively look up the tree.
        return _allClasses[self.inherits].conformsTo(B)
        
class SymbolTable(MutableMapping):
    """
    La diferencia entre una tabla de símbolos y un dict es que si la
    llave ya está en la tabla, entonces se debe lanzar excepción.
    """
    def __init__(self):
        self.dict = OrderedDict()

    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        """Aquí, si key ya está, regresar excepción"""
        if key in self.dict:
            raise KeyError(key)
        self.dict[key] = value 

    def __delitem__(self, key):
        del self.dict[key]

    def __iter__(self):
        return iter(self.dict)

    def __len__(self):
        return len(self.dict)

    def __repr__(self):
        return self.dict.__repr__()


class SymbolTableWithScopes(MutableMapping):
    """
    Esta versión de tabla de símbolos maneja scopes mediante una pila,
    guarda en el scope activo y busca en los superiores.
    """
    def __init__(self, klass: Klass):
        self.dict_list = [{}]
        self.last = 0
        self.klass = klass
    
    def __getitem__(self, key):
        for i in reversed(range(self.last+1)):
            if key in self.dict_list[i].keys():
                return self.dict_list[i][key]
        # If it is not in any of the scopes, look in class definition
        return self.klass.lookupAttribute(key)
        # Never reached
        raise KeyError(key)

    def __setitem__(self, key, value):
        if key in self.dict_list[self.last]:
            raise KeyError(key)
        self.dict_list[self.last][key] = value

    def __delitem__(self, key):
        del self.dict_list[self.last][key]

    def __iter__(self):
        return iter(self.dict_list[self.last])

    def __len__(self):
        return len(self.dict_list[self.last])

    def closeScope(self):
        self.dict_list.pop()
        self.last = self.last - 1

    def openScope(self):
        self.dict_list.append({})
        self.last = self.last + 1

    def __repr__(self):
        return self.dict_list.__repr__()

class PruebasDeEstructura(unittest.TestCase):
    def setUp(self):
        Klass("Object", None)  # so Object class exists in class store
        self.k = [Klass("A"), Klass("B", "A"), Klass("C", "B"), Klass("Z", "B")]

    def test1(self):
        self.k[0].addAttribute("a", "Integer")
        self.assertTrue(self.k[0].lookupAttribute("a") == "Integer")

    # Búsqueda por herencia
    def test2(self):
        self.k[0].addAttribute("a", "Integer")
        self.assertTrue(self.k[1].lookupAttribute("a") == "Integer")
        self.assertTrue(self.k[2].lookupAttribute("a") == "Integer")
        self.k[1].addAttribute("b", "String")
        self.assertTrue(self.k[2].lookupAttribute("b") == "String")

    def test3(self):
        with self.assertRaises(KeyError):
            self.k[3].lookupAttribute("z")

    def test4(self):
        m1 = Method("Integer")
        m2 = Method("String", [("a", "Integer"), ("b", "Boolean")])
        self.k[0].addMethod("test", m1)
        self.k[1].addMethod("test2", m2)
        self.assertTrue(self.k[0].lookupMethod("test") == m1)
        self.assertTrue(self.k[2].lookupMethod("test") == m1)
        self.assertTrue(self.k[1].lookupMethod("test2") == m2)

    def test5(self):
        with self.assertRaises(HierarchyException):
            z = Klass("A", "C")

    def test6(self):
        self.assertTrue(lookupClass("A") == self.k[0])

    def test7(self):
        self.assertTrue(self.k[0].conforms(self.k[2]))
        self.assertFalse(self.k[2].conforms(self.k[1]))

class PruebasConTablaLineal(unittest.TestCase):
    # Corre antes de cada método de prueba
    def setUp(self):
        self.st = SymbolTable()

    # Corre después de cada método de prueba
    def tearDown(self):
        self.st = None

    def test1(self):
        self.assertFalse('a' in self.st.keys())

    def test2(self):
        self.st['hola'] = 'mundo1'
        self.assertTrue('hola' in self.st.keys())
        self.assertTrue(self.st['hola'] == 'mundo1')

    def test3(self):
        with self.assertRaises(KeyError):
            self.st['hola']

    def test4(self):
        self.st['hola'] = 'mundo'
        with self.assertRaises(KeyError):
            self.st['hola'] = 'mundo'

class PruebasConScopes(unittest.TestCase):
    def setUp(self):
        k = Klass("Object", None)
        self.st = SymbolTableWithScopes(k)

    def tearDown(self):
        self.st = None

    def test1(self):
        self.assertFalse('a' in self.st.keys())

    def test2(self):
        self.st['hola'] = 'mundo1'
        self.assertTrue('hola' in self.st.keys())
        self.assertTrue(self.st['hola'] == 'mundo1')

    def test3(self):
        self.st['hola'] = 'mundo2'
        self.assertTrue('mundo2' in self.st.values())

    def test4(self):
        self.st['hola'] = 'mundo3'
        self.assertEqual('mundo3', self.st['hola'])

    def test5(self):
        with self.assertRaises(KeyError):
            self.st['hola']

    def test6(self):
        self.st.openScope()
        self.st['hola'] = 'mundo1'
        self.st.closeScope()
        self.assertFalse('hola' in self.st)

    def test7(self):
        self.st['hola'] = 'scope0'
        self.st.openScope()
        self.st['hola'] = 'scope1'
        self.st.openScope()
        self.st['hola'] = 'scope2'
        self.assertEqual(self.st['hola'], 'scope2')
        self.st.closeScope()
        self.assertEqual(self.st['hola'], 'scope1')
        self.st.closeScope()
        self.assertEqual(self.st['hola'], 'scope0')

class BaseKlasses(unittest.TestCase):
    def setUp(self):
        setBaseKlasses()
    
    def tearDown(self) -> None:
        _allClasses = {}
    
    def test1(self):
        io = lookupClass('IO')
        m = io.lookupMethod('out_int')        
        self.assertTrue(m.type, 'Int')

    def test2(self):
        str = lookupClass('String')
        m = str.lookupMethod('substr')
        self.assertTrue(m.params['l'], 'Int')

def getLCA(klasses: List[str]):
    '''Returns the Least Common Ancestor of an arbitrary number 
        of Klasses, provided len>0'''
    print("Get LCA of", klasses)
    lca = lookupClass(klasses[0])

    for i in range(1, len(klasses)):
        lca_name = getLeastCommonAncestor(lca, lookupClass(klasses[i]))
        lca = lookupClass(lca_name)
    print("LCA:", lca.name)
    return lca

def getLeastCommonAncestor(class_one: Klass, class_two:Klass) -> str:
    '''Get all ancestors of class one into a set.
    For all ancestors of class two, return the first klass
    in the class one ancestors set'''

    if class_one.name == 'Object' or class_two.name == 'Object':
        return 'Object'

    ancestors = set()
    ancestors.add('Object')

    c = class_one
    while c.name != 'Object':
        ancestors.add(c.name)
        c = lookupClass(c.inherits)
    
    c = class_two
    while c.name != 'Object':
        if c.name in ancestors:
            return c.name
        c = lookupClass(c.inherits)
    
    return 'Object'


# def getLeastCommonAncestor(class_one, class_two):
#     class_one_path = set()
#     class_two_path = set()
    
#     intersection = class_one_path.intersection(class_two_path)
    
#     while len(intersection) < 1:
#         class_one_path.add(class_one.name)
#         class_one = lookupClass(class_one.inherits)
        
#         class_two_path.add(class_two.name)
#         class_two = lookupClass(class_two.inherits)
        

#         intersection = class_one_path.intersection(class_two_path)

#     return intersection.pop()

'''
Mandar llamar a setBaseKlasses() para crear las declaraciones de las 5 clases básicas
'''
def setBaseKlasses():
    k = Klass('Object')
    k.addMethod('abort', Method('Object'))
    k.addMethod('type_name', Method('Object'))
    k.addMethod('copy', Method('SELF_TYPE'))
    
    k = Klass('IO')
    k.addMethod('out_string', Method('SELF_TYPE', [('x', 'String')]))
    k.addMethod('out_int', Method('SELF_TYPE', [('x', 'Int')]))
    k.addMethod('in_string', Method('String'))
    k.addMethod('in_int', Method('Int'))
    
    k = Klass('Int')
    
    k = Klass('String')
    k.addMethod('length', Method('Int'))
    k.addMethod('concat', Method('String', [('s', 'String')]))
    k.addMethod('substr', Method('String', [('i', 'Int'), ('l', 'Int')]))
    
    k = Klass('Bool')
    

if __name__ == '__main__':
    unittest.main(verbosity=2)
    '''Para correr estas pruebas unitarias se puede simplemente pytest structure.py
       Pytest las encuentra aunque están hechas al estilo unittest! Qué bonito es Python ;,,,,D
    '''