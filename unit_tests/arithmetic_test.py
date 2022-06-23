import unittest
import subprocess
import platform

class ArithmeticTest(unittest.TestCase):
    def test_addition(self):
        subprocess.call(["python", "main.py", "addition.golf"])
        subprocess.call(["clang", "compiled_tests/addition.ll"])
        if platform.system() in ["Darwin", "Linux"]:
            plus_output = subprocess.Popen(["a.out"], stdout=subprocess.PIPE).communicate()[0]
        else:
            # The host OS is Windows
            plus_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(plus_output.strip()), 5.0)

    def test_subtraction(self):
        subprocess.call(["python", "main.py", "subtraction.golf"])
        subprocess.call(["clang", "compiled_tests/subtraction.ll"])
        if platform.system() in ["Darwin", "Linux"]:
            sub_output = subprocess.Popen(["a.out"], stdout=subprocess.PIPE).communicate()[0]
        else:
            # The host OS is Windows
            sub_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(sub_output.strip()), 4.0)

    def test_multiply(self):
        subprocess.call(["python", "main.py", "multiply.golf"])
        subprocess.call(["clang", "compiled_tests/multiply.ll"])
        if platform.system() in ["Darwin", "Linux"]:
            mult_output = subprocess.Popen(["a.out"], stdout=subprocess.PIPE).communicate()[0]
        else:
            # The host OS is Windows
            mult_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(mult_output.strip()), 12.0)

    def test_divide(self):
        subprocess.call(["python", "main.py", "normal_divide.golf"])
        subprocess.call(["clang", "compiled_tests/normal_divide.ll"])
        if platform.system() in ["Darwin", "Linux"]:
            div_output = subprocess.Popen(["a.out"], stdout=subprocess.PIPE).communicate()[0]
        else:
            # The host OS is Windows
            div_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(div_output.strip()), 2.0)

    def test_modulus(self):
        subprocess.call(["python", "main.py", "modulus.golf"])
        subprocess.call(["clang", "compiled_tests/modulus.ll"])
        if platform.system() in ["Darwin", "Linux"]:
            mod_output = subprocess.Popen(["a.out"], stdout=subprocess.PIPE).communicate()[0]
        else:
            # The host OS is Windows
            mod_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(mod_output.strip()), 4.0)

    def test_increment(self):
        subprocess.call(["python", "main.py", "increment.golf"])
        subprocess.call(["clang", "compiled_tests/increment.ll"])
        if platform.system() in ["Darwin", "Linux"]:
            inc_output = subprocess.Popen(["a.out"], stdout=subprocess.PIPE).communicate()[0]
        else:
            # The host OS is Windows
            inc_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(inc_output.strip()), 5.1)

    def test_decrement(self):
        subprocess.call(["python", "main.py", "decrement_test.golf"])
        subprocess.call(["clang", "compiled_tests/decrement_test.ll"])
        if platform.system() in ["Darwin", "Linux"]:
            dec_output = subprocess.Popen(["a.out"], stdout=subprocess.PIPE).communicate()[0]
        else:
            # The host OS is Windows
            dec_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(dec_output.strip()), -1.2)


if __name__ == '__main__':
    unittest.main()
