import subprocess
import os

import backend


class TclTest(backend.LangGenericTestCase):
    BACKEND_INDEX = 7

    def run_program(self, path, input):
        p = subprocess.Popen(['/usr/bin/tclsh',path],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate(input)
        self.assertEqual(p.returncode, 0)
        return stdout


if __name__ == "__main__":
    import unittest
    unittest.main()
