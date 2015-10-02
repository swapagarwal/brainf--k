#!/usr/bin/env python

import sys

cells = [0]*30000
ptr = 0

def inc_pointer():
    """ Increment the position of the data pointer. """
    global ptr
    ptr += 1

def dec_pointer():
    """ Decrement the position of the data pointer. """
    global ptr
    ptr -= 1

def inc_byte():
    """ Increment the byte at the pointer by 1. """
    global ptr
    cells[ptr] = (cells[ptr] + 1) % 256

def dec_byte():
    """ Decrement the byte at the pointer by 1. """
    global ptr
    cells[ptr] = (cells[ptr] - 1) % 256

def output_byte():
    global ptr
    sys.stdout.write(chr(cells[ptr]))

def input_byte():
    global ptr
    c = ord(sys.stdin.read(1))
    cells[ptr] = c

handle_directly = {
    ">" : inc_pointer,
    "<" : dec_pointer,
    "+" : inc_byte,
    "-" : dec_byte,
    "." : output_byte,
    "," : input_byte,
}

def parse(code):
    """ Manage loops in source with [ and ]. """
    opening = []
    loop = {}
    for i,c in enumerate(code):
        if c == "[":
            opening.append(i)
        elif c == "]":
            begin = opening.pop()
            loop[begin] = i
    return loop

def eval_bf(code):
    """ Call correct functions based upon source code. """
    global ptr
    loop = parse(code)
    pc = 0
    stack = []
    while pc < len(code):
        instruction = code[pc]
        if instruction in handle_directly:
            apply(handle_directly[instruction])
        elif instruction == "[":
            if cells[ptr] > 0:
                stack.append(pc)
            else:
                pc = loop[pc]
        elif instruction == "]":
            pc = stack.pop() - 1
        pc += 1

def reset():
    global cells, ptr
    cells = [0]*30000
    ptr = 0

def interactive():
    print """Welcome to the brainf**k Interpreter.
Type (or paste) your program at the "$ " prompt.
Type 'run' on an empty line to evaluate your program.
Type 'reset' on an empty line to reset. (set all cells to 0)
Type 'quit' on an empty line to quit.
"""
    code = ""
    while True:
        line = str(raw_input("$ "))
        if line == "reset":
            reset()
            code = ""
        elif line == "run":
            sys.stdout.write("\n")
            eval_bf(code)
            sys.stdout.write("\n")
            code = ""
        elif line == "quit":
            return
        else:
            code += line

if __name__ == "__main__":
    interactive()
