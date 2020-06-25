class pyClass:
    """
    Create a class obj, in python interpretator 

    class object should have functions and members in its local_names
     
    """
    def __init__(self, func, name, extend=[]):
        self.name = name
        self.extend = []
        self.local_names = {}
        self.init = func

    def storeattr(self, attr:dict):
        self.local_names.update(attr)

    def getattr(self, attr):
        retval = self.local_names.get(attr)
        if retval:
            pass
        else:
            for e in self.extend:
                retval = e.getattr(attr)
                if retval:
                    break
        return retval