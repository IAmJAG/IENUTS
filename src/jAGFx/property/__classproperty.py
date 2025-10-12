

def classproperty(func):
    return classmethod(property(func))
