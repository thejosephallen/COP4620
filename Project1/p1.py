"""
This program performs the functions of a scanner for a C- compiler.
Author: Joseph Allen
Date: 9/5/18
"""
import sys, re

SYMBOL   = 'Symbol'
KEYWORD  = 'Keyword'
INT      = 'Int'
FLOAT    = 'Float'
ID       = 'ID'
#ERROR    = 'Error'
ERROR    = '\x1b[1;37;41m' + 'ERROR' + '\x1b[0m' # Debug help: Errors appear red
INCOMMENT = 'INCOMMENT'
OUTCOMMENT = 'OUTCOMMENT'

# Token definitions (comment_depth == 0)
token_defs = [
    (re.compile(r'\s+'),                    None),       # matches whitespace
    (re.compile(r'/\*'),                    INCOMMENT),  # start of ml-comment
    (re.compile(r'//[^\n]*'),               None),       # single line comment
    (re.compile(r'<=|>=|==|!='),            SYMBOL),     # double symbols
    (re.compile(r'[,;\-+<>=*/]'),           SYMBOL),     # single symbols
    (re.compile(r'[]()[{}]'),               SYMBOL),     # enclosing symbols

    # match invalid ints
    (re.compile(r'[0-9]+[a-df-zA-DF-Z][.0-9a-zA-Z]*'),  ERROR),

    # match invalid IDs
    (re.compile(r'[a-zA-Z]+[.0-9][.0-9a-zA-Z]*'),       ERROR),

    # match valid IDs
    (re.compile(r'[a-zA-Z]+'),              ID),

    # match valid ints
    (re.compile(r'(?<![\d.])[0-9]+(?![\d.Ee])'), INT),

    # match invalid floats
    (re.compile(r'(?<![a-zA-Z])\d*((\.\d*)?|\.\d+)[eE][-+]?\d*[a-zA-Z\.][a-zA-Z0-9\.]*'), ERROR), # Invalid Scientific
    (re.compile(r'(?<![a-zA-Z])(\d*\.\d*)[a-df-zA-DF-Z\.][a-zA-Z0-9\.]*'), ERROR), # Invalid Float

    # match valid floats
    (re.compile(r'(?<![a-zA-Z])\d*(\.\d+)?([eE][-+]?\d+)'), FLOAT),
    (re.compile(r'(?<![a-zA-Z])(\d*\.\d+)(?![eE])'), FLOAT),
    
    # match invalid character and anything attached until whitespace or symbol
    (re.compile(r'.[^][(){}+\-=<>=*/;,\s]*', re.S),         ERROR)]

# Comment definitions (comment_depth > 0)
comment_defs = [
    (re.compile(r'/\*'),                    INCOMMENT),
    (re.compile(r'\*/'),                    OUTCOMMENT),
    (re.compile(r'.', re.S),                None)]  # ignore noncomments within ml-comment

keywords = set(['else', 'if', 'int', 'float', 'return', 'void', 'while']) # python2.6.6 compatible

if __name__ == '__main__':
    tokens = []
    line_tokens = []
    comment_depth = 0
    with open(sys.argv[1], 'r') as file:
        for line in file:
            line = line.strip()
            print 'INPUT: ' + line
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
                            elif text in keywords: line_tokens.append((KEYWORD, text))
                            else: line_tokens.append((label, text))
                        break
                i = match.end(0)
            for label, text in line_tokens: print label + ': ' + text if label != SYMBOL else text
            tokens.extend(line_tokens)
            del line_tokens[:]