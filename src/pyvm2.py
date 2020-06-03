import dis
import sys
from .function import Function
from .frame import frame
import logging

log = logging.getLogger(__name__)

class VirtualMachineError():
    pass


"""code_obj 

"""


class VirtualMachine:

    def __init__(self):
        self.frames = []   # The call stack of frames.
        self.frame = None  # The current frame.
        self.return_value = None
        self.last_exception = None

    """ This part is used to help oprate the operand stack"""

    def top(self):
        return self.frame.stack[-1]

    def pop(self):
        return self.frame.stack.pop()

    def push(self, *vals):
        self.frame.stack.extend(vals)

    def popn(self, n):
        """Pop a number of values from the value stack.
        A list of `n` values is returned, the deepest value first.
        """
        if n:
            ret = self.frame.stack[-n:]
            self.frame.stack[-n:] = []
            return ret
        else:
            return []

    # NOTE code_obj.co_code is similar to b'd\x00d\x01\x84\x00Z\x00d\x02S\x00'
    # NOTE this function is used to get a {bytecode:argument} dict
    def prase_byte_code_and_argument(self):
        f = self.frame
        opoffset = f.last_instruction
        byteCode = f.f_code.co_code[opoffset]
        byteName = dis.opname[byteCode]
        arg = None
        arguments = []

        f.last_instruction += 2
        byte_name = dis.opname[byteCode]

        if byteCode >= dis.HAVE_ARGUMENT:
            arg = f.f_code.co_code[f.last_instruction-1]
            
            # index into the bytecode
            if byteCode in dis.hasconst:   # Look up a constant
                arg = f.f_code.co_consts[arg]
            elif byteCode in dis.hasname:  # Look up a name
                arg = f.f_code.co_names[arg]
            elif byteCode in dis.haslocal:  # Look up a local name
                arg = f.f_code.co_varnames[arg]
            elif byteCode in dis.hasjrel:  # Calculate a relative jump
                arg = f.last_instruction + arg
            else:
                arg = arg
            argument = [arg]
        else:
            argument = []

        return byte_name, argument, opoffset

    def dispatch(self, byteName, arguments):
        """ Dispatch by bytename to the corresponding methods.
        Exceptions are caught and set on the virtual machine."""
        try:
            # dispatch
            bytecode_fn = getattr(self, byteName)
            if not bytecode_fn:
                raise VirtualMachineError(
                    "unknown bytecode type: %s" % byteName
                )
            bytecode_fn(*arguments)
        except:
            log.exception("here is a exception")

    def run_code(self, code, global_names=None, local_names=None):
        """ An entry point to execute code using the virtual machine."""
        frame = self.make_frame(code, global_names=global_names,
                                local_names=local_names)
        return self.run_frame(frame)

    def make_frame(self, code, position_args=[], callargs={}, global_names=None, local_names=None):
        """create a frame when vm is running, when vm invoke a function ,then create
        a frame

        Arguments:
            code {[type]} -- code object 

        Keyword Arguments:
            callargs {dict} -- args  (default: {{}})
            global_names {[type]} -- [description] (default: {None})
            local_names {[type]} -- [description] (default: {None})

        Returns:
            frame[type] -- [description]
        """
        # log.info("make_frame: code=%r, callargs=%s" % (code, callargs))
        if global_names is not None and local_names is None:
            local_names = global_names
        elif self.frames:
            global_names = self.frame.f_globals
            local_names = {}
        else:
            global_names = local_names = {
                '__builtins__': __builtins__,
                '__name__': '__main__',
                '__doc__': None,
                '__package__': None,
            }
        local_names.update(callargs)
        re_frame = frame(code, global_names, local_names, self.frame)
        return re_frame

    def push_frame(self, frame):
        self.frames.append(frame)
        self.frame = frame

    def pop_frame(self):
        self.frames.pop()
        if self.frames:
            self.frame = self.frames[-1]
        else:
            self.frame = None

    def run_frame(self, frame):
        self.push_frame(frame)
        while True:
            byteName, arguments, opoffset = self.prase_byte_code_and_argument()
            if log.isEnabledFor(logging.INFO):
                self.log(byteName, arguments)
            if (byteName == '<0>'):
                break
            if (byteName == "RETURN_VALUE"):
                self.return_value = self.pop()
                break
            self.dispatch(byteName, arguments)

    # BYTE CODE
    def NOP(self):
        pass

    def LOAD_CONST(self, number):
        self.push(number)
        

    def LOAD_NAME(self, name):
        self.push(self.frame.f_locals.get(name))

    def STORE_NAME(self, name):
        val = self.pop()
        self.frame.f_locals[name] = val

    def LOAD_FAST(self, name):
        if name in self.frame.f_locals:
            val = self.frame.f_locals.get(name)
        else:
            raise UnboundLocalError(
                "local variable '%s' referenced before assignment" % name
            )
        self.push(val)

    def MAKE_FUNCTION(self, argc):
        name = self.pop()
        code = self.pop()
        defaults = self.popn(argc)
        globs = self.frame.f_globals
        fn = Function(name, code, globs, defaults, None, self)
        self.push(fn)

    #TODO: how to get function's arg name and store them into f_locals 
    def CALL_FUNCTION(self, arg):
        args = self.popn(arg)
        func = self.pop()
        frame = self.frame
        code = func.func_code
        
        f = self.make_frame(code, args, {}, frame.f_globals, frame.f_locals)
        self.run_frame(f)

    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print(answer)

    def PRINT_NOT_POP(self):
        print(self.stack[-1])

    def BINARY_ADD(self):
        first_num = self.pop()
        second_num = self.pop()
        total = first_num + second_num
        self.push(total)

    def jump(self, jump):
        self.pc = jump

    def JUMP(self, jump):
        self.jump(jump)

    def POP_JUMP_IF_FALSE(self, jump):
        val = self.stack.pop()
        if val:
            self.stack.append(val)
            return
        else:
            self.jump(jump)
