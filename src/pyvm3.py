import logging
import collections
from .frame import frame

log = logging.getLogger(__name__)
block = collections.namedtuple("Block", "type, handler, stack_height")


class VirtualMachineError():
    """[summary]
    """
    def __init__(self, message:str):
        print(message)


class VirtualMachine:
    """VirtualMachine main program, it should have a call stack, a refrence of 
        current frame. return value, raise exception.
        call stack is a stack of frames.
        current frame is the frame which is running the bytecode.
        code block stack is a stack for helping the process control, it should 
        help the try-catch statements, iterator, generator.
        return value should be the export of the program, last exception should 
        be the last raise exception from frames.        
    """

    def __init__(self):
        self.frames = []   # The call stack of frames.
        self.frame = None  # The current frame.
        self.return_value = None # The python program return value.
        self.last_exception = None # The raise exception.
        self.code_block_stack = [] # The stack of code block.

    def run_code(self, code, global_names=None, local_names=None):
        """the entry of VirtualMachine, this function should make a frame and
        run it, return the return value.

        Args:
            code ([type]): py code obj 
            global_names ([type], optional): global name space. Defaults to None.
            local_names ([type], optional): locak name space. Defaults to None.
        """
        frame = self.make_frame(code, global_names, local_names)
        return self.run_frame(frame)

    """frame operate
    """

    def push_frame(self, frame):
        self.frames.append(frame)
        self.frame = frame

    def pop_frame(self):
        self.frames.pop()
        if self.frames:
            self.frame = self.frames[-1]
        else:
            self.frame = None

    def make_frame(self, code, position_args=[], callargs={}, global_names=None, 
        local_names=None):
        """create a frame when vm is running, when vm invoke a function ,then 
        create a frame

        Arguments:
            code {[type]} -- code object 

        Keyword Arguments:
            callargs {dict} -- args  (default: {{}})
            global_names {[type]} -- global name space(default: {None})
            local_names {[type]} -- local name space(default: {None})

        Returns:
            frame[frame] -- frame obj 
        """
        log.info("make_frame: code=%r, callargs=%s" % (code, callargs))
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

    def run_frame(self, frame):
        status = None
        while True:
            bytecode, arguments = self.prase_byte_code_and_argument()
            dispatch(bytecode, arguments)
        return status

    def prase_byte_code_and_argument(self):
        pass

    def dispatch(self, bytecode, arguments):
        pass

    

