class SymbolTable:

    def __init__(self):
        self.var = 0
        self.arg = 0
        self.field = 0
        self.static = 0
        self.fieldScope = {}
        self.currentScope = self.fieldScope
        self.subroutineScope = {}
        self.whileCounter = 0
        self.ifCounter = 0

    def startSubroutine(self, name):
        self.subroutineScope[name] = {}
        self.var = 0
        self.arg = 0
        self.whileCounter = 0
        self.ifCounter = 0

    def define(self, name, type, kind):
        type = type.upper()
        name = name.upper()
        kind = kind.upper()
        if kind == 'FIELD':
            self.fieldScope[name] = (type, kind, self.field)
            self.field += 1
        elif kind == 'STATIC':
            self.fieldScope[name] = (type, kind, self.static)
            self.static += 1
        elif kind == 'ARG':
            self.currentScope[name] = (type, kind, self.arg)
            self.arg += 1
        elif kind == 'VAR':
            self.currentScope[name] = (type, kind, self.var)
            self.var += 1

    def VarCount(self, kind):
        kind = kind.upper()
        return len([value for (item, value) in self.currentScope.items() if value[1] == kind])

    def ClassCount(self, kind):
        kind = kind.upper()
        return len([value for (item, value) in self.fieldScope.items() if value[1] == kind])

    def KindOf(self, name):
        name = name.upper()
        if name in self.currentScope:
            return self.currentScope[name][1]
        if name in self.fieldScope:
            return self.fieldScope[name][1]
        else:
            return 'None'

    def TypeOf(self, name):
        name = name.upper()
        if name in self.currentScope:
            return self.currentScope[name][0]
        if name in self.fieldScope:
            return self.fieldScope[name][0]
        else:
            return 'None'

    def IndexOf(self, name):
        name = name.upper()
        if name in self.currentScope:
            return self.currentScope[name][2]
        if name in self.fieldScope:
            return self.fieldScope[name][2]
        else:
            return 'None'

    def scaleScope(self, scope):
        if scope == 'field':
            self.currentScope = self.fieldScope
        else:
            self.currentScope = self.subroutineScope[scope]
