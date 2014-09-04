import unittest

class TestTemplate(unittest.TestCase):

    def testPass(self):
        self.assertTrue(True)

    def testFail(self):
        self.assertTrue(False)

    def testError(self):
        raise RuntimeError('Test error!')

if __name__ == '__main__':
    unittest.main()

