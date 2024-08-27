import os
import enum

from typing import List, Set, Dict, Tuple

def get_valuations(input_dir: str) -> List[str]:
    valuations = list()
    for file in os.listdir(input_dir):
        with open(os.path.join(input_dir, file), "r") as f:
            valuations.append(f.read())
    return valuations

def parse_valuation(valuations: List[str]) -> List[Dict[int, int]]:
    vals = list()
    seen = set()
    for valuation in valuations:
        if valuation in seen:
            continue
        seen.add(valuation)
        val_map = dict()
        for line in valuation.split("\n"):
            if len(line) > 2:
                id, val = line.split()
                val_map[int(id)] = int(val)
        vals.append(val_map)
    return vals

class VarType(enum.Enum):
    INT = 0
    BOOL = 1
    PTR = 2

class LiveVariable():
    id: int
    name: str
    var_type: VarType
    def __init__(self, id: int, name: str, var_type: str):
        self.id = id
        self.name = name
        if var_type == "int":
            self.var_type = VarType.INT
        elif var_type == "bool":
            self.var_type = VarType.BOOL
        else:
            self.var_type = VarType.PTR


def get_live_vars(live_vars_file: str) -> Dict[int, LiveVariable]:
    live_vars = dict()
    with open(live_vars_file, "r") as f:
        for line in f:
            line = line.strip()
            if len(line) > 2:
                id, name, var_type = line.split()
                live_vars[int(id)] = LiveVariable(int(id), name, var_type)
    return live_vars

