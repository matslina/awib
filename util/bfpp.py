#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Simple brainfuck preprocessor.

The preprocessor performs comment removal and pretty-printing of brainfuck
source code. It also implements an include statement for building programs
from multiple source files.

By default, pretty-printing consists printing the preprocessed code with a
78-character line width. Optionally, a format file describing a more
elaborate formatting of the stripped code can be specified. If so, the
content of the format file is printed with the i:th non-whitespace character
replaced with the i:th brainfuck instruction from the stripped source code.

The include statement is expected to appear alone on a single line and
be on the form

 #include(FILENAME)

where FILENAME is the path of the file to include. The path must be absolute
or relative to the file holding the include statement.

2008-03-23
Mats Linander
"""

import sys
import re
import optparse
import os

include_re = re.compile(r'\s*#include\(([^)]+)\)')
BFIS = set([',','.','-','+','[',']','<','>'])

def preprocess(filename):
    """Preprocesses brainfuck sourcecode.

    Comments are stripped and files are included.
    """

    if filename:
        file = open(filename,"r")
        directory = os.path.split(filename)[0]
    else:
        file = sys.stdin
        directory = os.getcwd()

    data = []
    for line in file:
        m = include_re.match(line)
        if m:
            line = preprocess(os.path.join(directory, m.group(1)))
        data.append(''.join(c for c in line if c in BFIS))
    return ''.join(data)

def format(code, width=78, formatfile=None):
    """Formats preprocessed code for pretty-printing."""

    if formatfile is None:
        return [code[j:j+width] for j in xrange(0, len(code), width)]

    out, line, code = list(), list(), list(code)
    for f in open(formatfile).read()[:len(code)]:
        if f == ' ':
            line.append(' ')
        elif f == '\n':
            out.append(''.join(line))
            line = []
        else:
            line.append(code.pop(0))
    if line:
        out.append(''.join(line))

    return out + [''.join(code[j:j+width]) for j in xrange(0,len(code),width)]

def attach_interpreter(code):
    CFOOTER = ("/*[*/#define _$_(___,_$,__)(K[_$$]^(___))?_"
               "$_^_$_:_$ _$_ __;\n_$_,_$$,__$,____,__[4>>0"
               "02<<020];_(__){__$=____?__$:__;____=__;whil"
               "e(__$){__$+=*(__*__*__+_$$+K)-0133?22^_$$[K"
               "+__]^'K'?'.'^'u'^'[':-(__[_$$+K]&1):__*__;_"
               "$$+=__;_(__);}}___(){while(K[++_$$]){    _$"
               "_('v'^']',__[,]++)_$_(055|___==___,__[,]--)"
               "_$_('K'^'u',,++)_$_('w'^'K',--,)_$_('_'^4,_"
               "_[,]?_(_$$[K]&1>>1):_(_$$[K]&1))_$_('v'^'+'"
               ",__[,]?_((_$$[K]&2)-(_$$[K]&1)):_(0))K[_$$]"
               "-46?_(__[_$_]&1>>1):putchar(__[_$_]);if(_$$"
               "[K]^(1<<1^'.'))_(0);else{__[_$_]=getchar();"
               "}}}main(){--_$$;___();}/*]*/")
    return ['char K[]="\\'] + [line + ' \\' for line in code] + ['";', CFOOTER]

def main():
    parser = optparse.OptionParser(usage="%prog [options] FILE")
    parser.add_option("-t", "--format",
                      dest="format", metavar="F", default=None,
                      help="write output according to format in file F")
    parser.add_option("-w", "--width",
                      dest="width", type="int", metavar="W",default=78,
                      help="write output using line width W (default 78)")
    parser.add_option('-c', '--interpreter',
                      dest="interpreter", action='store_true',default=False,
                      help="attach C interpreter")
    (options, args) = parser.parse_args()

    filename = None
    if len(args) > 0 and args[0] != '-':
        filename = os.path.abspath(args[0])

    code = preprocess(filename)
    code = format(code, options.width, options.format)
    if options.interpreter:
        code = attach_interpreter(code)
    sys.stdout.write('\n'.join(code))
    sys.stdout.write('\n')

    return 0

if __name__ == "__main__":
    sys.exit(main())
