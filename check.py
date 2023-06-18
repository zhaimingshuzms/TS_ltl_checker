
from ltl_parser import parsing
from automaton import GNBA, NBA, AP
from TS import load_ts, Product
from AST import ASTNode

if __name__ == "__main__":
    # ret = GNBA(parsing("aU((!a)&b)"))
    ltl_formula = input("Enter ltl formula:")
    parse_result = parsing(ltl_formula)
    negation = ASTNode(parse_result).negation()
    gnba = GNBA(negation)
    nba = gnba.toNBA()
    print("nba intial:",nba.Q0)
    nba.print_edge()
    # print("Q0",nba.Q0)
    # print("AP",nba.AP)
    ts = load_ts()
    # print("----------------------")
    product = Product(ts, nba)
    print("product.I",product.I)
    product.print_edge()
    print("result:",product.nested_dfs())