# -*- coding: utf-8 -*-
import subprocess
import os

import backend


class JavaTestCase(backend.BackendTestCase):
    BACKEND_PATH = "lang_java/backend.b"
    BACKEND_INDEX = 8

    def run_program(self, path, input):
        tmpd = os.path.dirname(path)
        os.rename(path, os.path.join(tmpd, "Bf.java"))
        subprocess.call(["javac", os.path.join(tmpd, "Bf.java")])
        p = subprocess.Popen(["java", '-cp', tmpd, 'Bf'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate(input)
        self.assertEquals(p.returncode, 0)
        return stdout

    def test_deep_nested_loops(self):
        pass # test is _very_ slow for this backend


if __name__ == "__main__":
    import unittest
    unittest.main()
