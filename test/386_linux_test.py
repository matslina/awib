import subprocess

import backend


class LinuxTestCase(backend.BackendTestCase):
    BACKEND_PATH = "386_linux/backend.b"

    def run_program(self, path, input):
        subprocess.call(['chmod', '+x', path])
        p = subprocess.Popen([path],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        stdout, stderr = p.communicate(input)
        self.assertEquals(p.returncode, 0)
        return stdout


if __name__ == "__main__":
    import unittest
    unittest.main()
