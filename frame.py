class frame:
    """frame is use to description of the function object in vm runing time,
    it's maintain sth below:
        code object, global names, local names, prev frame, opreands stack,
    builtin_names is the """

    def __init__(self, code_obj, global_names, local_names, prev_frame):
        """frame is a code block of method 

        Arguments:
            code_obj {[type]} -- python byte code object
            global_names {[type]} -- global name space
            local_names {[type]} -- local name space
            prev_frame {[type]} -- [description]
        """
        self.code_obj = code_obj
        self.global_names = global_names
        self.local_names = local_names
        self.prev_frame = prev_frame
        self.stack = []
        if prev_frame:
            self.builtin_names = prev_frame.builtin_names
        else:
            self.builtin_names = local_names['__builtins__']
            if hasattr(self.builtin_names, '__dict__'):
                self.builtin_names = self.builtin_names.__dict__
    
        self.last_instruction = 0
        self.block_stack = []