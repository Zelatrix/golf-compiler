import unittest
import subprocess


class ConditionalTest(unittest.TestCase):
    def test_if(self):
        subprocess.call(["python", "main.py", "if_then.golf"])
        subprocess.call(["clang", "compiled_tests/if_then.ll"])
        equal_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
        self.assertAlmostEqual(float(equal_output.strip()), 5.0)

    # def test_if_else(self):
    #     subprocess.call(["python", "main.py", "if_else.golf"])
    #     subprocess.call(["clang", "compiled_tests/if_else.ll"])
    #     equal_output = subprocess.Popen(["a.exe"], stdout=subprocess.PIPE).communicate()[0]
    #     self.assertAlmostEqual(float(equal_output.strip()), 0)


if __name__ == '__main__':
    unittest.main()
