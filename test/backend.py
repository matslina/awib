#!/usr/bin/python
# -*- coding: utf-8 -*-

import shutil
import os
import shutil
import tempfile
import re

import ir
import common
import awip


class BackendTestCase(common.BFTestCase):
    """Collection of tests for backends.

    Inheriting test cases need only set BACKEND_PATH and implement
    run_program().

    BACKEND_PATH is path to backend source code, relative the awib root.
    run_program() runs what the backend outputs.
    """

    BACKEND_PATH = NotImplementedError()
    BACKEND_INDEX = NotImplementedError()
    MAX_NESTED_LOOPS = 300

    def __init__(self, *args, **kwargs):
        common.BFTestCase.__init__(self, *args, **kwargs)
        self.code = open(os.path.join(os.path.dirname(__file__),
                                      '..', self.BACKEND_PATH)).read()

    def run_program(self, path, input):
        """Runs a program built with this backend,

        @param path: path of program output by this backend
        @type input: str
        @param input: data to feed the program
        @rtype: str
        @return output data
        """

        raise NotImplementedError()

    def run_ir(self, code, input, expected_output, steps=5000000):
        """Compiles and runs code with this backend.

        @param code: bytecode to compile
        @param input: data to feed the compiled program when run
        @param expected_output: expected output
        """

        # calculate max loop depth
        max_depth, depth = 1, 1
        for op in code:
            if op.__class__ == ir.OPEN:
                depth += 1
            elif op.__class__ == ir.CLOSE:
                depth -= 1
            max_depth = max(depth, max_depth)

        # set up the precondition and execute the backend
        precond = [0] * 23
        precond.append(self.BACKEND_INDEX)
        precond.extend(ord(c) for c in (''.join(str(op) for op in code)))
        precond.extend([0, max_depth/256, max_depth%256])
        out, _ = self.run_bf(self.code, [], precondition=precond,
                             pointer=23, steps=steps)

        # write backend output to disk
        tmpd = tempfile.mkdtemp("awib_%s" % self.__class__.__name__.lower())
        prog_path = os.path.join(tmpd, 'prog')
        prog = open(prog_path, "w")
        prog.write(''.join(chr(i) for i in out))
        prog.close()

        # run backend output
        try:
            prog_out = self.run_program(prog_path, bytes(input))
        finally:
            shutil.rmtree(tmpd)

        # compare output
        for i, (o, e) in enumerate(zip(prog_out, expected_output)):
            self.assertEquals(o, e, "outputs differ at position %d: "
                              "expected %d, got %d" % (i, e, o))
        self.assertEquals(len(prog_out), len(expected_output))

    def test_empty_program(self):
        self.run_ir([],[],[])

    def test_basic_operations(self):
        # ,[->>++++++++<<]>>.[-].[-]+
        self.run_ir([ir.INPUT(),
                     ir.OPEN(),
                       ir.SUB(1), ir.RIGHT(2), ir.ADD(8), ir.LEFT(2),
                     ir.CLOSE(),
                     ir.RIGHT(2), ir.OUTPUT(), ir.SET(0), ir.OUTPUT()],
                    [8],
                    [64, 0])

    def test_nested_loops(self):
        # ++[->++[->++[->++[->++[->++<]<]<]<]<]>>>>>.[-].
        self.run_ir([ir.ADD(2),
                     ir.OPEN(), ir.SUB(1), ir.RIGHT(1), ir.ADD(2),
                       ir.OPEN(), ir.SUB(1), ir.RIGHT(1), ir.ADD(2),
                         ir.OPEN(), ir.SUB(1), ir.RIGHT(1), ir.ADD(2),
                           ir.OPEN(), ir.SUB(1), ir.RIGHT(1), ir.ADD(2),
                             ir.OPEN(), ir.SUB(1), ir.RIGHT(1), ir.ADD(2),
                             ir.LEFT(1), ir.CLOSE(),
                           ir.LEFT(1), ir.CLOSE(),
                         ir.LEFT(1), ir.CLOSE(),
                       ir.LEFT(1), ir.CLOSE(),
                     ir.LEFT(1), ir.CLOSE(),
                     ir.RIGHT(5), ir.OUTPUT(), ir.SET(0), ir.OUTPUT()],
                    [], [64, 0])

        # ++>+[[[[->]<]>]<].<.
        self.run_ir([ir.ADD(2), ir.RIGHT(1), ir.ADD(1),
                     ir.OPEN(),
                       ir.OPEN(),
                         ir.OPEN(),
                           ir.OPEN(),
                             ir.SUB(1), ir.RIGHT(1),
                           ir.CLOSE(),
                           ir.LEFT(1),
                         ir.CLOSE(),
                         ir.RIGHT(1),
                       ir.CLOSE(),
                       ir.LEFT(1),
                     ir.CLOSE(),
                     ir.OUTPUT(), ir.LEFT(1), ir.OUTPUT()],
                    [], [0, 2])

    def test_eof_behaviour(self):
        # do no-change on EOF
        # ++++++++++,.
        self.run_ir([ir.ADD(10), ir.INPUT(), ir.OUTPUT()],
                    [], [10])

    def test_cells_wrap(self):
        # .-.++.+{254}.+.-.
        self.run_ir([ir.OUTPUT(),
                     ir.SUB(1), ir.OUTPUT(),
                     ir.ADD(2), ir.OUTPUT(),
                     ir.ADD(254), ir.OUTPUT(),
                     ir.ADD(1), ir.OUTPUT(),
                     ir.SUB(1), ir.OUTPUT()],
                    [], [0, 255, 1, 255, 0, 255])

    def test_deep_nested_loops(self):
        # +[{many}-(>+.<]){many}
        self.run_ir([ir.ADD(1)] +
                    ([ir.OPEN()] * self.MAX_NESTED_LOOPS) +
                    [ir.SUB(1)] +
                    ([ir.RIGHT(1), ir.ADD(1), ir.OUTPUT(),
                      ir.LEFT(1), ir.CLOSE()] * self.MAX_NESTED_LOOPS),
                    [], [i % 256 for i in range(1, self.MAX_NESTED_LOOPS + 1)],
                    steps=50000000)

    def test_set(self):
        self.run_ir([ir.SET(0), ir.OUTPUT()], [], [0])
        self.run_ir([ir.SET(1), ir.OUTPUT()], [], [1])
        self.run_ir([ir.SET(2), ir.OUTPUT()], [], [2])
        self.run_ir([ir.SET(255), ir.OUTPUT()], [], [255])

        self.run_ir([ir.ADD(12), ir.SET(0), ir.OUTPUT()], [], [0])
        self.run_ir([ir.ADD(12), ir.SET(1), ir.OUTPUT()], [], [1])
        self.run_ir([ir.ADD(12), ir.SET(2), ir.OUTPUT()], [], [2])
        self.run_ir([ir.ADD(12), ir.SET(255), ir.OUTPUT()], [], [255])

    def test_mul(self):
        self.run_ir([ir.ADD(4), ir.RMUL(2, 4), ir.RIGHT(2), ir.OUTPUT()],
                    [], [16])
        self.run_ir([ir.ADD(4), ir.RIGHT(2), ir.ADD(7), ir.LMUL(2, 254),
                     ir.LEFT(2), ir.OUTPUT()],
                    [], [246])

        self.run_ir([ir.RIGHT(127), ir.SUB(2), ir.LMUL(127, 1),
                     ir.LEFT(127), ir.OUTPUT()],
                     [], [254])
        self.run_ir([ir.RIGHT(127), ir.SUB(2), ir.LMUL(127, 12),
                     ir.LEFT(127), ir.OUTPUT()],
                    [], [232])
        self.run_ir([ir.RIGHT(127), ir.SUB(2), ir.LMUL(127, 255),
                     ir.LEFT(127), ir.OUTPUT()],
                    [], [2])

        self.run_ir([ir.SET(3), ir.RMUL(127, 1), ir.RIGHT(127), ir.OUTPUT()],
                    [], [3])
        self.run_ir([ir.SET(3), ir.RMUL(127, 12), ir.RIGHT(127), ir.OUTPUT()],
                    [], [36])
        self.run_ir([ir.SET(3), ir.RMUL(127, 255),
                     ir.RIGHT(127), ir.OUTPUT()],
                    [], [253])

        self.run_ir([ir.ADD(12), ir.RMUL(1, 12), ir.RIGHT(1), ir.OUTPUT()],
                    [], [144])
        self.run_ir([ir.RIGHT(1), ir.ADD(12), ir.LMUL(1, 12), ir.LEFT(1),
                     ir.OUTPUT()],
                    [], [144])

    def test_mul_overreaching(self):
        """Backend should handle MUL writing up to 127 cells outside of tape.

        There are perfectly valid programs for which the frontend will
        output multiplication operations that write to a position
        outside of the tape. One example would be '.[-<+>]' for which
        an OUTPUT() followed by LMUL(1,1) will be produced. There are
        other less obvious cases that the frontend cannot catch (and
        my gut says catching them all it's equivalent to the halting
        problem).

        One option is for the backends to always check that the
        current cell is non-zero before writing the product of a
        multiplication operation. Another option is to simply pad the
        tape with 127 cells on each end and to initialize the pointer
        at position 127 instead of 0 (and 127 is magic because it's
        the max offset the frontend emits for the multipication
        operations).
        """

        # offsets on the left
        self.run_ir([ir.LMUL(1, 1), ir.OUTPUT()], [], [0])
        self.run_ir([ir.LMUL(2, 1), ir.OUTPUT()], [], [0])
        self.run_ir([ir.LMUL(3, 1), ir.OUTPUT()], [], [0])
        self.run_ir([ir.LMUL(126, 1), ir.OUTPUT()], [], [0])
        self.run_ir([ir.LMUL(127, 1), ir.OUTPUT()], [], [0])

        # offsets on the right
        movetolastcell = [ir.RIGHT(127) for _ in range(516)] + [ir.RIGHT(2)]
        self.run_ir(movetolastcell + [ir.RMUL(1, 1), ir.OUTPUT()], [], [0],
                    steps=10000000)
        self.run_ir(movetolastcell + [ir.RMUL(2, 1), ir.OUTPUT()], [], [0],
                    steps=10000000)
        self.run_ir(movetolastcell + [ir.RMUL(3, 1), ir.OUTPUT()], [], [0],
                    steps=10000000)
        self.run_ir(movetolastcell + [ir.RMUL(126, 1), ir.OUTPUT()], [], [0],
                    steps=10000000)
        self.run_ir(movetolastcell + [ir.RMUL(127, 1), ir.OUTPUT()], [], [0],
                    steps=10000000)


class LangGenericTestCase(BackendTestCase):
    BACKEND_PATH = "lang_generic/backend.b"
    BACKEND_INDEX = NotImplementedError()

    include_re = re.compile(r'#include\((.*)\)')

    def __init__(self, *args, **kwargs):
        BackendTestCase.__init__(self, *args, **kwargs)

        dir = os.path.join(os.path.dirname(__file__), '..',
                           os.path.dirname(self.BACKEND_PATH))

        code = []
        for line in self.code.split('\n'):
            m = self.include_re.match(line)
            if m:
                line = open(os.path.join(dir, m.group(1))).read()
            code.append(line)

        self.code = ''.join(code)


if __name__ == "__main__":
    import unittest
    unittest.main()
