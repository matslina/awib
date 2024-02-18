#!/usr/bin/python

import sys

ADD = 1
INPUT = 2
SUB = 3
OUTPUT = 4
LEFT = 5
RIGHT = 6
OPEN = 7
CLOSE = 8
CLEAR = 9
ADDLEFT = 10
ADDRIGHT = 11
NOP = None

# the trivial map from brainfuck to awib IR
bf_to_ir = {'+': (ADD, 1),
            '-': (SUB, 1),
            '<': (LEFT, 1),
            '>': (RIGHT, 1),
            '[': (OPEN, 0),
            ']': (CLOSE, 0),
            ',': (INPUT, 0),
            '.': (OUTPUT, 0)}

ir_to_str = {ADD:'ADD', SUB:'SUB', LEFT:'LEFT', RIGHT:'RIGHT',
             OPEN:'OPEN', CLOSE:'CLOSE', INPUT:'INPUT', OUTPUT:'OUTPUT',
             CLEAR:'CLEAR', ADDLEFT: 'ADDLEFT', ADDRIGHT: 'ADDRIGHT'}


class AWIPError(Exception):
    """Base class for AWIP errors."""

class AWIPCompileError(AWIPError):
    pass

class AWIPRuntimeError(AWIPError):
    pass

class AWIPStepError(AWIPRuntimeError):
    """Raised if program exceeds a specified step limit."""

class AWIP:

    EOF_NO_CHANGE = 1
    EOF_WRITE_ZERO = 2
    EOF_WRITE_MINUS_ONE = 3

    _DEFAULT_MEMORY_SIZE = 0xffff

    def __init__(self, code):
        self.code = code
        self._compile()
        self._dead_code()
        self._reduce()
        self._clear_loops()
        self._copy_loops()
        self._remove_nops()
        self._jmp_offsets()

    def _compile(self):
        """Compiles bf to IR and sanity checks."""

        ir = []
        line, col = 1, 0
        depth = 0

        for c in self.code:
            if c == '\n':
                line += 1
                col = 0
            else:
                col += 1

            oparg = bf_to_ir.get(c)
            if oparg is None:
                continue
            if oparg[0] == OPEN:
                depth += 1
            elif oparg[0] == CLOSE:
                depth -= 1
                if depth < 0:
                    raise AWIPError("mismatched loop close at line %d col %d" %
                                    (line, col))
            ir.append(oparg)
        if depth > 0:
            raise AWIPError("%d loop openers without closers" % depth)
        self.code = ir

    def _dead_code(self):
        """Removes blocks of obviously dead code."""

        code, i = self.code, 0
        while i < len(code):
            if code[i][0] == OPEN and i > 0 and code[i-1][0] == CLOSE:
                code[i], depth, i = (NOP, 0), 1, i+1
                while depth:
                    if code[i][0] == OPEN:
                        depth += 1
                    elif code[i][0] == CLOSE:
                        depth -= 1
                    code[i] = (NOP, 0)
                    i += 1
            else:
                i += 1

    def _reduce(self):
        """Reduces sequences of '<', '>', '-' and '+' into LEFT, RIGHT..."""

        reduction = [(NOP, 0)]
        opposite = {LEFT: RIGHT, RIGHT: LEFT, SUB: ADD, ADD: SUB}

        for oparg in self.code:
            if oparg[0] not in opposite or reduction[-1][0] not in opposite:
                reduction.append(oparg)
                continue

            (op, arg), (pop, parg) = oparg, reduction[-1]
            if op == pop:
                reduction[-1] = (pop, parg + arg)
            elif op == opposite[op]:
                diff = parg - arg
                if diff < 0:
                    reduction[-1] = (op, -diff)
                elif diff > 0:
                    reduction[-1] = (pop, diff)
                else:
                    reduction.pop(-1)
            else:
                reduction.append(oparg)
        reduction.pop(0)
        self.code = reduction

    def _clear_loops(self):
        """Reduces clear loops ('[-]' and '[+]') into CLEAR."""

        code = self.code
        for i in range(2, len(code)):
            if (code[i][0] == CLOSE and code[i-2][0] == OPEN and
                code[i-1][1] == 1 and code[i-1][0] in (SUB, ADD)):
                code[i-2] = code[i-1] = (NOP, 0)
                code[i] = (CLEAR, 0)

    def _copy_loops(self):
        """Reduces copy loops (e.g. '[->+>+<<]') into ADDLEFT/ADDRIGHT."""

    def _remove_nops(self):
        """Removes nops."""

        nonops = []
        for oparg in self.code:
            if oparg[0] != NOP:
                nonops.append(oparg)
        self.code = nonops

    def _jmp_offsets(self):
        """Calculates and stores jmp offsets for OPEN and CLOSE."""

        code, jmps, i = self.code, [], 0
        while i < len(code):
            if code[i][0] == OPEN:
                jmps.append(i)
            elif code[i][0] == CLOSE:
                assert len(jmps)
                opener = jmps.pop()
                code[opener] = (OPEN, i)
                code[i] = (CLOSE, opener)
            i += 1

    def dump(self):
        return ["%s(%d)" % (ir_to_str[op], arg) for op,arg in self.code]

    def run(self, cell_size=8, eof_behaviour=EOF_NO_CHANGE, steps=None,
            memory_limit=None, memory="", pointer=0,
            input='', input_file=None, output_file=None):
        """Runs code.

        @type cell_size: int
        @param cell_size: bits per cell
        @type eof_behaviour: int
        @param eof_behaviour: what to do if code requests input after EOF
        @type steps: int
        @param steps: run code for at most steps IR operations
        @type memory_limit: int
        @param memory_limit: restricts memory area to memory_limit cells
        @type memory: iterable
        @param memory: data to initalize memory area with instead of zeroes
        @type pointer: int
        @param pointer: initial pointer position
        @type input: str
        @param input: block of data to feed as input
        @type input_file: file-like object
        @param input_file: source of input in addition to static input
        @type output_file: file-like objet
        @param output_file: sink for output in addition to return value
        @rtype: (str, [int])
        @return: tuple with program output and memory
        """

        mem = list(memory) + [0]*(self._DEFAULT_MEMORY_SIZE - len(memory))
        mod = 2**cell_size
        code, codelen = self.code, len(self.code)
        input = list(input)
        output = []
        ip, p = 0, pointer
        opcount = 0

        while ip < codelen:
            op, arg = code[ip]

            if steps is not None and opcount >= steps:
                raise AWIPStepError()

            if op == ADD:
                mem[p] = (mem[p] + arg) % mod

            elif op == SUB:
                mem[p] = (mem[p] - arg) % mod

            elif op == LEFT:
                p -= arg
                if p < 0:
                    raise AWIPRuntimeError("pointer moved below memory area")

            elif op == RIGHT:
                p += arg
                if memory_limit is not None and p > memory_limit:
                    raise AWIPRuntimeError("pointer moved beyond memory area")
                if p >= len(mem):
                    mem.extend([0]*(1+len(mem)/2))

            elif op == INPUT:
                eof = True
                if input:
                    mem[p] = input.pop(0)
                    if isinstance(mem[p], str):
                        mem[p] = ord(mem[p])
                    mem[p] %= mod
                    eof = False
                elif input_file:
                    c = input_file.read(1)
                    if c:
                        mem[p] = ord(c) % mod
                        eof = False
                if eof:
                    if eof_behaviour == self.EOF_WRITE_ZERO:
                        mem[p] = 0
                    elif eof_behaviour == self.EOF_WRITE_MINUS_ONE:
                        mem[p] = (-1) % mod

            elif op == OUTPUT:
                output.append(mem[p])
                if output_file:
                    output_file.write(chr(mem[p]))

            elif op == OPEN:
                if mem[p] == 0:
                    ip = arg

            elif op == CLOSE:
                if mem[p] != 0:
                    ip = arg

            elif op == CLEAR:
                mem[p] = 0

            elif op == ADDLEFT:
                mem[p-arg] += mem[p]

            elif op == ADDRIGHT:
                mem[p+arg] += mem[p]

            ip += 1
            opcount += 1

        return (output, mem)


