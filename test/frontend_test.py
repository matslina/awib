#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import ir
import common
import awip

frontend_path = "frontend/frontend.b"

_386_LINUX = 1
_LANG_C = 2


class FrontendTest(common.BFTestCase):

    code = open(os.path.join(os.path.dirname(__file__),
                             '..', frontend_path)).read()

    def _check_post_condition(self, mem, code, target=None, maxdepth=None):
        """Checks frontend post execution memory against expected ir code."""

        # sanity
        self.assert_(len(mem) >= 6, "post exec memory must span at least 6 "
                     "cells, only got %d" % len(mem))
        if target is not None:
            self.assertEqual(mem[0], target,
                              "bad target platform (%d!=%d)" % (mem[0],target))
        else:
            self.assert_(mem[0] in (_LANG_C, _386_LINUX),
                         "frontend chose bad target platform T (=%d)" % mem[0])
        self.assertEqual(mem[1], 0, "frontend should leave cell 1 blank")
        self.assert_(mem[2], "frontend marked bytecode as not OK")

        # find end of compiled code block
        i = 3
        while i < len(mem) and mem[i] != 0:
            i += 2

        # more sanity
        self.assert_( not (len(mem) < i+3), "maximum loop depth is missing")
        self.assert_( not (len(mem) > i+3), "junk data beyond max loop depth")
        if maxdepth is not None:
            Mm = mem[i+1]*0xff + mem[i+2]
            self.assertEqual(Mm, maxdepth, "wrong max depth, got %d not %d" %
                              (Mm, maxdepth))


        compile = mem[3:i]

        # compare frontend output with expected byte code
        try:
            compile = ir.parse_codes(mem[3:i])
        except ValueError as ve:
            self.fail("broken bytecode: %s" % ve)
        for i, (op, expected) in enumerate(zip(compile, code)):
            if op != expected:
                self.fail("expected %r but got %r at pos %d" %
                          (expected, op, i))
        if len(compile) != len(code):
            self.fail("expected %d ops but got %d; all %d matched though" %
                      (len(code), len(compile), min(len(code), len(compile))))

    ##
    ## Byte code compilation
    ##

    def _run_and_check_ir(self, program, ir, maxdepth=1):
        out, mem = self.run_bf(self.code, program,
                               precondition=[1], steps=10000000)
        self.assertEqual(out, [], "frontend should not produce output")
        self._check_post_condition(mem, ir, maxdepth=maxdepth)

    def test_empty_input(self):
        # The trivial program compiles to nothing
        self._run_and_check_ir("", [])

    def test_single_instruction(self):
        # Single brainfuck instructions can be valid programs
        self._run_and_check_ir(">", [ir.RIGHT(1)])
        self._run_and_check_ir("<", [ir.LEFT(1)])
        self._run_and_check_ir(",", [ir.INPUT()])
        self._run_and_check_ir(".", [ir.OUTPUT()])
        self._run_and_check_ir("+", [ir.ADD(1)])
        self._run_and_check_ir("-", [ir.SUB(1)])

    def test_single_instruction_with_comment(self):
        # Single instructions with comments can be valid programs
        self._run_and_check_ir("a>", [ir.RIGHT(1)])
        self._run_and_check_ir("<a", [ir.LEFT(1)])
        self._run_and_check_ir("a.a", [ir.OUTPUT()])
        self._run_and_check_ir("aa,", [ir.INPUT()])
        self._run_and_check_ir("+aa", [ir.ADD(1)])
        self._run_and_check_ir("aa-aa", [ir.SUB(1)])

    def test_all_instructions(self):
        # All instructions can live in the same program
        self._run_and_check_ir(">+.<-[,]",
                               [ir.RIGHT(1),
                                ir.ADD(1),
                                ir.OUTPUT(),
                                ir.LEFT(1),
                                ir.SUB(1),
                                ir.OPEN(),
                                ir.INPUT(),
                                ir.CLOSE()], maxdepth=2)
        self._run_and_check_ir("+,[->.]<",
                               [ir.ADD(1),
                                ir.INPUT(),
                                ir.OPEN(),
                                ir.SUB(1),
                                ir.RIGHT(1),
                                ir.OUTPUT(),
                                ir.CLOSE(),
                                ir.LEFT(1)], maxdepth=2)

    def test_nested_loops(self):
        # Loops can be nested
        # Loop depth is calculated
        self._run_and_check_ir("+[-[+<].]>[[[]+]+]+",
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
                                ir.ADD(1)], maxdepth=4)
        self._run_and_check_ir("+[[[[[[[[.]]]]],[[[]]]]]]",
                               [ir.ADD(1)] +
                               [ir.OPEN()] * 8 +
                               [ir.OUTPUT()] +
                               [ir.CLOSE()] * 5 +
                               [ir.INPUT()] +
                               [ir.OPEN()] * 3 +
                               [ir.CLOSE()] * 6,
                               maxdepth=9)

    def test_clear_loops(self):
        # The [-] and [+] constructs become SET(0)
        # These are not included when calculating loop depth
        self._run_and_check_ir(",[-].[+]",
                               [ir.INPUT(),
                                ir.SET(0),
                                ir.OUTPUT(),
                                ir.SET(0)], maxdepth=1)

    def test_loop_elimination(self):
        # Obviously dead loops are skipped entirely

        # Loop open as first op => dead
        self._run_and_check_ir("[+,-.]", [])
        self._run_and_check_ir("[+[[[,]-]-]-.]", [])
        self._run_and_check_ir("[+[[[,]-]-]-.][-]", [])
        self._run_and_check_ir("[+[[[,]-]-]-.][+]", [])
        self._run_and_check_ir("[+[[[,]-]-]-.][>>>]", [])
        self._run_and_check_ir("[+[[[,]-]-]-.][>>>][.]", [])

        # Loop open after loop close => dead
        self._run_and_check_ir("+[>][.]",
                               [ir.ADD(1),
                                ir.OPEN(),
                                  ir.RIGHT(1),
                                ir.CLOSE()],
                               maxdepth=2)

        # Loop open after SET(0) => dead
        self._run_and_check_ir(",[-][>>]",
                               [ir.INPUT(), ir.SET(0)])
        self._run_and_check_ir(",[-][>>][..]",
                               [ir.INPUT(), ir.SET(0)])
        self._run_and_check_ir(",[-][>>].",
                               [ir.INPUT(), ir.SET(0), ir.OUTPUT()])

        # But open after SET(x) where x > 0 => alive
        self._run_and_check_ir(",[-]+[>>]",
                               [ir.INPUT(), ir.SET(1),
                                ir.OPEN(), ir.RIGHT(2), ir.CLOSE()],
                               maxdepth=2)

    ##
    ## Cancellation
    ##

    def test_cancellation_of_basic_instructions(self):
        # Two pairs of the basic brainfuck instructions are mutually
        # cancelling

        # Pairs of cancelling instructions are reduced
        self._run_and_check_ir("+-", [])
        self._run_and_check_ir("+-", [])
        self._run_and_check_ir("><", [])
        self._run_and_check_ir("<>", [])

        # Longer sequences of cancelling instructions are reduced
        self._run_and_check_ir("-+<>+-><", [])
        self._run_and_check_ir(".<<<<>>>>++++----.",
                               [ir.OUTPUT(), ir.OUTPUT()])

        # The cancelling instructions do not have to be immediately adjacent
        self._run_and_check_ir("+++-->><-+<-,  <>-++-+-<><>.",
                               [ir.INPUT(), ir.OUTPUT()])
        self._run_and_check_ir(",>>+++>+--+<----+<<++>><<--",
                               [ir.INPUT()])

    def test_cancellation_partial(self):
        # Cancellation can be partial, leaving part of the cancelling
        # instructions behind.

        # The basic brainfuck instructions
        self._run_and_check_ir("++++--", [ir.ADD(2)])
        self._run_and_check_ir("--++++", [ir.ADD(2)])
        self._run_and_check_ir("++----", [ir.SUB(2)])
        self._run_and_check_ir("----++", [ir.SUB(2)])
        self._run_and_check_ir(">>>><<", [ir.RIGHT(2)])
        self._run_and_check_ir("<<>>>>", [ir.RIGHT(2)])
        self._run_and_check_ir(">><<<<", [ir.LEFT(2)])
        self._run_and_check_ir("<<<<>>", [ir.LEFT(2)])

        # Cases with argument overflow, i.e. >255 of the same
        # instructions in a row, are also cancelled correctly.
        self._run_and_check_ir(['>']*258 + ['<', '<'],
                               [ir.RIGHT(255),
                                ir.RIGHT(1)])
        self._run_and_check_ir(['>']*258 + ['<', '<', '<'],
                               [ir.RIGHT(255)])
        self._run_and_check_ir(['>']*258 + ['<', '<', '<', '<'],
                               [ir.RIGHT(254)])

        self._run_and_check_ir(['<']*258 + ['>', '>'],
                               [ir.LEFT(255),
                                ir.LEFT(1)])
        self._run_and_check_ir(['<']*258 + ['>', '>', '>'],
                               [ir.LEFT(255)])
        self._run_and_check_ir(['<']*258 + ['>', '>', '>', '>'],
                               [ir.LEFT(254)])

    def test_cancellation_arithmetic_set(self):
        # SET() invalidates all immediately preceding arithmetic
        # operations.
        self._run_and_check_ir('+[-]', [ir.SET(0)])
        self._run_and_check_ir('+[+]', [ir.SET(0)])
        self._run_and_check_ir('++++++++++[-]', [ir.SET(0)])
        self._run_and_check_ir('++++++++++[+]', [ir.SET(0)])
        self._run_and_check_ir('----------[-]++', [ir.SET(2)])
        self._run_and_check_ir('++++++++++[+]++', [ir.SET(2)])

    ##
    ## Contraction
    ##

    def test_contraction_simple_cases(self):
        # Sequences of multiple brainfuck instructions can be
        # contracted into single bytecode operations
        self._run_and_check_ir("++", [ir.ADD(2)])
        self._run_and_check_ir("+++", [ir.ADD(3)])
        self._run_and_check_ir("+" * 128, [ir.ADD(128)])
        self._run_and_check_ir("--", [ir.SUB(2)])
        self._run_and_check_ir("---", [ir.SUB(3)])
        self._run_and_check_ir("-" * 128, [ir.SUB(128)])
        self._run_and_check_ir("<<", [ir.LEFT(2)])
        self._run_and_check_ir("<<<", [ir.LEFT(3)])
        self._run_and_check_ir("<" * 128, [ir.LEFT(128)])
        self._run_and_check_ir(">>", [ir.RIGHT(2)])
        self._run_and_check_ir(">>>", [ir.RIGHT(3)])
        self._run_and_check_ir(">" * 128, [ir.RIGHT(128)])

    def test_contraction_overflow_arithmetic(self):
        # Arithmetic operations are removed on argument overflow
        self._run_and_check_ir(['+']*255, [ir.ADD(255)])
        self._run_and_check_ir(['+']*256, [])
        self._run_and_check_ir(['+']*257, [ir.ADD(1)])
        self._run_and_check_ir(['-']*255, [ir.SUB(255)])
        self._run_and_check_ir(['-']*256, [])
        self._run_and_check_ir(['-']*257, [ir.SUB(1)])

    def test_contraction_overflow_movement(self):
        # Argument overflow on movement operations only add more
        # operations
        self._run_and_check_ir(['>']*255, [ir.RIGHT(255)])
        self._run_and_check_ir(['>']*256, [ir.RIGHT(255), ir.RIGHT(1)])
        self._run_and_check_ir(['>']*257, [ir.RIGHT(255), ir.RIGHT(2)])
        self._run_and_check_ir(['<']*255, [ir.LEFT(255)])
        self._run_and_check_ir(['<']*256, [ir.LEFT(255), ir.LEFT(1)])
        self._run_and_check_ir(['<']*257, [ir.LEFT(255), ir.LEFT(2)])

    def test_contraction_set_arithmetic(self):
        # Arithmetic ops after a SET() are collapsed into the SET()
        self._run_and_check_ir(',[-]--', [ir.INPUT(), ir.SET(254)])
        self._run_and_check_ir(',[-]-', [ir.INPUT(), ir.SET(255)])
        self._run_and_check_ir(',[-]', [ir.INPUT(), ir.SET(0)])
        self._run_and_check_ir(',[-]+', [ir.INPUT(), ir.SET(1)])
        self._run_and_check_ir(',[-]++', [ir.INPUT(), ir.SET(2)])
        self._run_and_check_ir(',[+]--', [ir.INPUT(), ir.SET(254)])
        self._run_and_check_ir(',[+]-', [ir.INPUT(), ir.SET(255)])
        self._run_and_check_ir(',[+]', [ir.INPUT(), ir.SET(0)])
        self._run_and_check_ir(',[+]+', [ir.INPUT(), ir.SET(1)])
        self._run_and_check_ir(',[+]++', [ir.INPUT(), ir.SET(2)])


    ##
    ## Copy loops
    ##

    def test_copy_loop_not_optimizeable(self):
        # loop must end where it started
        self._run_and_check_ir(',[->+]',
                               [ir.INPUT(), ir.OPEN(), ir.SUB(1), ir.RIGHT(1),
                                ir.ADD(1), ir.CLOSE()],
                               maxdepth=2)
        self._run_and_check_ir(',[->+<<]',
                               [ir.INPUT(), ir.OPEN(), ir.SUB(1), ir.RIGHT(1),
                                ir.ADD(1), ir.LEFT(2), ir.CLOSE()],
                               maxdepth=2)

        # must subtract 1 from cell 0 exactly once
        self._run_and_check_ir(',[->+<-]',
                               [ir.INPUT(), ir.OPEN(), ir.SUB(1), ir.RIGHT(1),
                                ir.ADD(1), ir.LEFT(1), ir.SUB(1), ir.CLOSE()],
                               maxdepth=2)
        self._run_and_check_ir(',[+>+<--]',
                               [ir.INPUT(), ir.OPEN(), ir.ADD(1), ir.RIGHT(1),
                                ir.ADD(1), ir.LEFT(1), ir.SUB(2), ir.CLOSE()],
                               maxdepth=2)
        self._run_and_check_ir(',[->+<+<->-]',
                               [ir.INPUT(), ir.OPEN(), ir.SUB(1), ir.RIGHT(1),
                                ir.ADD(1), ir.LEFT(1), ir.ADD(1), ir.LEFT(1),
                                ir.SUB(1), ir.RIGHT(1), ir.SUB(1), ir.CLOSE()],
                               maxdepth=2)

        # must be fewer than 127 < and 127 >
        self._run_and_check_ir(',[-' + '>' * 127 + '+' + '<' * 127 + ']',
                               [ir.INPUT(), ir.OPEN(), ir.SUB(1), ir.RIGHT(127),
                                ir.ADD(1), ir.LEFT(127), ir.CLOSE()],
                               maxdepth=2)
        self._run_and_check_ir(',[-' + '<' * 127 + '+' + '>' * 127 + ']',
                               [ir.INPUT(), ir.OPEN(), ir.SUB(1), ir.LEFT(127),
                                ir.ADD(1), ir.RIGHT(127), ir.CLOSE()],
                               maxdepth=2)

    def test_copy_loop_simple(self):
        # single cell copy loops
        self._run_and_check_ir(',[->+<]',
                               [ir.INPUT(), ir.RMUL(1,1), ir.SET(0)])
        self._run_and_check_ir(',[->-<]',
                               [ir.INPUT(), ir.RMUL(1,255), ir.SET(0)])
        self._run_and_check_ir(',[-<+>]',
                               [ir.INPUT(), ir.LMUL(1,1), ir.SET(0)])
        self._run_and_check_ir(',[-<->]',
                               [ir.INPUT(), ir.LMUL(1,255), ir.SET(0)])
        self._run_and_check_ir(',[<->-]',
                               [ir.INPUT(), ir.LMUL(1,255), ir.SET(0)])
        self._run_and_check_ir(',[>+<-]',
                               [ir.INPUT(), ir.RMUL(1,1), ir.SET(0)])

    def test_copy_loop_multiple_separate_offsets(self):
        # 2 offsets
        self._run_and_check_ir(',[->+>+<<]',
                               [ir.INPUT(), ir.RMUL(1,1), ir.RMUL(2,1),
                                ir.SET(0)])
        self._run_and_check_ir(',[->->-<<]',
                               [ir.INPUT(), ir.RMUL(1,255), ir.RMUL(2,255),
                                ir.SET(0)])
        self._run_and_check_ir(',[<+>>-<-]',
                               [ir.INPUT(), ir.LMUL(1,1), ir.RMUL(1,255),
                                ir.SET(0)])

        # many but less than 127 offsets
        self._run_and_check_ir(',[-' + '<+' * 126 + '>' * 126 + ']',
                               [ir.INPUT()] +
                               [ir.LMUL(i,1) for i in range(1,127)] +
                               [ir.SET(0)])
        self._run_and_check_ir(',[<<<+>>>>>-<<<<<<<+>>>>>-<+>]',
                               [ir.INPUT(),
                                ir.LMUL(3, 1), ir.RMUL(2,255),
                                ir.LMUL(5, 1), ir.LMUL(1, 1),
                                ir.SET(0)])

    def test_copy_loop_multiple_repeated_offsets(self):
        # repeated offsets result in multiple LMUL/RMUL
        self._run_and_check_ir(',[->+>++<+++>----<<]',
                               [ir.INPUT(),
                                ir.RMUL(1,1), ir.RMUL(2,2),
                                ir.RMUL(1,3), ir.RMUL(2,252),
                                ir.SET(0)])

    def test_copy_loop_wrap_around(self):
        self._run_and_check_ir(',[->' + '+' * 255 + '<]',
                               [ir.INPUT(), ir.RMUL(1, 255), ir.SET(0)])
        self._run_and_check_ir(',[->' + '+' * 256 + '<]',
                               [ir.INPUT(), ir.SET(0)])
        self._run_and_check_ir(',[->' + '+' * 257 + '<]',
                               [ir.INPUT(), ir.RMUL(1, 1), ir.SET(0)])
        self._run_and_check_ir(',[-<<' + '-' * 255 + '>>]',
                               [ir.INPUT(), ir.LMUL(2, 1), ir.SET(0)])
        self._run_and_check_ir(',[-<<' + '-' * 256 + '>>]',
                               [ir.INPUT(), ir.SET(0)])
        self._run_and_check_ir(',[-<<' + '-' * 257 + '>>]',
                               [ir.INPUT(), ir.LMUL(2, 255), ir.SET(0)])


    ##
    ## Target string
    ##

    def _run_and_check_target(self, default_target, target, program, ir=[]):
        default_target = 17 # some target
        out, mem = self.run_bf(self.code, program,
                               precondition=[default_target], steps=500000)
        self.assertEqual(out, [], "frontend should not produce output")
        self._check_post_condition(mem, ir, target=target)

    def test_target_empty(self):
        self._run_and_check_target(17, 17, "")
        self._run_and_check_target(17, 17, "@")
        self._run_and_check_target(17, 17, " @")
        self._run_and_check_target(17, 17, " @ ")
        self._run_and_check_target(17, 17, "\n")
        self._run_and_check_target(17, 17, "@\n")
        self._run_and_check_target(17, 17, " @\n")
        self._run_and_check_target(17, 17, " @ \n")

    def test_target_incomplete(self):
        self._run_and_check_target(17, 17, "@lang_")
        self._run_and_check_target(17, 17, "@lang_ ")
        self._run_and_check_target(17, 17, "@lang_\n")
        self._run_and_check_target(17, 17, "@lang_+", ir=[ir.ADD(1)])

        self._run_and_check_target(17, 17, "@386_linu")
        self._run_and_check_target(17, 17, "@386_linu ")
        self._run_and_check_target(17, 17, "@386_linu\n")
        self._run_and_check_target(17, 17, "@386_linu_.", ir=[ir.OUTPUT()])

    def test_target_lang_c(self):
        self._run_and_check_target(17, _LANG_C, "@lang_c ")
        self._run_and_check_target(17, _LANG_C, "@lang_c\n")
        self._run_and_check_target(17, _LANG_C, "@lang_c+", ir=[ir.ADD(1)])
        self._run_and_check_target(17, _LANG_C, "@lang_c.+",
                                   ir=[ir.OUTPUT(), ir.ADD(1)])
        self._run_and_check_target(17, _LANG_C, "@lang_c[.]")
        self._run_and_check_target(17, _LANG_C, "@lang_c..",
                                   ir=[ir.OUTPUT(), ir.OUTPUT()])

    def test_target_386_linux(self):
        self._run_and_check_target(17, _386_LINUX, "@386_linux ")
        self._run_and_check_target(17, _386_LINUX, "@386_linux,,",
                                   ir=[ir.INPUT(), ir.INPUT()])
        self._run_and_check_target(17, _386_LINUX, "@386_linux->",
                                   ir=[ir.SUB(1), ir.RIGHT(1)])
        self._run_and_check_target(17, _386_LINUX, "@386_linux[foobar]")
        self._run_and_check_target(17, _386_LINUX, "@386_linux foobar")


    ##
    ## Other stuff
    ##

    def _run_and_check_mismatched(self, program):
        out, mem = self.run_bf(self.code, program,
                               precondition=[1], steps=5000000)
        self.assertEqual(''.join(chr(c) for c in out),
                          'Error: unbalanced brackets!\n')
        self.assertEqual(mem[2], 0, "code should not be marked as ok")

    def test_unbalanced_loop(self):
        self._run_and_check_mismatched("[")
        self._run_and_check_mismatched("+[")
        self._run_and_check_mismatched("+[-]>[")
        self._run_and_check_mismatched("+[-]>[+++<.")
        self._run_and_check_mismatched("+[+]>[+++<.[,,+>]")
        self._run_and_check_mismatched("+[-]>[+++<.[,,+>]]+]")
        self._run_and_check_mismatched("]")
        self._run_and_check_mismatched("]++")
        self._run_and_check_mismatched("]++[+]")
        self._run_and_check_mismatched("]++[+]+[")
        self._run_and_check_mismatched("][")


if __name__ == "__main__":
    import unittest
    unittest.main()
