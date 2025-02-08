import os
import sys
import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    if len(sys.argv) > 1:
        for test_name in sys.argv[1:]:
            suite.addTest(loader.loadTestsFromName(test_name))
    else:
        suite = loader.discover('.', pattern='*_test.py')

    verbosity = 2 if os.getenv("CI") else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    if not result.wasSuccessful():
        sys.exit(1)
    else:
        sys.exit(0)
