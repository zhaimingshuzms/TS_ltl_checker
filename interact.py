from ltl_parser import parsing
from automaton import GNBA, NBA, AP
from TS import load_ts, Product
from AST import ASTNode
from utils import *
import sys

def run(ltl_formula, data_dir, **kwargs):
    parse_result = parsing(ltl_formula)
    negation = ASTNode(parse_result).negation()
    gnba = GNBA(negation)
    nba = gnba.toNBA()
    ts = load_ts(data_dir, **kwargs)
    product = Product(ts, nba)
    print("result:",product.nested_dfs())

def interact_engine():
    ltl_formula = input("Enter ltl formula: ")
    data_dir = input("Enter TS filepath: ")
    run(ltl_formula, data_dir)

def test_engine(**kwargs):
    ltl_path = kwargs['-l']
    ltl_data = load_data(ltl_path)
    data_dir = kwargs['-t']
    n, m = int(ltl_data[0][0]), int(ltl_data[0][1])
    for i in range(n):
        ltl_formula = ''
        for j in ltl_data[i+1]:
            ltl_formula += j
        run(ltl_formula, data_dir)
    for i in range(m):
        initial = [int(ltl_data[i+n+1][0])]
        ltl_formula = ''
        for j in range(1,len(ltl_data[i+n+1])):
            ltl_formula += ltl_data[i+n+1][j]
        run(ltl_formula, data_dir, I=initial)

if __name__ == "__main__":
    kwargs = {'-t':'','-l':'','-i':False}

    for i in range(1,len(sys.argv)):
        if sys.argv[i] == '-i':
            kwargs['-i'] = True
        elif sys.argv[i] in kwargs:
            kwargs[sys.argv[i]] = sys.argv[i+1]

    if kwargs['-i']:
        interact_engine()
    elif kwargs['-t']!='' and kwargs['-l']!='':
        test_engine(**kwargs)
    else:
        print("Wrong arguments.")