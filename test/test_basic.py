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

    def test_class(self):
        self.assert_eval_OK("""\
            class a:
                def __init__(self):
                    self.b = 0
            c = a()
            print(c.b)
            """)

    def test_if(self):
        self.assert_eval_OK("""\
            a = 0
            if a > 0:
                pass
            else:
                a + 1
            print(a)
            """)
    
    def test_break(self):
        self.assert_eval_OK("""\
            a = 5
            while a > 1:
                a = a - 1
                if a == 2:
                    break
            print(a)
            """)
    
    def test_continue(self):
        self.assert_eval_OK("""\
            a = 5
            while a > 1:
                if a == 2:
                    a = 0
                    continue
                a = a - 1
            print(a)
            """)

    def test_basic_error(self):
        self.assert_eval_OK("""\
            x = 10
            while x > 0:
                try:
                    break
                finally:
                    print("Exiting loop")
            """)