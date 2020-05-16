import frame
from logging import log
import dis
import sys
from function import Function
import logging

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

    #NOTE code_obj.co_code is similar to b'd\x00d\x01\x84\x00Z\x00d\x02S\x00'
    #NOTE this function is used to get a {bytecode:argument} dict
    def prase_byte_code_and_argument(self):
        f = self.frame
        opoffset = f.last_instruction
        byteCode = f.code_obj.co_code[opoffset]
        byteName = dis.opname[byteCode]
        arg = None
        arguments = []
        
        f.last_instruction += 1
        byte_name = dis.opname[byteCode]
        
        if byteCode >= dis.HAVE_ARGUMENT:
            arg = f.f_code.co_code[f.f_lasti:f.f_lasti+2]
            f.last_instruction += 2
            intArg = arg[0] + (arg[1] << 8)
            # index into the bytecode
            if byteCode in dis.hasconst:   # Look up a constant
                arg = f.f_code.co_const[intArg]
            elif byteCode in dis.hasname:  # Look up a name
                arg = f.f_code.co_name[intArg]
            elif byteCode in dis.haslocal: # Look up a local name
                arg = f.f_code.co_varnames[intArg]
            elif byteCode in dis.hasjrel:  # Calculate a relative jump
                arg = f.last_instruction + intArg
            else:
                arg = intArg
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

    def run_code(self, code, global_names=None, local_names=None):
        """ An entry point to execute code using the virtual machine."""
        frame = self.make_frame(code, global_names=global_names, 
                                local_names=local_names)
        return self.run_frame(frame)

    def make_frame(self, code, callargs={}, global_names=None, local_names=None):
        """create a frame when vm is running, when vm invoke a function ,then create
        a frame

        Arguments:
            code {[type]} -- code object 

        Keyword Arguments:
            calla88rgs {dict} -- args  (default: {{}})
            global_names {[type]} -- [description] (default: {None})
            local_names {[type]} -- [description] (default: {None})

        Returns:
            frame[type] -- [description]
        """
        # log.info("make_frame: code=%r, callargs=%s" % (code, callargs))
        if global_names is not None and local_names is None:
            local_names = global_names
        elif self.frames:
            global_names = self.frame.global_names
            local_names = {}
        else:
            global_names = local_names = {
                '__builtins__': __builtins__,
                '__name__': '__main__',
                '__doc__': None,
                '__package__': None,
            }
        local_names.update(callargs)
        frame = frame(code, global_names, local_names, self.frame)
        return frame

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
        while True:
            byteName, arguments, opoffset= self.prase_byte_code_and_argument()
            if log.isEnabledFor(logging.INFO):
                self.log(byteName, arguments)
            self.dispatch(byteName, arguments)
            if (byteName == "RETURN_VALUE"):
                break

    # BYTE CODE 
    def NOP(self):
        pass

    def LOAD_CONST(self, number):
        self.stack.append(number)

    def LOAD_FAST(self, name):
        self.stack.append(self.enviornment.get(name))
    
    def STORE_FAST(self, name):
        val = self.stack.pop()
        self.enviornment[name] = val

    def MAKE_FUNCTION(self, argc):
        name = self.pop()
        code = self.pop()
        defaults = self.popn(argc)
        globs = self.frame.f_globals
        fn = Function(name, code, globs, defaults, None, self)
        self.push(fn)

    def CALL_FUNCTION(self, arg):
        arg = self.popn(arg)
        func = self.pop()
        frame = self.frame
        code = func.func_code
        self.make_frame(code, callarg,frame.global_names, frame.local_names)
        self.run_frame()

    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print(answer)

    def PRINT_NOT_POP(self):
        print(self.stack[-1])

    def BINARY_ADD(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)

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