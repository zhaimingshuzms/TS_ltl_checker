def eq(a, b):
    return a == b

def implies(a, b):
    return not a or b

def list_and(A, B):
    return [i for i in A if i in B]

def seteq(A, B):
    if A == None or B == None:
        return False
    return set(A) == set(B)

def no_true(A):
    if A == None:
        return None
    return [i for i in A if i!='True']

def load_data(data_path):
    raw_data = None
    try:
        with open(data_path,"r") as f:
            raw_data = f.readlines()
    except:
        print("Please enter correct filepath.")
        exit(0)
    
    data = []
    for s in raw_data:
        data.append(s.strip().split(' '))
    
    return data