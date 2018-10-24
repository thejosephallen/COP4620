"""
This program, p2.py, performs the functions of an LL(1) parser. It uses
a scanner, p1.py, to gather tokens, loads a grammar, loads first sets,
computes follow sets, and returns the result of a parse
with this context.

By: Joseph Allen
Date: 10/19/18
"""
from p1 import p1 as scan
from tools import load_firsts, load_grammar, find_follows
from parse import parse
from sys import argv

if __name__ == "__main__":

    # use P1 scanner to scan source file for tokens and get the token stack
    tokens = scan(argv[1])

    # load grammar and some useful sets
    grammar, terminals, nonterminals, start = load_grammar("grammar")

    # load first sets
    first_sets = load_firsts("first_sets")

    # find the follow sets using what we have
    follow_sets = find_follows(grammar, nonterminals, terminals, first_sets, start)

    # finally, parse the tokens
    accept = parse(tokens, grammar, first_sets, follow_sets, terminals, nonterminals, start)

    # result of parse
    print "ACCEPT" if accept else "REJECT" 
