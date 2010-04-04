# -*- coding: utf-8 -*-
# Copyright (c) 2010 Spotify AB

import subprocess
import os

import backend


class GoTest(backend.LangGenericTestCase):
    BACKEND_INDEX = 4

    def run_program(self, path, input):
        os.rename(path, path + ".go")
        subprocess.call(["8g", "-o", path + ".8", path + ".go"])
        subprocess.call(["8l", "-o", path, path + ".8"])
        p = subprocess.Popen([path],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate(input)
        self.assertEquals(p.returncode, 0)
        return stdout


if __name__ == "__main__":
    import unittest
    unittest.main()
