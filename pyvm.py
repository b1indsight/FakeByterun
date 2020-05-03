import frame
from logging import log
import dis
import sys

class VirtualMachineError():
    pass

class Interpreter:

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

    #TODO code obj 格式要类似与what_to_execute， 
    def prase_byte_code_and_argument(self):
        f = self.frame
        byteCode, arg_val = f.code_obj["instructions"][f.last_instruction] 
        #TODO code obj want's to set as a list[turple]
        f.last_instruction += 1
        byte_name = dis.opname[byteCode]
        
        if byteCode >= dis.HAVE_ARGUMENT:
            # index into the bytecode
            if byteCode in dis.hasconst:   # Look up a constant
                arg = f.code_obj["numbers"][arg_val]
            elif byteCode in dis.hasname:  # Look up a name
                arg = f.code_obj["names"][arg_val]
            elif byteCode in dis.haslocal: # Look up a local name
                arg = f.code_obj["localnames"][arg_val]
            elif byteCode in dis.hasjrel:  # Calculate a relative jump
                arg = f.last_instruction + arg_val / 2 
            else:
                arg = arg_val
            argument = [arg]
        else:
            argument = []

        return byte_name, argument

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
            

    def NOP(self):
        pass

    def LOAD_VALUE(self, number):
        self.stack.append(number)

    def LOAD_NAME(self, name):
        self.stack.append(self.enviornment.get(name))
    
    def STORE_NAME(self, name):
        val = self.stack.pop()
        self.enviornment[name] = val

    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print(answer)

    def PRINT_NOT_POP(self):
        print(self.stack[-1])

    def ADD_TWO_VALUES(self):
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
            

    def run_code(self, code, global_names=None, local_names=None):
        """ An entry point to execute code using the virtual machine."""
        frame = self.make_frame(code, global_names=global_names, 
                                local_names=local_names)
        self.run_frame(frame)

    def make_frame(self, code, callargs={}, global_names=None, local_names=None):
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
        pass
            