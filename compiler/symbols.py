class Var:

    def __init__(self, id, name, type, value):
        self.id = id
        self.name = name
        self.type = type
        self.value = value

    def __del__(self):
      class_name = self.__class__.__name__
      print class_name, self.name, "destroyed"

    def clear(self):
        self.id = -1
        self.name = ""
        self.type = 0
        self.value = None

    def __str__(self):
        return 'Variable (%s, %d)' % (self.name, self.type)

class SymbolTable:

    def __init__(self):
        self.vars = {}
        self.parent_table = None
        self.children_tables = []

    def create_child_table(self):
        new_table = SymbolTable()
        new_table.parent_table = self
        self.children_tables.append(new_table)
        return new_table

    def children_count(self):
        return len(self.children_tables)

    def insert(self, name):
        if self.lookup(name):
            print "Variable", name, "is already declared"
        else:
            self.vars[name] = Var(0, name, type, None)
            return self.vars[name]
        return 0

    def lookup(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent_table is not None and self.parent_table.lookup(name):
            return self.parent_table.lookup(name)
        else:
            # Symbol does not exist
            print "Variable", name, "not declared"
            return 0
