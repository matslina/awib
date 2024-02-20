import subprocess
import os

import backend


class LinuxTestCase(backend.BackendTestCase):
    BACKEND_PATH = "lang_c/backend.b"
    BACKEND_INDEX = 2

    cc_flags = []

    def __init__(self, *args, **kwargs):
        super(LinuxTestCase, self).__init__(*args, **kwargs)

        p = subprocess.Popen(['gcc', '-v'], stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        self.assertEquals(p.returncode, 0)

        if "clang" in stderr.decode("utf-8"):
            self.cc_flags = ["-fbracket-depth=512"]

    def run_program(self, path, input):
        os.rename(path, path + ".c")
        subprocess.call(['gcc', path + ".c", '-o', path] + self.cc_flags)
        p = subprocess.Popen([path],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate(input)
        self.assertEquals(p.returncode, 0)
        return stdout


if __name__ == "__main__":
    import unittest
    unittest.main()
