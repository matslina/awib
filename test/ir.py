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

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.arg == other.arg

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def from_code(self, s):
        if len(s) != 2:
            raise ValueError("single op spans 2 codes")
        if s[0] not in op:
            raise ValueError("unknown op code %d" % s[0])
        return op[s[0]](s[1])

class WideOp(object):
    """Represents a wide 4 byte IR operation."""

    ranges = ([0], [0])

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __str__(self):
        codes = [self.code, self._x, self.padding, self._y]
        return ''.join(map(chr, codes))

    def __repr__(self):
        return "%s(%d, %d)" % (self.__class__.__name__,
                               self._x, self._y)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        return (other.__class__ == self.__class__ and
                other._x == self._x and
                other._y == self._y)

    @classmethod
    def from_code(self, s):
        if len(s) != 4:
            raise ValueError("wide op spans 4 codes")
        if s[0] not in op:
            raise ValueError("unknown op code %d" % s[0])
        if s[2] != self.padding:
            raise ValueError("wide op %d need padding %d, got %d" %
                             (s[0], self.padding, s[2]))
        return op[s[0]](s[1], s[3])


class ADD(Op):
    code = 1
    range = xrange(1,256)
class SUB(Op):
    code = 3
    range = xrange(1,256)
class LEFT(Op):
    code = 5
    range = xrange(1,256)
class RIGHT(Op):
    code = 6
    range = xrange(1,256)
class INPUT(Op): code = 2
class OUTPUT(Op): code = 4
class OPEN(Op): code = 7
class CLOSE(Op): code = 8
class SET(Op):
    code = 9
    range = xrange(0,256)

class LMUL(WideOp):
    code = 10
    padding = 11
    range = (xrange(1,128), xrange(1,256))
class RMUL(WideOp):
    code = 12
    padding = 13
    range = (xrange(1,128), xrange(1,256))

op = dict((op.code, op) for op in [ADD,SUB,LEFT,RIGHT,INPUT,OUTPUT,
                                   OPEN,CLOSE,SET,LMUL,RMUL])

def parse_codes(c):
    ops = []
    i = 0
    while i < len(c):
        if c[i] not in op:
            raise ValueError("unknown code at pos %d: %d" % (i, c[i]))
        if issubclass(op[c[i]], WideOp):
            ops.append(op[c[i]].from_code(c[i:i+4]))
            i += 4
        else:
            ops.append(op[c[i]].from_code(c[i:i+2]))
            i += 2
    return ops

