# -*- coding: utf-8 -*-

"""Utilities and data related to the awib intermediate representation."""

class Op(object):
    """Represents an IR operation."""

    range = [0]

    def __init__(self, arg=0):
        if arg not in self.range:
            raise ValueError("argument %s out of range" % arg)
        self.arg = arg

    def __str__(self):
        return chr(self.code) + chr(self.arg)

    def __repr__(self):
        return "%s(%d)" % (self.__class__.__name__, self.arg)

    @classmethod
    def from_str(self, s):
        if len(s) != 2:
            raise ValueError("string rep of single op must have length 2")

        if s[0] not in code_to_op:
            raise ValueError("unknown op code %d" % ord(s[0]))

        return code_to_op[s[0]](s[1])

class ADD(Op):
    code = 1
    range = xrange(1,256)
class SUB(Op):
    code = 3
    range = xrange(1,256)
class LEFT(Op):
    code = 5
    range = xrange(1,128)
class RIGHT(Op):
    code = 6
    range = xrange(1,128)
class INPUT(Op): code = 2
class OUTPUT(Op): code = 4
class OPEN(Op): code = 7
class CLOSE(Op): code = 8
class SET(Op):
    code = 9
    range = xrange(0,256)

operations = [ADD, SUB, LEFT, RIGHT, INPUT, OUTPUT, CLOSE, OPEN, SET]

code_to_op = dict((op.code, op) for op in operations)
