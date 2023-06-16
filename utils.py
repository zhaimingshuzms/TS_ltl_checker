def eq(a, b):
    return a == b

def implies(a, b):
    return not a or b

def list_and(A, B):
    return [i for i in A if i in B]

def no_true(A):
    if A == None:
        return None
    return [i for i in A if i!='True']