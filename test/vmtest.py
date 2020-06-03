import unittest
import textwrap
import dis
import types
from src.pyvm2 import VirtualMachine


def dis_code(code):
    """Disassemble `code` and all the code it refers to."""
    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            dis_code(const)

    print("")
    print(code)
    dis.dis(code)


class vmtest(unittest.TestCase):

    def assert_eval_OK(self, code):
        code = textwrap.dedent(code)
        code = compile(code, "<%s>" % self.id(), "exec", 0, 1)

        dis_code(code)

        vm = VirtualMachine()
        vm_value = vm.run_code(code)

        py_value = py_exc = None
        globs = {}
        try:
            py_value = eval(code, globs, globs)
        except AssertionError:              # pragma: no cover
            raise
        except Exception as e:
            py_exc = e

        self.assertEqual(vm_value, py_value)

