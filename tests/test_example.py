import unittest
from python_pypi_package_template import Example


class test_example(unittest.TestCase):
    def test_example(self):
        self.assertTrue(Example.run())


if __name__ == '__main__':
    unittest.main()
