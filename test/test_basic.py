import unittest
from vmtest import vmtest


class testBasic(vmtest):

    def test_constant(self):
        self.assert_eval_OK("17")

    def test_add(self):
        self.assert_eval_OK("1 + 2")

    def test_val(self):
        self.assert_eval_OK("a = 1")

    def test_dec(self):
        self.assert_eval_OK("""\
            a = 2
            b = a - 1
                """)

    def test_mul(self):
        self.assert_eval_OK("""\
            a = 2
            b = a * 1
                """)

    def test_div(self):
        self.assert_eval_OK("""\
            a = 2
            b = a / 1
                """)

    def test_complex(self):
        self.assert_eval_OK("""\
            a = 2
            b = a - 1
            c = (a * 2) + (b / 3)
                """)

    def test_define_function(self):
        self.assert_eval_OK("""\
            def a(x):
                return x + 1
                """)

    def test_call_function(self):
        self.assert_eval_OK("""\
            def a(x, y):
                return x + y + 1
            b = a(2, 1)
            """)

    def test_loop(self):
        self.assert_eval_OK("""\
            a = 10
            while a > 2:
                a -= 1
            """)

    def test_print(self):
        self.assert_eval_OK("""\
            print("test")
            """)

    