class SymbolTable:
    counter = {'FIELD': 0, 'STATIC': 0, 'ARG': 0, 'VAR': 0}

    def __init__(self):
        self.counter['FIELD'] = 0
        self.fieldScope = {}
        self.staticScope = {}
        self.subroutineScope = {}

    def startSubroutine(self):
        self.subroutineScope.clear()
        self.counter['ARG'] = 0
        self.counter['VAR'] = 0

    def define(self, name, type, kind):
        if kind == 'FIELD':
            self.fieldScope[name] = (type, kind, self.counter[kind])
            self.counter[kind] += 1
        elif kind == 'STATIC':
            self.staticScope[name] = (type, kind, self.counter[kind])
            self.counter[kind] += 1
        elif kind == 'ARG':
            self.subroutineScope[name] = (type, kind, self.counter[kind])
            self.counter[kind] += 1
        elif kind == 'VAR':
            self.subroutineScope[name] = (type, kind, self.counter[kind])
            self.counter[kind] += 1

    def VarCount(self, kind):
        return self.counter[kind]

    def KindOf(self, name):
        if name in self.subroutineScope.keys():
            return self.subroutineScope[name][1]
        elif name in self.fieldScope.keys():
            return self.fieldScope[name][1]
        elif name in self.staticScope.keys():
            return self.fieldScope[name][1]
        else:
            return 'NONE'

    def TypeOf(self, name):
        if name in self.subroutineScope.keys():
            return self.subroutineScope[name][0]
        elif name in self.fieldScope.keys():
            return self.fieldScope[name][0]
        elif name in self.staticScope.keys():
            return self.fieldScope[name][0]
        else:
            return 'NONE'

    def IndexOf(self, name):
        if name in self.subroutineScope.keys():
            return self.subroutineScope[name][2]
        elif name in self.fieldScope.keys():
            return self.fieldScope[name][2]
        elif name in self.staticScope.keys():
            return self.fieldScope[name][2]
        else:
            return 'NONE'
