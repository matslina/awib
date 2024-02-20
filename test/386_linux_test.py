import subprocess

import backend
import ir

class LinuxTestCase(backend.BackendTestCase):
    BACKEND_PATH = "386_linux/backend.b"
    BACKEND_INDEX = 1

    def run_program(self, path, input):
        subprocess.call(['chmod', '+x', path])
        p = subprocess.Popen([path],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate(input)
        self.assertEqual(p.returncode, 0)
        return stdout

    def test_deep_nested_loops(self):
        pass # test is _very_ slow for this backend

    def test_left_right(self):
        # the 386_linux backend outputs different machine instructions
        # for LEFT and RIGHT depending on the size of the
        # argument. this tests the edge cases.

        ops = []

        # set up memory to 0,1,2,...,255,0,0,0,...
        for i in range(256):
            ops.append(ir.SET(i))
            ops.append(ir.RIGHT(1))

        # jump all the "edgy" distances left and right and output
        edges = [1, 2, 3, 4, 126, 127, 128, 129, 130, 131, 253, 254, 255]
        for i in edges:
            ops.append(ir.LEFT(i))
            ops.append(ir.OUTPUT())
            ops.append(ir.RIGHT(i))
            ops.append(ir.OUTPUT())

        # expected output is 0 alternated with all the edges
        expected = []
        for i in edges:
            expected.append(256 - i)
            expected.append(0)

        self.run_ir(ops, [], expected)

    def test_left_right_loop(self):
        # Previously had a bug where code was emitted correctly, but
        # size of machine code was incorrectly calculated in the
        # left-right edge cases. This is similar to the left_right
        # test, but wraps the LEFT/RIGHT in a loop to trigger crashes
        # if size of machine code is miscalculated.

        def ops(d):
            ops = []
            # first use only LEFT(1) and RIGHT(1) to set up memory
            ops += ([ir.RIGHT(1)] * (d) + [ir.SET(12)] +
                    [ir.RIGHT(1)] * (d) + [ir.SET(32)] +
                    [ir.RIGHT(1)] * (d) + [ir.SET(17)] +
                    [ir.LEFT(1)] * (d * 2))

            # state:   0(d) *12 0(d - 1) 32 0(d - 1) 17 0

            # run a [.>>>>] construct to move up the pointer. this
            # should output 12, 32 and 17.
            ops += ([ir.OPEN(), ir.OUTPUT(), ir.RIGHT(d), ir.CLOSE()])

            # state:   0(d) 12 0(d - 1) 32 0(d - 1) 17 0(d - 1) *0

            # same thing in other direction. should output 17,32
            ops += [ir.LEFT(d)]
            ops += ([ir.OPEN(), ir.OUTPUT(), ir.LEFT(d), ir.CLOSE()])

            return ops

        self.run_ir(ops(1), [], [12, 32, 17, 17, 32, 12])
        self.run_ir(ops(2), [], [12, 32, 17, 17, 32, 12])
        self.run_ir(ops(3), [], [12, 32, 17, 17, 32, 12])
        self.run_ir(ops(4), [], [12, 32, 17, 17, 32, 12])
        self.run_ir(ops(127), [], [12, 32, 17, 17, 32, 12])
        self.run_ir(ops(128), [], [12, 32, 17, 17, 32, 12])
        self.run_ir(ops(129), [], [12, 32, 17, 17, 32, 12])
        self.run_ir(ops(130), [], [12, 32, 17, 17, 32, 12])
        self.run_ir(ops(254), [], [12, 32, 17, 17, 32, 12], steps=10000000)
        self.run_ir(ops(255), [], [12, 32, 17, 17, 32, 12], steps=10000000)


if __name__ == "__main__":
    import unittest
    unittest.main()
