import unittest
import textwrap
import dis
import types
import sys
from src.pyvm2 import VirtualMachine, VirtualMachineError


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
        vm_value = vm_exc = None
        vm_print = None

        try:
            vm_value = vm.run_code(code)
        except VirtualMachineError:         # pragma: no cover
            # If the VM code raises an error, show it.
            raise
        except AssertionError:              # pragma: no cover
            # If test code fails an assert, show it.
            raise
        except Exception as e:
            raise
            vm_exc = e
        finally:
            real_stdout.write("----- vm stdout ----------\n")
            vm_print = vm_stdout.getValue()
            real_stdout.write(vm_print)
        

        py_value = py_exc = None
        py_stdout = redirect()
        sys.stdout = py_stdout
        py_print = None
        globs = {}
        try:
            py_value = eval(code, globs, globs)
        except AssertionError:              # pragma: no cover
            raise
        except Exception as e:
            raise
            py_exc = e
        finally:
            real_stdout.write("----- py stdout -----------\n")
            py_print = py_stdout.getValue()
            real_stdout.write(py_print)

        sys.stdout = real_stdout

        self.assert_same_exception(vm_exc, py_exc)
        self.assertEqual(vm_print, py_print)
        self.assertEqual(vm_value, py_value)

    def assert_same_exception(self, vm_exc, py_exc):
        self.assertIs(type(vm_exc), type(py_exc))
        self.assertEqual(str(vm_exc), str(py_exc))
