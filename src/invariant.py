from typing import List, Set, Dict, Tuple, Union
import enum

import utils

class InvariantType(enum.Enum):
    VAR = 0
    CONST = 1
    EQ = 2
    NE = 3
    GT = 4
    GE = 5
    LT = 6
    LE = 7
    ADD = 8
    SUB = 9
    MUL = 10
    DIV = 11

INVARIANT_MAP = { InvariantType.VAR: "VAR", InvariantType.CONST: "CONST", InvariantType.EQ: "==", InvariantType.NE: "!=", InvariantType.GT: ">", InvariantType.GE: ">=", InvariantType.LT: "<", InvariantType.LE: "<=", InvariantType.ADD: "+", InvariantType.SUB: "-", InvariantType.MUL: "*", InvariantType.DIV: "/"}

class Relation(enum.Enum):
    GT = 1
    EQ = 0
    LT = -1

class Invariant():
    inv_type: InvariantType
    data: int
    left: 'Invariant'
    right: 'Invariant'
    
    def __init__(self, inv_type: InvariantType, left: 'Invariant' = None, right: 'Invariant' = None, data: int = 0):
        self.inv_type = inv_type
        if inv_type == InvariantType.VAR or inv_type == InvariantType.CONST:
            self.data = data
            self.left = None
            self.right = None
        else:
            self.left = left
            self.right = right
            self.data = 0
    
    def __str__(self) -> str:
        if self.inv_type == InvariantType.VAR:
            return f"VAR({self.data})"
        elif self.inv_type == InvariantType.CONST:
            return f"CONST({self.data})"
        else:
            return f"({self.left} {INVARIANT_MAP[self.inv_type]} {self.right})"

    def __repr__(self) -> str:
        return str(self)
    
    def to_str(self, lv: Dict[int, utils.LiveVariable]) -> str:
        if self.inv_type == InvariantType.VAR:
            return lv[self.data].name
        elif self.inv_type == InvariantType.CONST:
            return str(self.data)
        else:
            return f"({self.left.to_str(lv)} {INVARIANT_MAP[self.inv_type]} {self.right.to_str(lv)})"
    
    def compare(self, other: 'Invariant') -> Relation:
        return Relation.EQ

class InvariantVisitor():
    def __init__(self):
        pass
    
    def visit(self, inv: Invariant):
        if inv.inv_type == InvariantType.VAR:
            self.visit_var(inv)
        elif inv.inv_type == InvariantType.CONST:
            self.visit_const(inv)
        else:
            self.visit_operation(inv)
    
    def visit_var(self, inv: Invariant):
        pass
    
    def visit_const(self, inv: Invariant):
        pass
    
    def visit_operation(self, inv: Invariant):
        if inv.left:
            self.visit(inv.left)
        if inv.right:
            self.visit(inv.right)

class VariableCollector(InvariantVisitor):
    variables: Set[int]
    def __init__(self):
        self.variables = set()
    
    def visit_var(self, inv: Invariant):
        self.variables.add(inv.data)
    
    def get_vars(self) -> Set[int]:
        return self.variables

class Lattice:
    inv: Invariant
    id: int
    parent: Set[int]
    children: Set[int]

    def __init__(self, inv: Invariant, id: int):
        self.inv = inv
        self.id = id
        self.parent = set()
        self.children = set()
    
    def add_parent(self, parent_id: int):
        self.parent.add(parent_id)
    
    def add_child(self, child_id: int):
        self.children.add(child_id)
    
    def get_parent(self) -> Set[int]:
        return self.parent
    
    def get_children(self) -> Set[int]:
        return self.children


class InvariantManager():
    invs: List[Invariant]
    lattice_map: Dict[int, Lattice]
    def __init__(self):
        self.invs = list()
    
    def add_invariant(self, inv: Invariant) -> int:
        self.invs.append(inv)
        return len(self.invs) - 1
    
    def get_invariant_by_id(self, id: int) -> List[Invariant]:
        if id < 0 or id >= len(self.invs):
            return None
        return self.invs[id]
    
    def add_invariant_to_lattice_recursive(self, parent: Lattice, inv: Lattice):
        for c in parent.get_children():
            pass
    
    def add_invariant_to_lattice(self, inv: Invariant) -> int:
        inv_id = self.add_invariant(inv)
        lattice = Lattice(inv, inv_id)
        vars = VariableCollector()
        vars.visit(inv)
        for var in vars.get_vars():
            # Get lattice that contains the variable
            if var in self.lattice_map:
                l = self.lattice_map[var]
                self.add_invariant_to_lattice_recursive(l, lattice)
            else:
                # Create a new lattice
                self.lattice_map[var] = lattice
        return inv_id