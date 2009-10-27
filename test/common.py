# -*- coding: utf-8 -*-

import unittest

from awip import AWIP, AWIPError, AWIPStepError

def _diff_pos(a,b):
    for i in xrange(min(len(a), len(b))):
        if a[i] != b[i]:
            return i
    return -1

class BFTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.__code = None

    def run_bf(self, code, input, steps=50000,
            check_output=True, check_memory=True, precondition=[]):
        """Runs code with different cell size and eof-behaviour.

        @param input: program input
        @param steps: number of AWIP IR operations before failing
        @param check_output: assert output is equal regardless of environment
        @param check_memory: assert memory post execution is equal ...
        @param precondition: run program with this initial memory layout
        @rtype: ([], [])
        @return: program output and memory post execution as: (output, memory)
        """

        if self.__code != code:
            self._interpreter = AWIP(code)
            self.__code = code

        output, memory, prev_cs, prev_eb = None, None, None, None

        for cell_size in (8,16,64):
            for eof__code, eof_name in\
                    ((AWIP.EOF_NO_CHANGE, "no change"),
                     (AWIP.EOF_WRITE_ZERO, "write zero"),
                     (AWIP.EOF_WRITE_MINUS_ONE, "write minus one")):

                try:
                    out, mem = self._interpreter.run(input=input,
                                                     memory=precondition,
                                                     cell_size=cell_size,
                                                     eof_behaviour=eof__code,
                                                     steps=steps)
                except AWIPStepError:
                    self.fail("code didn't terminate within %d steps for "
                              "(%d bits, %s)" %
                              (steps, cell_size, eof_name))
                except AWIPError, ae:
                    self.fail("code fails for (%d bits, %s): %s" %
                              (cell_size, eof_name, ae))

                if output is None:
                    output = out
                elif check_output and output != out:
                    i = _diff_pos(output, out)
                    self.fail("output differs between (%d bits, %s) and "
                              "(%d bits, %s) in position %d: 0x%02x != 0x%02x" %
                              (cell_size, eof_name, prev_cs, prev_eb,
                               i, out[i], output[i]))

                if memory is None:
                    memory = mem
                elif check_memory and memory != mem:
                    i = _diff_pos(memory, mem)
                    self.fail("memory (post exec) differs between "
                              "(%d bits, %s) and (%d bits, %s) in position"
                              " %d: 0x%02x != 0x%02x" %
                              (cell_size, eof_name, prev_cs, prev_eb,
                               i, mem[i], memory[i]))

                prev_cs, prev_eb = cell_size, eof_name

        for i in xrange(len(memory)-1, -1, -1):
            if memory[i] != 0:
                break

        return (output, memory[:i+1])
