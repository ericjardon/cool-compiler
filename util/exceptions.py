class anattributenamedself(Exception):
    pass

class assignnoconform(Exception):
    pass

class attrbadinit(Exception):
    pass

class attroverride(Exception):
    pass

class badargs1(Exception):
    pass

class badarith(Exception):
    pass

class baddispatch(Exception):
    pass

class badequalitytest(Exception):
    pass

class badequalitytest2(Exception):
    pass

class badmethodcallsitself(Exception):
    pass

class badredefineint(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Bad redefinition of class 'Int'")

class badstaticdispatch(Exception):
    pass

class badwhilebody(Exception):
    pass

class badwhilecond(Exception):
    pass

class caseidenticalbranch(Exception):
    pass

class dupformals(Exception):
    pass

class inheritsbool(Exception):
    pass

class inheritsselftype(Exception):
    pass

class inheritsstring(Exception):
    pass

class letself(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Let declaration of keyword 'self'")
    

class letbadinit(Exception):
    pass

class lubtest(Exception):
    pass

class missingclass(Exception):
    pass

class nomain(Exception):
    pass

class outofscope(Exception):
    pass

class overridingmethod4(Exception):
    pass

class signaturechange(Exception):
    pass

class redefinedclass(Exception):
    pass

class redefinedobject(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Bad redefinition of class 'Object'")

class returntypenoexist(Exception):
    pass

class selfassignment(Exception):
    pass

class selfinformalparameter(Exception):
    pass

class selftypebadreturn(Exception):
    pass

class selftypeparameterposition(Exception):
    pass

class selftyperedeclared(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Bad redefinition of SELF_TYPE")

class trickyatdispatch2(Exception):
    pass
