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

INT_C = \
    [r"#include<stdio.h>",
     r"#define _K_(___,_K,__)(K[_KK]^(___))?_K_^_K_:_K _K_ __;",
     r"int  _K_,_KK,__K,____,__[4>>002<<020]; void _(int __){__K=____?__K:__;",
     r"____=__;while(__K)<%__K+=*(__*__*__+_KK+K)-0133?22^_KK<:K+__:>^'K'?'.'",
     r"^'u'^'[':-(__<:_KK+K:>&1):__*__;_KK+=__;_(__);%>}void ___()<% while(K[",
     r"++_KK:>){_K_('v'^']',__<:,:>++)_K_(055|___==___,__[,:>--)_K_('K'^'u',,",
     r"++)_K_('w'^'K',--,)_K_('_'^4,__<:,:>?_(_KK<:K]&1>>1):_(_KK<:K:>&1))_K_",
     r"('v'^'+',__[,]?_((_KK<:K]&2)-(_KK<:K]&1)):_(0))K<:_KK]-46?_(__<:_K_:>&",
     r"1>>1):putchar(__<:_K_:>);if(_KK<:K:>^(01<<01^'.'))_(0);else<%__<:_K_]=",
     r"getchar();%>%>%>int main(){--_KK;___();}"]

INT_BASH = \
    [r'O0=($(echo "$K"|sed -e"s/\(.\)/\\1 /g"));OO=($(for((i=0;i<65535;i++))',
     r'do echo "0";done));Oo=0;oo="";oO=0;o0=0;while [ $oO -lt ${#O0[@]} ];do',
     r'case ${O0[$oO]} in ">")o0=$((o0+1));;"<")o0=$((o0-1));;"+")OO[$o0]=$((',
     r'(${OO[$o0]}+1)%0x100));;"-")OO[$o0]=$(((${OO[$o0]}+0377)%0x100));;".")',
     r'echo -ne "\0$(((${OO[$o0]}/64)%8))""$(((${OO[o0]}/8)%8))$((${OO[o0]}%8',
     r'))";;",")if ((${#oo}==0)); then oo=$(cat);fi;if ((${#oo}>0)); then OO[',
     '$o0]=$(printf "%d" "\'${oo:0:1}");oo=${oo:1};fi;;"[")if ((${OO[$o0]}==0',
     r'));then c=1;while (($c>0));do oO=$(($oO+1));if [  ${O0[$oO]} == \[ ] ;',
     r'then c=$((c+1));fi;if [ ${O0[$oO]} == \] ]; then ((c-- ));fi;done;else',
     r'O0O[$Oo]=$oO;((Oo++)); fi;;"]")((Oo--));if ((${OO[$o0]})); then oO=$((',
     r'${O0O[$Oo]}-1));fi;;esac;((oO++));done;']

INT_TCL = \
    [r"fconfigure stdout -encoding binary;fconfigure stdin -encoding binary;set __ 0",
     r"set _ 0;set _1 {0};;for {set ___ 0} {$___<0xffff} {incr ___} {lappend _1 0}",
     "lappend _1_ 0;;while {$_ < [string length $K]} {switch -exact -- \\",
     r"[string index $K $_] {{>} {incr __} {<} {set __ [expr $__-1]} {,}",
     "{set __1 [read stdin 1]; if {[string length $__1]==1} {lset _1 $__ [scan $__1 \\",
     r"%c]}} {.} {puts -nonewline stdout [format %c [lindex $_1 $__]]}	{[} {",
     r"if {[lindex $_1 $__] == 0} {set ___ 1; while {$___ != 0} {incr _;",
     "set __1 [string index $K $_];if {[string equal $__1 {[} ]} {incr ___;} \\",
     r"elseif {[string equal $__1 {]}]} {set ___ [expr $___-1]}}} else {",
     r"lappend _1_ [expr $_ - 1]}} {]} {if {[lindex $_1 $__] != 0} {",
     r"set _ [lindex $_1_ end]};set _1_ [lrange $_1_ 0 end-1]} {+} {",
     "lset _1 $__ [expr ([lindex $_1 $__] + 1)%256]} {-} {lset _1 $__ [expr \\",
     r"([lindex $_1 $__] - 1)%256]} default {}}; incr _}"]

POLYGLOT = """#define EOF char* /* !\\
cat >>/dev/null <<EOF
set K {
[]*/
EOF
K="\\
%(code)s";

#if 0 /*[
%(bash_interpreter)s
cat >>/dev/null <<EoF
*/
#else
%(c_interpreter)s
#endif
#define EoF
#if 0
]}
#[
%(tcl_interpreter)s
exit
]
#endif
EoF
"""

def attach_interpreters(code):
    data = {'code': ' \\\n'.join(code),
            'bash_interpreter': '\n'.join(INT_BASH),
            'tcl_interpreter': '\n'.join(INT_TCL),
            'c_interpreter': '\n'.join(INT_C)}

    return [POLYGLOT % data]

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
        return [code[j:j+width] for j in range(0, len(code), width)]

    out, line, code = list(), list(), list(code)
    for f in open(formatfile).read():
        if f == ' ':
            line.append(' ')
        elif f == '\n':
            out.append(''.join(line))
            line = []
        else:
            line.append(code.pop(0))
            if not code:
                break
    if line:
        out.append(''.join(line))

    return out + [''.join(code[j:j+width]) for j in range(0,len(code),width)]

def main():
    parser = optparse.OptionParser(usage="%prog [options] FILE")
    parser.add_option("-t", "--format",
                      dest="format", metavar="F", default=None,
                      help="write output according to format in file F")
    parser.add_option("-w", "--width",
                      dest="width", type="int", metavar="W",default=78,
                      help="write output using line width W (default 78)")
    parser.add_option('', '--interpreter',
                      dest="interpreter", action='store_true',default=False,
                      help="attach C, bash and Tcl interpreters")
    (options, args) = parser.parse_args()

    filename = None
    if len(args) > 0 and args[0] != '-':
        filename = os.path.abspath(args[0])

    code = preprocess(filename)
    code = format(code, options.width, options.format)
    if options.interpreter:
        code = attach_interpreters(code)
    sys.stdout.write('\n'.join(code))
    sys.stdout.write('\n')

    return 0

if __name__ == "__main__":
    sys.exit(main())
