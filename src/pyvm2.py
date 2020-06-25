import dis
import sys
from .function import Function
from .frame import frame
from .pyclass import pyClass
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
            return bytecode_fn(*arguments)
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
            state = self.dispatch(byteName, arguments)
            if state == "return":
                break
        
    # BYTE CODE
    #-------------------------------------------------------
    def NOP(self):
        pass

    def POP_TOP(self):
        self.pop()

    def LOAD_CONST(self, number):
        self.push(number)
        

    def LOAD_NAME(self, name):
        retval = self.frame.f_locals.get(name)
        if retval == None:
            retval = self.frame.f_globals.get(name)
            if retval == None:
                retval = self.frame.f_builtins.get(name)
        self.push(retval)

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

    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print(answer)

    def PRINT_NOT_POP(self):
        print(self.stack[-1])

    def jump(self, jump):
        self.frame.last_instruction = jump

    def JUMP_ABSOLUTE(self, jump):
        self.jump(jump)

    def POP_JUMP_IF_FALSE(self, jump):
        val = self.pop()
        if val:
            self.push(val)
            return
        else:
            self.jump(jump)

    def JUMP_FORWARD(self, jump):
        self.jump(self.last_instruction + jump)

    #oprate
    def BINARY_ADD(self):
        first_num = self.pop()
        second_num = self.pop()
        total = first_num + second_num
        self.push(total)

    def BINARY_SUBTRACT(self):
        second_num = self.pop()
        first_num = self.pop()
        total = first_num - second_num
        self.push(total)

    def BINARY_MULTIPLY(self):
        first_num = self.pop()
        second_num = self.pop()
        total = first_num * second_num
        self.push(total)

    def BINARY_TRUE_DIVIDE(self):
        first_num = self.pop()
        second_num = self.pop()
        total = first_num / second_num
        self.push(total)

    def INPLACE_SUBTRACT(self):
        first_num = self.pop()
        second_num = self.pop()
        total = first_num - second_num
        self.push(total)

    def COMPARE_OP(self, arg):
        #TODO: complete compare dic
        compare_dic = [
            lambda x, y: x,
            lambda x, y: x,
            lambda x, y: x == y,
            lambda x, y: x - y < 0,
            lambda x, y: x - y > 0,
        ]
        second_num = self.pop()
        first_num = self.pop()
        if compare_dic[arg](first_num, second_num):
            self.push(1)
        else:
            self.push(0)
    
    #function oprate
    def MAKE_FUNCTION(self, argc):
        name = self.pop()
        code = self.pop()
        defaults = self.popn(argc)
        globs = self.frame.f_globals
        fn = Function(name, code, globs, defaults, None, self)
        self.push(fn)

    def CALL_FUNCTION(self, arg):
        args = self.popn(arg)
        func = self.pop()

        # builtin function and create class function
        if hasattr(func, '__module__'):
            if func.__module__ == 'builtins' or func.__module__ == 'src.pyvm2':
                self.push(func(*args))
                return

        # class __init__ function 
        # TODO：class define function should return the class , but this still return None  
        if isinstance(func, pyClass):
            code = func.init.func_code
        else:
            code = func.func_code

        frame = self.frame
        tmpdic, i = {}, 0
        for x in code.co_varnames:
            tmpdic.update({x:args[i]})
            i += 1
        f = self.make_frame(code, args, tmpdic, frame.f_globals, frame.f_locals)
        self.push(self.run_frame(f)) 

    def RETURN_VALUE(self):
        self.frame.f_back = self.pop()
        retval = self.frame.f_back
        self.pop_frame()
        if not self.frame:
            self.return_value = retval
        else:
            self.push(retval)
        return "return"

    #class oprate
    def LOAD_BUILD_CLASS(self):
        def create_class(func, name):
            return pyClass(func, name)
        self.push(create_class)

    def LOAD_ATTR(self, attr):
        obj = self.pop()
        val = obj.getattr(attr)
        self.push(val)

    def STORE_ATTR(self, attr):
        val, obj = self.popn(2)
        obj.storeattr()