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

