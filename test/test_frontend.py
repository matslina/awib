#!/usr/bin/python
# -*- coding: utf-8 -*-

import ir
import common
import awip

frontend_path = "/home/ml/src/awib/trunk/frontend/frontend.b"

_LANG_C = 1
_386_LINUX = 2


class FrontendTest(common.BFTestCase):

    def setUp(self):
        self.code = open(frontend_path).read()

    def _check_post_condition(self, mem, code):
        """Checks frontend post execution memory against expected ir code."""

        # sanity
        self.assert_(len(mem) >= 6, "post exec memory must span at least 6 "
                     "cells, only got %d" % len(mem))
        self.assert_(mem[0] in (_LANG_C, _386_LINUX),
                     "frontend chose bad target platform T (= %d)" % mem[0])
        self.assertEquals(mem[1], 0, "frontend should leave cell 1 blank")
        self.assert_(mem[2], "frontend marked bytecode as not OK")

        # find end of compiled code block
        i = 3
        while i < len(mem) and mem[i] != 0:
            i += 2

        # more sanity
        self.assert_( not (len(mem) < i+3), "maximum loop depth is missing")
        self.assert_( not (len(mem) > i+3), "junk data beyond max loop depth")
        self.assertEquals((i-3)/2, len(code), "expected %d ops, got %d" %
                          (len(code), (i-3)/2))

        compile = mem[3:i]

        # compare frontend output with expected byte code
        for i, expected in enumerate(code):

            op_code = compile[2*i]
            op_arg = compile[2*i + 1]

            if op_code not in ir.code_to_op:
                self.fail("invalid code at pos %d: %d" % (i, op_code))

            try:
                op = ir.code_to_op[op_code](op_arg)
            except ValueError, ve:
                self.fail("invalid op at pos %d: %s" % (i, ve))

            if expected.__class__ != op.__class__ or expected.arg != op.arg:
                self.fail("expected %r but got %r at op %d" %
                          (expected, op, i))

    def _run_and_check(self, program, ir):
        out, mem = self.run_bf(self.code, program,
                               precondition=[1], steps=5000000)
        self.assertEquals(out, [], "frontend should not produce output")
        self._check_post_condition(mem, ir)

    def test_empty_input(self):
        self._run_and_check("", [])

    def test_basic_operations(self):
        self._run_and_check(">+.<-[,]",
                             [ir.RIGHT(1),
                              ir.ADD(1),
                              ir.OUTPUT(),
                              ir.LEFT(1),
                              ir.SUB(1),
                              ir.OPEN(),
                              ir.INPUT(),
                              ir.CLOSE()])

    def test_nested_loops(self):
        self._run_and_check("+[-[+<].]>[[[]+]+]+[+]",
                             [ir.ADD(1),
                              ir.OPEN(),
                                ir.SUB(1),
                                ir.OPEN(),
                                  ir.ADD(1),
                                  ir.LEFT(1),
                                ir.CLOSE(),
                                ir.OUTPUT(),
                              ir.CLOSE(),
                              ir.RIGHT(1),
                              ir.OPEN(),
                                ir.OPEN(),
                                  ir.OPEN(),
                                  ir.CLOSE(),
                                  ir.ADD(1),
                                ir.CLOSE(),
                                ir.ADD(1),
                              ir.CLOSE(),
                              ir.ADD(1),
                              ir.OPEN(),
                                ir.ADD(1),
                              ir.CLOSE()])

    def test_clear_loops(self):
        self._run_and_check("+[-]+[+]",
                             [ir.ADD(1),
                              ir.CLEAR(),
                              ir.ADD(1),
                              ir.OPEN(),
                                ir.ADD(1),
                              ir.CLOSE()])

    def test_loop_elimination(self):
        self._run_and_check("[+++]+[][+++].[-][+++]",
                             [ir.ADD(1),
                              ir.OPEN(),
                              ir.CLOSE(),
                              ir.OUTPUT(),
                              ir.CLEAR()])
        self._run_and_check("[-][+++]", [])

    def test_cancellation(self):
        self._run_and_check("+++-->><-+<-,  <>-++-+-<><>.",
                             [ir.INPUT(), ir.OUTPUT()])
        self._run_and_check("-+<>+-><", [])
        self._run_and_check(".<<<<>>>>++++----.",
                             [ir.OUTPUT(), ir.OUTPUT()])

    def test_contraction(self):
        self._run_and_check("+++", [ir.ADD(3)])
        self._run_and_check(['+']*255, [ir.ADD(255)])
        self._run_and_check(['+']*256, [])
        self._run_and_check("---", [ir.SUB(3)])
        self._run_and_check(['-']*255, [ir.SUB(255)])
        self._run_and_check(['-']*256, [])
        self._run_and_check("<<<", [ir.LEFT(3)])
        self._run_and_check(['<']*128, [ir.LEFT(127), ir.LEFT(1)])
        self._run_and_check(">>>", [ir.RIGHT(3)])
        self._run_and_check(['>']*128, [ir.RIGHT(127), ir.RIGHT(1)])

    def test_contraction_and_cancellation(self):
        self._run_and_check("++++--", [ir.ADD(2)])
        self._run_and_check("--++++", [ir.ADD(2)])
        self._run_and_check("++----", [ir.SUB(2)])
        self._run_and_check("----++", [ir.SUB(2)])
        self._run_and_check(">>>><<", [ir.RIGHT(2)])
        self._run_and_check("<<>>>>", [ir.RIGHT(2)])
        self._run_and_check(">><<<<", [ir.LEFT(2)])
        self._run_and_check("<<<<>>", [ir.LEFT(2)])

        self._run_and_check(['>']*130 + ['<', '<'],
                             [ir.RIGHT(127),
                              ir.RIGHT(1)])
        self._run_and_check(['>']*130 + ['<', '<', '<'],
                             [ir.RIGHT(127)])
        self._run_and_check(['>']*130 + ['<', '<', '<', '<'],
                             [ir.RIGHT(126)])

        self._run_and_check(['<']*130 + ['>', '>'],
                             [ir.LEFT(127),
                              ir.LEFT(1)])
        self._run_and_check(['<']*130 + ['>', '>', '>'],
                             [ir.LEFT(127)])
        self._run_and_check(['<']*130 + ['>', '>', '>', '>'],
                             [ir.LEFT(126)])

    def test_target_selection(self):
        pass

    def test_unbalanced_loop(self):
        pass

    def test_maximum_loop_depth(self):
        pass

if __name__ == "__main__":
    import unittest
    unittest.main()
