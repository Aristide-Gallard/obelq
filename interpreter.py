import sys

file = "./examples/calculator.obelq"
DEBUG = False
totalTime = 100


def load_instrs():
    instrList = []
    with open(file, "r") as f:
        lid = 0  # line id

        for line in f:
            p = line.strip().split()  # remove spaces and split in lists

            if not p:
                continue  # to be able to have empty lines

            operation = p[0]
            a = p[1]
            b = p[2]
            try:
                timeS = int(p[3])  # timestamp
                if lid > 0:
                    if abs(timeS - instrList[-1][0]) < 6:  # 6 dif rule
                        print(f"spacing violation at line {lid}")
                        sys.exit()
            except (ValueError, TypeError):
                timeS = p[3]  # variable timestamp

            instrList.append([timeS, lid, operation, a, b])
            lid += 1
    return instrList


def add(A, b): return A + try_read(b), 4
def sub(A, b): return A - try_read(b), 4
def mov(A, _): return A, 2
def neg(A, _): return -A, 3
def inp(_, __):  return input(), 2
# to add another instr add it here and in the dictionary
ops = {
    "ADD": add,
    "SUB": sub,
    "MOV": mov,
    "NEG": neg,
    "INPUT": inp
}

def try_read(var):
    if isinstance(var, str) and var.startswith("@"):
        try:
            return int(mem.get(var[1:], 0))
        except ValueError:
            return mem.get(var[1:], 0)
    try:
        return int(var)
    except ValueError:
        return var


def exec_ins(op, a, b):
    val_a = try_read(a)

    if op == "PRINT":
        print(val_a)
        return val_a, 2

    res, dur = ops[op](val_a, b) # get result and duration of instruction
    if isinstance(b, str) and b.startswith("@"):
        mem[b[1:]] = res # if b is memory variable then store data
    return res, dur


mem = {}
time = 1
useless = 0

instrs = load_instrs()

while time < totalTime:
    instr = []
    toadd = 0
    for i in range(len(instrs)):
        if try_read(instrs[i][0]) == time:
            instr.append(instrs[i])
            if len(instr) == 1:
                res = exec_ins(instr[0][2], instr[0][3], instr[0][4])
                toadd += res[1]

            elif len(instr) >= 2:
                if res[0] < 0:
                    res = exec_ins(instr[1][2], instr[1][3], instr[1][4])
                    toadd = 0
                    time = res[0]
                break
    if DEBUG:
        print(f"time : {time} => {instr}")
    time += toadd
    if len(instr) == 0:
        time += 1
        useless += 1
print(f"you ran {useless} useless iteration")