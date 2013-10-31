awib-0.3
========

About
-----

In summary, awib 0.3 is:

- a brainfuck compiler written in brainfuck
- polyglot in Tcl, C and bash (and brainfuck!)
- optimizing
- capable of compiling to
 - Linux executables (for i386)
 - Tcl
 - Ruby
 - Go
 - C

The bulk of awib is written by Mats Linander <matslina (at) gmail (dot) com>.


Usage
-----

Feed awib brainfuck source code as input and the compiled program
will be written as output.

Awib is a cross-compiler. The supported target platforms are
listed in table 1. By default, the target "lang_c" is chosen.

To specify a target platform, insert a line on the form "@TARGET"
(without the quotation marks and with "TARGET" suitably replaced)
at the very beginning of the source code you wish to compile.
Awib will then produce output accordingly.

-   **386_linux** Linux on i386
-   **lang_c** C programming language
-   **lang_ruby** Ruby programming language
-   **lang_go** Go programming language
-   **lang_tcl** Tcl programming language

For instance, the following input would produce an executable hello
world-program for Linux:

    @386_linux
    ++++++[->++++++++++++<]>.----[--<+++>]<-.+++++++..+++.[--->+<]>-----.--
    -[-<+++>]<.---[--->++++<]>-.+++.------.--------.-[---<+>]<.[--->+<]>-.

The following would produce a hello world-program in Ruby:

    @lang_ruby
    ++++++[->++++++++++++<]>.----[--<+++>]<-.+++++++..+++.[--->+<]>-----.--
    -[-<+++>]<.---[--->++++<]>-.+++.------.--------.-[---<+>]<.[--->+<]>-.

And this would give you the hello world-program in C:

    @lang_c
    ++++++[->++++++++++++<]>.----[--<+++>]<-.+++++++..+++.[--->+<]>-----.--
    -[-<+++>]<.---[--->++++<]>-.+++.------.--------.-[---<+>]<.[--->+<]>-.


Optimizations
-------------

Awib is an optimizing compiler:

-  Sequences of '-','>','<' and '+' are contracted into single
   instructions. E.g. "----" is replaced with a single SUB(4).

-  Mutually cancelling instructions are reduced. E.g. "+++-->><"
   is equivalent to "+>" and is compiled accordingly.

-  Some common constructs are identified and replaced with single
   instructions. E.g. "[-]" is compiled into a single CLEAR-
   instruction.

-  Loops known to never be entered are removed. This is the case
   for loops opened at the very beginning of a program (when all
   cells are 0) and loops opened immediately after the closing
   of another loop.


Requirements
------------

Awib will run smoothly in any brainfuck environment where:

-  Cells are 8-bit or larger

-  The read instruction ',' (comma) issued after end of
   input results in 0 being written OR -1 being written
   OR no change being made to the cell at all.

The vast majority of brainfuck environments meet these criteria.

Since awib is polyglot, it is also possible to compile and/or run awib
directly as C or bash. For instance, using gcc, the following will
build an executable file called awib from awib-0.2.b.

    $ cp awib-0.2.b awib-0.2.c
    $ gcc awib-0.2.c -o awib.tmp
    $ ./awib.tmp < awib-0.2.b > awib-0.2.c
    $ gcc -O2 awib-0.2.c -o awib

Using bash works fine, but is very very very slow:

    $ (echo "@386_linux"; cat awib.b) | bash awib.b > awib
    $ chmod +x awib


Environment
-----------

Code compiled with awib will execute in an environment where:

-  Cells are 8-bit wrapping integers.

-  Issuing the read instruction ',' (comma) after
   end of input results in the current cell being
   left as is  (no-change on EOF).

-  At least 2^16-1 = 65535 cells are available.

-  Operating beyond the available memory, in either
   direction, results in undefined behaviour.


License
-------

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


Mats Linander, 2010-10-03
