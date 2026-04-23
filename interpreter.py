import sys


def load_program(filename):
    prog = []
    f = open(filename, "r")

    lid = 0

    for line in f:
        p = line.strip().split()
        if not p:
            continue

        op = p[0]
        a = p[1]
        b = p[2]
        try:
            t = int(p[3])
            if lid > 0:
                if abs(t - prog[-1][0]) < 6:
                    print(f"{t} : {prog[-1][0]}")
                    print(f"spacing violation at line {lid}")
                    sys.exit()
        except:
            t = int(p[3])

        prog.append([t, lid, op, a, b])
        lid += 1

    f.close()
    return prog


def key(x):
    if x.startswith("@"):
        return x[1:]
    return x


def val(x):
    if isinstance(x, str) and x.startswith("@"):
        try:
            return int(mem.get(x[1:], 0))
        except:
            return mem.get(x[1:], 0)
    try:
        return int(x)
    except:
        return x


def exec_ins(op, a, b):
    A = val(a)
    B = key(b)

    if op == "ADD":
        mem[B] = A + val(b)
        return mem[B], 4
    if op == "SUB":
        mem[B] = A - val(b)
        return mem[B], 4
    if op == "MOV":
        mem[B] = A
        return mem[B], 2
    if op == "NEG":
        mem[B] = -A
        return mem[B], 3
    if op == "INPUT":
        mem[B] = input()
        return mem[B], 2
    if op == "PRINT":
        print(A)
        return A, 2
    
    return 0, 0


mem = {}
totalTime = 100
time = 1
DEBUG = False

prog = load_program("program")

while time < totalTime:
    todo = []
    toadd = 0
    for i in range(len(prog)):
        if val(prog[i][0]) == time:
            todo.append(prog[i])
            if len(todo) == 1:
                try:
                    res = exec_ins(todo[0][2], todo[0][3], todo[0][4])
                    toadd += res[1]
                except:
                    print(f"error with {prog[i]}")
                    sys.exit()
            elif len(todo) >= 2:
                if res[0] < 0:
                    try:
                        res = exec_ins(todo[1][2], todo[1][3], todo[1][4])
                        toadd = 0
                        time = res[0]
                    except:
                        print(
                            f"error at line {prog[i][1]} with {todo[1][2]} {key(todo[1][3])} {key(todo[1][4])}"
                        )
                        sys.exit()
                break
    if DEBUG:
        print(f"time : {time} => {todo}")
    time += toadd
    if len(todo) == 0:
        time += 1
