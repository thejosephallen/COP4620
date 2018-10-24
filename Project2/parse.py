"""
This function uses LL(1) parsing techniques to determine whether an input program
is acceptable w.r.t a given grammar.
Input: see params
Output: ACCEPT or REJECT
"""
def parse(tokens, grammar, first_sets, follow_sets, terminals, nonterminals, start):
    epsilon = "@"
    stack = ['$', start]
    current, token = [x.pop() for x in [stack, tokens]]
    while current != '$' or token != '$':
        while current == token: current, token = [ x.pop() for x in [stack, tokens]]
        if current not in nonterminals: return False # REJECT - unexpected token
        next_rule = True # flag for breaking the rule loop
        for rule in grammar[current]: # find the rule that generates current token
            if next_rule:
                for production in rule: 
                    if production in nonterminals:
                        if token in first_sets[production]:
                            current = production
                            if len(rule) > 1: stack.extend(reversed(rule[1:]))
                            next_rule = False
                        elif epsilon in first_sets[production]: continue # try next production
                        else: # try next rule, REJECT if no more to try
                            if rule == grammar[current][-1]: return False
                    elif production == epsilon:
                        if token in follow_sets[current]:
                            current = stack.pop()
                            next_rule = False
                        else: return False # REJECT - token not in follows of current
                    elif production in terminals:
                        if token == production:
                            current = production
                            if len(rule) > 1: stack.extend(reversed(rule[1:]))
                            next_rule = False
                        else: # try next rule, REJECT if no more to try
                            if rule == grammar[current][-1]: return False
                    else: return False # REJECT - shouldn't reach here
                    break # break production loop
    return True if current == token == '$' else False