import unittest
import subprocess


class ArithmeticTest(unittest.TestCase):
    def test_addition(self):
        subprocess.call(["python", "main.py", "addition.golf"])
        subprocess.call(["clang", "compiled_tests/addition.ll"])
        plus_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(plus_output.strip()), 5.0)

    def test_subtraction(self):
        subprocess.call(["python", "main.py", "subtraction.golf"])
        subprocess.call(["clang", "compiled_tests/subtraction.ll"])
        sub_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(sub_output.strip()), 4.0)

    def test_multiply(self):
        subprocess.call(["python", "main.py", "multiply.golf"])
        subprocess.call(["clang", "compiled_tests/multiply.ll"])
        sub_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(sub_output.strip()), 12.0)

    def test_divide(self):
        subprocess.call(["python", "main.py", "normal_divide.golf"])
        subprocess.call(["clang", "compiled_tests/normal_divide.ll"])
        sub_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(sub_output.strip()), 2.0)


if __name__ == '__main__':
    unittest.main()
