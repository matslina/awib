import subprocess
import os

import backend


class GoTest(backend.LangGenericTestCase):
    BACKEND_INDEX = 4
    MAX_NESTED_LOOPS = 95

    def run_program(self, path, input):
        os.rename(path, path + ".go")
        subprocess.call(["go", "build", "-o", path, path + ".go"])
        p = subprocess.Popen([path],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate(input)
        self.assertEqual(p.returncode, 0)
        return stdout


if __name__ == "__main__":
    import unittest
    unittest.main()
