from pyltl import parse

ltl_formula = 'G((p -> Fq) & (q -> FGp))'

# Parse the LTL formula and build an AST
ast = parse(ltl_formula)

# Print the AST
print(ast)