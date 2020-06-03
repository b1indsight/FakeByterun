import  unittest
from vmtest import vmtest

class testBasic(vmtest):

    def test_constant(self):
        self.assert_eval_OK("17")

    def test_add(self):
        self.assert_eval_OK("1 + 2")

    def test_val(self):
        self.assert_eval_OK("a = 1")

    def test_define_function(self):
        self.assert_eval_OK("""\
            def a(x):
                return x + 1
                """)          

    def test_call_function(self):
        self.assert_eval_OK("""\
            def a(x):
                return x + 1
            b = a(2)""")
            
