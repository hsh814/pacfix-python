import os
import enum
import math

from typing import List, Set, Dict, Tuple

def get_valuations(input_dir: str) -> List[str]:
    valuations = list()
    for file in os.listdir(input_dir):
        with open(os.path.join(input_dir, file), "r") as f:
            valuations.append(f.read())
    return valuations

# parse valuation and returns neg, pos valuations
def parse_valuation(neg: List[str], pos: List[str]) -> Tuple[List[Dict[int, int]], List[Dict[int, int]]]:
    neg_vals = list()
    pos_vals = list()
    for valuation in neg:
        groups: List[Dict[int, int]] = list()
        in_group = False
        val_map = dict()
        for line in valuation.split("\n"):
            if line.startswith("#") or len(line) < 3:
                continue
            if line.startswith("[begin]"):
                in_group = True
                val_map = dict()
            elif line.startswith("[end]"):
                in_group = False
                groups.append(val_map)                
            elif in_group:
                id, val = line.split()
                val_map[int(id)] = int(val)
        # Only last one is negative
        for i in range(len(groups)):
            val_map = groups[i]
            if i < len(groups) - 1:
                pos_vals.append(val_map)
            else:
                neg_vals.append(val_map)
    for valuation in pos:
        groups: List[Dict[int, int]] = list()
        in_group = False
        val_map = dict()
        for line in valuation.split("\n"):
            if line.startswith("#") or len(line) < 3:
                continue
            if line.startswith("[begin]"):
                in_group = True
                val_map = dict()
            elif line.startswith("[end]"):
                in_group = False
                groups.append(val_map)                
            elif in_group:
                id, val = line.split()
                val_map[int(id)] = int(val)
        for val_map in groups:
            pos_vals.append(val_map)
    return neg_vals, pos_vals

def parse_valuations_uni(neg: List[str], pos: List[str]) -> List[Dict[int, int]]:
    neg_vals = list()
    pos_vals = list()
    for valuation in neg:
        groups: List[Dict[int, int]] = list()
        val_map = dict()
        for line in valuation.split("\n"):
            if line.startswith("#") or len(line) < 3:
                continue
            if line.startswith("----------------------------"):
                groups.append(val_map)
                val_map = dict() 
            elif line.startswith("__valuation:"):
                value_str = line.removeprefix("__valuation:").strip()
                tokens = value_str.split()
                id = tokens[4].strip()
                val = tokens[5].strip()
                val_map[int(id)] = int(val)
        # Only last one is negative
        for i in range(len(groups)):
            val_map = groups[i]
            if i < len(groups) - 1:
                pos_vals.append(val_map)
            else:
                neg_vals.append(val_map)
    for valuation in pos:
        groups: List[Dict[int, int]] = list()
        in_group = False
        val_map = dict()
        for line in valuation.split("\n"):
            if line.startswith("#") or len(line) < 3:
                continue
            if line.startswith("----------------------------"):
                groups.append(val_map)
                val_map = dict() 
            elif line.startswith("__valuation:"):
                value_str = line[len("__valuation:"):].strip()
                tokens = value_str.split()
                id = tokens[4].strip()
                val = tokens[5].strip()
                val_map[int(id)] = int(val)
        for val_map in groups:
            pos_vals.append(val_map)
    return neg_vals, pos_vals

def filter_duplicate(valuations: List[Dict[int, int]]) -> List[Dict[int, int]]:
    seen = set()
    result = list()
    for val in valuations:
        key = frozenset(val.items())
        if key not in seen:
            seen.add(key)
            result.append(val)
    return result

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
    
    def __str__(self):
        return f"LiveVariable(id={self.id}, name={self.name}, var_type={self.var_type})"
    
    def __repr__(self):
        return self.__str__()


def get_live_vars(live_vars_file: str) -> Dict[int, LiveVariable]:
    live_vars = dict()
    with open(live_vars_file, "r") as f:
        for line in f:
            line = line.strip()
            if len(line) > 2:
                id, name, var_type = line.split()
                live_vars[int(id)] = LiveVariable(int(id), name, var_type)
    return live_vars


def get_lv_file(lv_file: str) -> Set[str]:
    live_vars = set()
    with open(lv_file, "r") as f:
        for line in f:
            if len(line.strip()) > 0:
                live_vars.add(line.strip())
    return live_vars

def calculate_pac(samples: int, hypothesis_space: int, delta: float) -> float:
    if hypothesis_space == 0 or samples == 0:
        return 0
    return (1 / samples) * (math.log(hypothesis_space) + (math.log(1 / delta)))