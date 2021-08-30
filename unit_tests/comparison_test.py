import unittest
import subprocess
import platform

# if platform.system() in ["Darwin", "Linux"]:
#     equal_output = subprocess.Popen(["a.out"], stdout=subprocess.PIPE).communicate()[0]
# else:
#     # The host OS is Windows
#     equal_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]

class ComparisonTest(unittest.TestCase):
    def test_less_than(self):
        subprocess.call(["python", "main.py", "less_than.golf"])
        subprocess.call(["clang", "compiled_tests/less_than.ll"])
        if platform.system() in ["Darwin", "Linux"]:
            equal_output = subprocess.Popen(["a.out"], stdout=subprocess.PIPE).communicate()[0]
        else:
            # The host OS is Windows
            equal_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(equal_output.strip()), 0)

    def test_greater_than(self):
        subprocess.call(["python", "main.py", "greater_than.golf"])
        subprocess.call(["clang", "compiled_tests/greater_than.ll"])
        if platform.system() in ["Darwin", "Linux"]:
            equal_output = subprocess.Popen(["a.out"], stdout=subprocess.PIPE).communicate()[0]
        else:
            # The host OS is Windows
            equal_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(equal_output.strip()), 1)

    def test_less_than_equal(self):
        subprocess.call(["python", "main.py", "less_equal.golf"])
        subprocess.call(["clang", "compiled_tests/less_equal.ll"])
        if platform.system() in ["Darwin", "Linux"]:
            equal_output = subprocess.Popen(["a.out"], stdout=subprocess.PIPE).communicate()[0]
        else:
            # The host OS is Windows
            equal_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(equal_output.strip()), 0)

    def test_greater_than_equal(self):
        subprocess.call(["python", "main.py", "greater_equal.golf"])
        subprocess.call(["clang", "compiled_tests/greater_equal.ll"])
        if platform.system() in ["Darwin", "Linux"]:
            equal_output = subprocess.Popen(["a.out"], stdout=subprocess.PIPE).communicate()[0]
        else:
            # The host OS is Windows
            equal_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(equal_output.strip()), 1)

    def test_equal(self):
        subprocess.call(["python", "main.py", "equal_test.golf"])
        subprocess.call(["clang", "compiled_tests/equal_test.ll"])
        if platform.system() in ["Darwin", "Linux"]:
            equal_output = subprocess.Popen(["a.out"], stdout=subprocess.PIPE).communicate()[0]
        else:
            # The host OS is Windows
            equal_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(equal_output.strip()), 0)

    def test_not_equal(self):
        subprocess.call(["python", "main.py", "not_equal_test.golf"])
        subprocess.call(["clang", "compiled_tests/not_equal_test.ll"])
        if platform.system() in ["Darwin", "Linux"]:
            equal_output = subprocess.Popen(["a.out"], stdout=subprocess.PIPE).communicate()[0]
        else:
            # The host OS is Windows
            equal_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(equal_output.strip()), 1)


if __name__ == '__main__':
    unittest.main()