def _main():
    # options
    parser = optparse.OptionParser(usage='%prog [options] FILE')
    parser.add_option('-c', '--cell-size',
                      metavar='B', default=8, type='int',
                      help='run in environment with B bit cells (default: 8)')
    parser.add_option('', '--eof-no-change',
                      action='store_true', default=False,
                      help='do nothing when reading input after EOF (default)')
    parser.add_option('', '--eof-write-zero',
                      action='store_true', default=False,
                      help='write zero (0) when reading input after EOF')
    parser.add_option('', '--eof-write-minus-one',
                      action='store_true', default=False,
                      help='write minus one (-1) when reading input after EOF')
    parser.add_option('-s', '--steps',
                      metavar='S', type='int',
                      help='terminate execution after S awib IR operations')
    parser.add_option('-d', '--dump',
                      action='store_true', default=False,
                      help='output compiled IR, do not run code')
    (options, args) = parser.parse_args()

    # sanity
    if options.cell_size < 1:
        sys.stderr.write("Error: cell size %d < 1\n" % options.cell_size)
        sys.exit(1)
    if (options.eof_no_change +
        options.eof_write_zero +
        options.eof_write_minus_one) > 1:
        sys.stderr.write("Error: multiple eof behaviours specified\n")
        sys.exit(1)
    if options.steps is not None and options.steps < 0:
        sys.stderr.write("Error: negative number (%d) of steps requested\n" %
                        options.steps)
        return 1
    if len(args) != 1:
        sys.stderr.write("Error: please specify a program to run\n")
        return 1

    # eof behaviour
    if options.eof_write_zero:
        eof_behaviour = AWIP.EOF_WRITE_ZERO
    elif options.eof_write_minus_one:
        eof_behaviour = AWIP.EOF_WRITE_MINUS_ONE
    else:
        eof_behaviour = AWIP.EOF_NO_CHANGE

    # fetch brainfuck source
    try:
        code = open(args[0]).read()
    except IOError as ie:
        sys.stderr.write("Error: could not open '%s' for reading: %s\n" %
                         (args[0], ie))
        return 1

    # compile
    try:
        int = AWIP(code)
    except AWIPError as bfe:
        sys.stderr.write("Error: failed to compile code: %s\n" % bfe)
        return 1

    if options.dump:
        sys.stdout.write('\n'.join(int.dump())+'\n')
        return 0

    # run
    try:
        int.run(steps=options.steps, eof_behaviour=eof_behaviour,
                cell_size=options.cell_size,
                input_file=sys.stdin, output_file=sys.stdout)
    except AWIPStepError:
        sys.stderr.write("Error: program terminated after exceeding step "
                         "limit %d\n" % options.steps)
        return 1
    except AWIPRuntimeError as bfe:
        sys.stderr.write("Error: %s\n" % bfe)
        return 1
    return 0

if __name__ == '__main__':
    import optparse
    sys.exit(_main())
