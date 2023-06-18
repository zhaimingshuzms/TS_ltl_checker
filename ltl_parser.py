from pyparsing import *

def parsing(ltl_formula:str):
    ltl_formula = ltl_formula.replace('/\\','&')
    ltl_formula = ltl_formula.replace('\\/','|')


    # Define the grammar for LTL formulas
    prop = Group(Word(alphas.lower()))
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
    neg = Group(op_not + expr)
    next = Group(op_next + expr)
    eventually = Group(op_eventually + expr)
    always = Group(op_always + expr)
    # no ambiguity
    atom = prop | (lparen + expr + rparen) | neg | next | eventually | always

    until = Group(atom + op_until + expr)
    release = Group(atom + op_release + expr)
    and_expr = Group(atom + op_and + expr)
    or_expr = Group(atom + op_or + expr)
    implies = Group(atom + op_implies + expr)
    equiv = Group(atom + op_equiv + expr)
    binary_op = until | release | and_expr | or_expr | implies | equiv | atom
    expr << binary_op

    # Parse an LTL formula and build an AST
    # ltl_formula = 'G((p -> Fq) U (q -> FGp))'
    ast = expr.parseString(ltl_formula).as_list()[0]

    # Print the AST
    # print("parse result: ",ast)
    return ast

