class PyClass:
    """
    Create a class obj, in python interpretator 

    class object should have functions and members in its local_names
     
    """
    def __init__(self, func, name, extend=[]):
        self.name = name
        self.extend = []
        self.local_names = {}
        self.init = func

    def store_attr(self, attr:dict):
        self.local_names.update(attr)

    def get_attr(self, attr):
        retval = self.local_names.get(attr)
        if retval:
            pass
        else:
            for e in self.extend:
                retval = e.get_attr(attr)
                if retval:
                    break
        return retval