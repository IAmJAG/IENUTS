from inspect import currentframe


def getMethodName():
    return currentframe().f_back.f_code.co_name
