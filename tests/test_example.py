import unittest
from sqlalchemy_model_faker import Example


class test_example(unittest.TestCase):
    def test_example(self):
        self.assertTrue(Example.run())


if __name__ == '__main__':
    unittest.main()
