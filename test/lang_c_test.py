import subprocess
import os

import backend


class LinuxTestCase(backend.BackendTestCase):
    BACKEND_PATH = "lang_c/backend.b"

    def run_program(self, path, input):
        os.rename(path, path + ".c")
        subprocess.call(['gcc', path + ".c", '-o', path])
        p = subprocess.Popen([path],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate(input)
        self.assertEquals(p.returncode, 0)
        return stdout


if __name__ == "__main__":
    import unittest
    unittest.main()
