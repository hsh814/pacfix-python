import random
def my_program(x: int, y: int, z: int) -> int:
    b = x + y
    c = x - y
    res = ""
    res += f"1 {x}\n"
    res += f"2 {y}\n"
    res += f"3 {z}\n"
    res += f"4 {b}\n"
    res += f"5 {c}\n"
    if c == 0:
        return 0, res, True
    if z == 0:
        a = b * b // c
    else:
        a = b // c
    return a, res, False


for i in range(20):
    res_str = ""
    is_crash = False
    for j in range(random.randint(1, 5)):
        a, res, crash = my_program(random.randint(0, 10), random.randint(0, 10), random.randint(0, 1))
        res_str += "[begin]\n" + res + "[end]\n"
        if crash:
            is_crash = True
            break
    if is_crash:
        with open(f"mem/neg/crash_{i}.txt", "w") as f:
            f.write(res_str)
    else:
        with open(f"mem/pos/output_{i}.txt", "w") as f:
            f.write(res_str)
my_program(1, 2, 0)  