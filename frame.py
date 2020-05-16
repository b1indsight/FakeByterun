class frame:
    """frame is use to description of the function object in vm runing time,
    it's maintain sth below:
        code object, global names, local names, prev frame, opreands stack,
    f_builtins is the """

    def __init__(self, code_obj, global_names, local_names, prev_frame):
        """frame is a code block of method 

        Arguments:
            code_obj {[type]} -- python byte code object
            global_names {[type]} -- global name space
            local_names {[type]} -- local name space
            prev_frame {[type]} -- [description]
        """
        self.f_code = code_obj
        self.f_globals = global_names
        self.f_locals = local_names
        self.f_back = prev_frame
        self.stack = []
        if f_back:
            self.f_builtins = f_back.f_builtins
        else:
            self.f_builtins = local_names['__builtins__']
            if hasattr(self.f_builtins, '__dict__'):
                self.f_builtins = self.f_builtins.__dict__
    
        #PC
        self.last_instruction = 0
        self.block_stack = []