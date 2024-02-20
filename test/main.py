import unittest
import sys

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    if len(sys.argv) > 1:
        for test_name in sys.argv[1:]:
            suite.addTest(loader.loadTestsFromName(test_name))
    else:
        suite = loader.discover('.', pattern='*_test.py')

    runner = unittest.TextTestRunner()
    runner.run(suite)
