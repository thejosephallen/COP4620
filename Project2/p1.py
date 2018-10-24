"""
This program performs the functions of a scanner for a C- compiler.
Modified for use by parser.
Author: Joseph Allen
Date: 9/5/18
"""
from re import compile, match, S

SYMBOL   = 'Symbol'
KEYWORD  = 'Keyword'
#INT      = 'Int'
#FLOAT    = 'Float'
NUM      = 'NUM'
ID       = 'ID'
ERROR    = 'Error'
#ERROR    = '\x1b[1;37;41m' + 'ERROR' + '\x1b[0m' # Debug help: Errors appear red
INCOMMENT = 'INCOMMENT'
OUTCOMMENT = 'OUTCOMMENT'

# Token definitions (comment_depth == 0) TODO simplify & optimize regexs
token_defs = [
    (compile(r'\s+'),                    None),       # matches whitespace
    (compile(r'/\*'),                    INCOMMENT),  # start of ml-comment
    (compile(r'//[^\n]*'),               None),       # single line comment
    (compile(r'<=|>=|==|!='),            SYMBOL),     # double symbols
    (compile(r'[,;\-+<>=*/]'),           SYMBOL),     # single symbols
    (compile(r'[]()[{}]'),               SYMBOL),     # enclosing symbols

    # match invalid ints
    (compile(r'[0-9]+[a-df-zA-DF-Z][.0-9a-zA-Z]*'),  ERROR),

    # match invalid IDs
    (compile(r'[a-zA-Z]+[.0-9][.0-9a-zA-Z]*'),       ERROR),

    # match valid IDs
    (compile(r'[a-zA-Z]+'),              ID),

    # match valid ints
    (compile(r'(?<![\d.])[0-9]+(?![\d.Ee])'), NUM),

    # match invalid floats
    (compile(r'(?<![a-zA-Z])\d*((\.\d*)?|\.\d+)[eE][-+]?\d*[a-zA-Z\.][a-zA-Z0-9\.]*'), ERROR), # Invalid Scientific
    (compile(r'(?<![a-zA-Z])(\d*\.\d*)[a-df-zA-DF-Z\.][a-zA-Z0-9\.]*'), ERROR), # Invalid Float

    # match valid floats
    (compile(r'(?<![a-zA-Z])\d*(\.\d+)?([eE][-+]?\d+)'), NUM),
    (compile(r'(?<![a-zA-Z])(\d*\.\d+)(?![eE])'), NUM),
    
    # match invalid character and anything attached until whitespace or symbol
    (compile(r'.[^][(){}+\-=<>=*/;,\s]*', S),         ERROR)]

# Comment definitions (comment_depth > 0)
comment_defs = [
    (compile(r'/\*'),                    INCOMMENT),
    (compile(r'\*/'),                    OUTCOMMENT),
    (compile(r'.', S),                None)]  # ignore noncomments within ml-comment

keywords = set(['else', 'if', 'int', 'float', 'return', 'void', 'while']) # python2.6.6 compatible


def p1(filename):
    tokens = []
    line_tokens = []
    comment_depth = 0
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            #print 'INPUT: ' + line
            i = 0
            while i < len(line):
                match = None
                defs = token_defs if comment_depth == 0 else comment_defs
                for definition in defs:
                    regex, label = definition
                    match = regex.match(line, i)
                    if match:
                        text = match.group(0)
                        if label:
                            if label == INCOMMENT: comment_depth += 1
                            elif label == OUTCOMMENT: comment_depth -= 1
                            else: line_tokens.append(text if text in keywords or label == SYMBOL else label)
                        break
                i = match.end(0)
            #for token in line_tokens: print token
            tokens.extend(line_tokens)
            del line_tokens[:]
    tokens.append('$') # prep as stack for parsing
    tokens.reverse()
    return tokens