from pyparsing import *

def print_tree(node, indent=''):
    if isinstance(node, list):
        for item in node:
            print_tree(item, indent + '  ')
    else:
        print(indent + str(node))

# Define the grammar for LTL formulas
prop = Word(alphas.lower())
op_not = Literal("!")
op_and = Literal("&")
op_or = Literal("|")
op_implies = Literal("->")
op_equiv = Literal("<->")
op_next = Literal("X")
op_eventually = Literal("F")
op_always = Literal("G")
op_until = Literal("U")
op_release = Literal("R")
lparen = Literal("(").suppress()
rparen = Literal(")").suppress()

expr = Forward()
neg = op_not + expr
next = op_next + expr
eventually = op_eventually + expr
always = op_always + expr
# no ambiguity
atom = prop | (lparen + expr + rparen) | neg | next | eventually | always

until = Group(atom + op_until + atom)
release = Group(atom + op_release + atom)
and_expr = Group(atom + op_and + atom)
or_expr = Group(atom + op_or + atom)
implies = Group(atom + op_implies + atom)
equiv = Group(atom + op_equiv + atom)
binary_op = until | release | and_expr | or_expr | implies | equiv | atom
expr << binary_op

# Parse an LTL formula and build an AST
ltl_formula = 'G((p -> Fq) U (q -> FGp))'
ast = expr.parseString(ltl_formula).as_list()

# Print the AST
print(ast)

