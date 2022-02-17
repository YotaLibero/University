import unittest
from Module_calc import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        self.assertEqual(self.calculator.add(4, 7), 11)

    def test_subtract(self):
        self.assertEqual(self.calculator.subtract(10, 5), 5)

    def test_multiply(self):
        self.assertEqual(self.calculator.multiply(3, 7), 21)

    def test_divide(self):
        self.assertEqual(self.calculator.divide(10, 2), 5)

    def test_square(self):
        self.assertEqual(self.calculator.square(3.2, -7.8, 1), "x1 = 2.3  и  x2 = 0.14")
        self.assertEqual(self.calculator.square(2, 4, 2), "x = -1.0")
        self.assertEqual(self.calculator.square(8, 4, 2), "Корней нет")


# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
