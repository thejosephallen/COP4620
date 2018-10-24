from sys import exit
from re import findall

"""
This function reads a file containing a formatted grammar and loads it into a dict.
Input:       S -> a S c | b | @   
Output:      grammar[S] = [['a','S','c'],['b'],['@']]  
"""
def load_grammar(filename):
    grammar = {}
    terminals = []    
    try:
        with open(filename, 'r') as gf:
            for i, line in enumerate(gf):
                line = line.split('->')
                if i == 0: start = line[0].strip()
                grammar[line[0].strip()] = [findall(r'\S+', rule) for rule in line[1].split('|')]
    except:
        print "Error loading grammar."
        exit()

    nonterminals = grammar.keys()
    
    for ruleset in grammar.values():
        for rule in ruleset:
            for element in rule:
                if element not in nonterminals and element not in terminals:
                    terminals.append(element)
    
    return grammar, terminals, nonterminals, start

"""
This function reads a file containing formatted first sets and loads them into a dict.
"""
def load_firsts(filename):
    first_sets = {}
    try:
        with open("first_sets", 'r') as fs:
            for line in fs:
                line = line.split('*{')
                first_sets[line[0].strip()] = line[1].strip().split()
    except:
        print "Error loading first sets."
        exit()
    return first_sets

"""
This function finds the follow sets of a grammar.
Input: grammar dict, terminals & nonterminals sets/lists, first sets dict, and 
the start production of grammar.
Output: follow sets dict.
"""
def find_follows(grammar, nonterminals, terminals, first_sets, start):
    follow_sets = {}
    epsilon = "@"
    for nt in nonterminals: follow_sets[nt] = set()
    follow_sets[start].add('$')
    changes = True
    while (changes):
        changes = False
        for nt in nonterminals:
            for rule in grammar[nt]:
                # add direct follows
                for i, production in enumerate(rule): # iterate through t & nt in rule
                    if production in nonterminals:
                        for y, prod_after_i in enumerate(rule[i+1:]):
                            # if terminal, add to follows, then break
                            if prod_after_i in terminals:
                                if prod_after_i not in follow_sets[production]:
                                    follow_sets[production].add(prod_after_i)
                                    changes = True
                                break
                            # add {firsts} - {epsilon} if it can go away, then continue 
                            if first_sets[prod_after_i][-1] == epsilon:
                                for j in first_sets[prod_after_i][:-1]:
                                    if j not in follow_sets[production]:
                                        follow_sets[production].add(j)
                                        changes = True
                            # if next production cant go away, just add its firsts, then break
                            else:
                                for l in first_sets[prod_after_i]:
                                    if l not in follow_sets[production]:
                                        follow_sets[production].add(l)
                                        changes = True
                                break
                # add indirect follows
                for x in reversed(rule):
                    if x in nonterminals:
                        for w in follow_sets[nt]:
                            if w not in follow_sets[x]:
                                follow_sets[x].add(w)
                                changes = True
                        if first_sets[x][-1] == epsilon: continue
                        else: break
                    else: break
    #for key, item in follow_sets.items(): print "KEY: {:25} -> {}".format(str(key), str(item))
    return follow_sets
