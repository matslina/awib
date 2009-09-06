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

    def _post_condition(self, data, code,
                        assert_sane=True):
        """Parses and checks frontend memory post condition."""

        # T *0 b (code) 0 M m
        # where b = (bytecode OK ? 1 : 0) and Mm = maximum loop depth

        # sanity check output
        self.assert_(len(data) >= 6,
                     "expected at least 6 cells, got %d" % len(data))

        self.assert_(data[0] in (_LANG_C, _386_LINUX), "bad target platform T")
        self.assertEquals(data[1], 0, "cell intentionally left blank")
        self.assert_(data[2], "bytecode not OK")

        # find end of code block
        i = 3
        while i < len(data) and data[i] != 0:
            i += 2

        # sanity
        self.assert_( not (len(data) < i+3), "maximum loop depth is missing")
        self.assert_( not (len(data) > i+3), "junk data beyond max loop depth")
        self.assertEquals((i-3)/2, len(code),
                          "expected %d ops, got %d" % (len(code), (i-3)/2))

        # compare frontend output with expected byte code
        for i in xrange(len(code)):
            if data[2*i + 3] not in ir.code_to_op:
                self.fail("invalid code at pos %d: %d" % (i, data[2*i]))
            op_cls = ir.code_to_op[data[2*i]]

            try:
                op = op_cls(data[2*i+1])
            except ValueError, ve:
                self.fail("invalid op at pos %d: %d" % (i, ve))

            if code[i].__class__ != op.__class__ or code[i].arg != op.arg:
                self.fail("expected %r but got %r at op %d" % (op, code[i], i))

    def test_empty_input(self):
        out, mem = self.run_bf(self.code, "", precondition=[1])

        self.assertEquals(out, [])
        pc = self._post_condition(mem, [])

if __name__ == "__main__":
    import unittest
    unittest.main()
