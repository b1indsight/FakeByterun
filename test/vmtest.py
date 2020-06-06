import unittest
import textwrap
import dis
import types
import sys
from src.pyvm2 import VirtualMachine


def dis_code(code):
    """Disassemble `code` and all the code it refers to."""
    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            dis_code(const)

    print("")
    print(code)
    dis.dis(code)

class redirect:
    content = ""

    def write(self,str):
        self.content += str

    def flush(self):
        self.content = ""

    def getValue(self):
        return self.content

class vmtest(unittest.TestCase):

    def assert_eval_OK(self, code):
        code = textwrap.dedent(code)
        code = compile(code, "<%s>" % self.id(), "exec", 0, 1)

        dis_code(code)

        real_stdout = sys.stdout

        vm_stdout = redirect()
        sys.stdout = vm_stdout
        vm = VirtualMachine()
        vm_value = vm.run_code(code)
        vm_print = vm_stdout.getValue()
        real_stdout.write(vm_print)
        

        py_value = py_exc = None
        py_stdout = redirect()
        sys.stdout = py_stdout
        globs = {}
        try:
            py_value = eval(code, globs, globs)
        except AssertionError:              # pragma: no cover
            raise
        except Exception as e:
            py_exc = e
        py_print = py_stdout.getValue()
        real_stdout.write(py_print)

        sys.stdout = real_stdout

        self.assertEqual(vm_print, py_print)
        self.assertEqual(vm_value, py_value)
