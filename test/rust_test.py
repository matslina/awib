import subprocess
import os

import backend


class RustTest(backend.LangGenericTestCase):
    BACKEND_INDEX = 3
    MAX_NESTED_LOOPS = 95

    def run_program(self, path, input):
        os.rename(path, path + ".rs")
        subprocess.call(["rustc", path + ".rs", "-o", path])
        p = subprocess.Popen([path],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate(input)
        self.assertEqual(p.returncode, 0)
        return stdout


if __name__ == "__main__":
    import unittest
    unittest.main()
