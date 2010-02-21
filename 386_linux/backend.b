# This is the awib 386 Linux backend
# Please refer to the developer documentation for details


## Phase 1
## Calculating jump offsets
##

% 5(0) *(bcode) 0 M m     (where 16b integer Mm = maximum loop depth of bcode)
# Build stack of depth Mm plus 2
# To allow simple stack traversal no stack frame may hold 0
[>>]>[->>+<<]>[->>+<<]>>>+[-<<
[->>+<<]+>[->>+<<]+>
{ 16b dec >>+<[>-<[->>+<<]]>>[-<<+>>]<<->
  [-<+<->++++++++[->++++++++<]>[-<++++>]<->]<< }
{ 16b isnonzero >[>>+<]>[<]<<[[->>+<<]>>>+<<<]>>[-<<+>>]>[[-]<+>]<<< }
>>]<<
+>+>+>+>+>+>+>+[<]>>->->>->->-<<<<<<<
% 5(0) (bcode) 0 0 *0 1 (stack) 1
% where (stack) = A a B b ::: Z z 1 0 0 0 1 1 1 ::: 1
%       Aa is the bottom element
%       Zz is the top element
%       1 0 0 0 indicates the stack top

# Set the bottom element to the size of the mandatory machine code (i e
# the code for memory allocation and sys_exit(0))
>>+++++[->+++++++++++<]<<<<<<[<<]>>


# Move through the bytecode and calculate jmp offsets for OPEN and CLOSE
# Store offsets in a list in the order that they appear in the bcode

% 0 0 (bcode) 0 0 0 *(bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
% where (jmplist) = 1 A a 1 B b 1 ::: 1 Z z
%       Aa Bb are the first two offsets and Zz is the last
[
% 0 0 (bcode) 0 0 0 *P p (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
[-<+<<+>>>]>[-<<<+>>>]<<
% 0 0 (bcode) P p *P 0 0 (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
>+<-[-[-[-[-[-[-[-[-[[-]>-<]

>[-
# CLEAR
% 0 0 (bcode) P p 0 *0 0 (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
>++<
% 0 0 (bcode) P p 0 *0 2 (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
]<]

>[-
# CLOSE
% 0 0 (bcode) P p 0 *0 0 (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
# Pop the top stack element Dd; add Dd to the new stack top; copy Dd
# up to the jmplist
>>[>>]>>>[[[>]>]>]<<<
% ::: (stack) D d *1 0 0 0 1 :::
-<[->>+>>+<<<<]<[->>+>>+<<<<]>>[-<<+>>]>[-<<+>>]<<<
% ::: (stack) *D d 0 0 D d 1 :::
{ 16 addleft [-<<+>>]>[->+<]>[-<++++++++[-<++++++++>]<[->++++<]<
                   [->+>-<<]>+[-<+>]+>-[<->[-]]<[-<[-]<+>>]>>]<< }
+>>>>>>-<<
% ::: (stack) 1 0 0 0 *D d 0 1 ::: 1 0 0 0 (jmplist) 0 0 0 0 0 0 0
[->>>[>]>>>[>>>]>+<<<<[<<<]<[<]<<]>[->>[>]>>>[>>>]>>+<<<<<[<<<]<[<]<]
<+>+>+[>]>>>[>>>]
>[->>>+<<<]>[->>>+<<<]<<+
% ::: (jmplist) 1 0 0 (jmplist) *1 0 0 0 D d

# Copy Dd into the rightmost blank (0) list element which corresponds to
# the OPEN operation matching this CLOSE
[[<]<]<->>>[>>>]>[-<<<+<[<<<]>+>>[>>>]>]>[-<<<+<<[<<<]>>+>[>>>]>>]
<<<<<[<<<]+[>>>]<[->>+<<]<[->>+<<]
% ::: (jmplist) 1 D d (jmplist) 1 *0 0 D d

# Compute Ff = sub(0xFFFF dec(Dd)) and make Ff the last jmplist element
# Ff is the jmp offset for the CLOSE
++++++++++++++++[-<++++++++++++++++>]<--[->+>+<<]+>>>
{ 16b dec >>+<[>-<[->>+<<]]>>[-<<+>>]<<->[-<+
     <->++++++++[->++++++++<]>[-<++++>]<->]<< }
{ 16b subleft [-<<->>]>[->+<]>[-<<+<[>-<[->>+<<]]>>[-<<+>>]
        <<->[-<+<->++++++++[->++++++++<]>[-<++++>]<->]>>]<< }
% ::: (jmplist) 1 F f *0 0 0 0
<<<[<<<]<[<]<<<[[[<]<]<]<<[<<]
% 0 0 (bcode) P p 0 *0 0 (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
]<]

>[-
# OPEN
% 0 0 (bcode) P p 0 *0 0 (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)

# Add size of OPEN machine code (= 8) to top stack element and then add a new
# stack element holding size of CLOSE machine code (= 8)
>>[>>]>>>[[[>]>]>]<<<->>++++++++[-<<<<
{ 16b inc >>>++++++++[-<++++++++>]<[->++++<]<[->+>-<<]>+
                         [-<+>]+>-[<->[-]]<[-<[-]<+>>]<< }
>>>>]<++++++++>+>>->->[>]>>
% 0 0 (bcode) P p 0 0 0 (bcode) 0 0 0 1 (stack) 1 0 0 *0 (jmplist)

# Append to jmplist an empty element  This element will be filled later on
# when the CLOSE corresponding to this OPEN is encountered
>[>>>]+[<<<]<[[[<]<]<]<[[[<]<]<]<<[<<]
% 0 0 (bcode) P p 0 *0 0 (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
]<]

>[-
# RIGHT
% 0 0 (bcode) P p 0 *0 0 (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
# if p==1 then s=1   (s = size of machine code)
# if p==2 then s=2
#         else s=3
>+++<<+<
-[>-]>[>]<[->>--<<]+<
-[>-]>[>]<[->>-<<]<++>>
% 0 0 (bcode) P p 0 *0 s (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
]<]

>[-
# LEFT
% 0 0 (bcode) P p 0 *0 0 (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
# if p==1 then s=1   (s = size of machine code)
# if p==2 then s=2
#         else s=3
>+++<<+<
-[>-]>[>]<[->>--<<]+<
-[>-]>[>]<[->>-<<]<++>>
% 0 0 (bcode) P p 0 *0 s (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
]<]

>[-
# OUTPUT
% 0 0 (bcode) P p 0 *0 0 (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
>++++<
% 0 0 (bcode) P p 0 *0 4 (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
]<]

>[-
# SUB
% 0 0 (bcode) P p 0 *0 0 (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
# if p==1 then size of machine code s=2 else s=3
>+++<<+<-[>-]>[>]<[->>-<<]<+>>
% 0 0 (bcode) P p 0 *0 s (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
]<]

>[-
# INPUT
% 0 0 (bcode) P p 0 *0 0 (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
>++++++<
% 0 0 (bcode) P p 0 *0 6 (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
]<]

>[-
# ADD
% 0 0 (bcode) P p 0 *0 0 (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
# if p==1 then size of machine code s=2 else s=3
>+++<<+<-[>-]>[>]<[->>-<<]<+>>
% 0 0 (bcode) P p 0 *0 s (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
]<

# Depending on the operation the code above may hafe left a value s
# holding the size of the operation's machine code   If so we
# add s to the top stack element
% 0 0 (bcode) *0 0 s (bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
>>[->[>>]>>>[[[>]>]>]<<<-<<
{ 16b inc >>>++++++++[-<++++++++>]<[->++++<]<[->+>-<<]
                     >+[-<+>]+>-[<->[-]]<[-<[-]<+>>]<< }
>>+[[[<]<]<]<<[<<]>]>
% 0 0 (bcode) 0 0 0 *(bcode) 0 0 0 1 (stack) 1 0 0 0 (jmplist)
]

% 0 0 (bcode) 0 0 0 *0 0 0 1 M m 1 0 0 0 1 ::: 1 0 0 0 (jmplist)
% where Mm is the size of the machine code





## Phase 2
## Output of headers and code
##

# ELF header (hex):
#   7f 45 4c 46 01 01 01 03  00 00 00 00 00 00 00 00
#   02 00 03 00 01 00 00 00  54 80 04 08 34 00 00 00
#   00 00 00 00 00 00 00 00  34 00 20 00 01 00 28 00
#   00 00 00 00
+++++++++[>++++++++++++++<-]>+.+[--<+>]<
+++++.+++++++.------.>+...++.---........
++.--.+++.---.+.-...++++[-<+++>]<++.
[-->+++<]>++.<++++.++++.[-]>--[------->+++<]>--.
<...........>.<.+++++[->----<]>.<.+.-.>++++++++.[-].....

# Program header (hex):
#   01 00 00 00 00 00 00 00  00 80 04 08 00 80 04 08
#        X           X       05 00 00 00 00 10 00 00
# where X = total file size = add(Mm sizeof(headers)) = add(Mm 0x54)
% 0 0 (bcode) 0 0 0 0 *0 0 1 M m 1 0 0 0 1 ::: 1 0 0 0 (jmplist)
>.-........++++++++[-<++++++++++++++++>]<.>++++.++++.[-].<.[-]>++++.++++.[-]
<++++++[->++++++++++++++<]>>>>-<<<[->
{ 16b inc >>>++++++++[-<++++++++>]<[->++++<]<[->+>-<<]
                     >+[-<+>]+>-[<->[-]]<[-<[-]<+>>]<< }
<]>>.<.<..>>.<.<..+++++.[-]....++++++++++++++++.[-]..
>>[-]>>>>+<+<+<+<+<+<+<+<<<
% 0 0 (bcode) 0 0 *0 0 0 1  ::: 1 0 0 0 (jmplist)

# Machine code for memory allocation etc (hex!):
#   b8 c0 00 00 00 31 db b9  ff ff 00 00 ba 03 00 00
#   00 be 22 00 00 00 31 ff  31 ed cd 80 89 c2 97 fc
#   f3 aa 89 d1 89 c3 43 89  da 89 df 47 47 89 fe 46
#   45 45
++++++++++[->++++++++++++++++++++++>+
++++++++++++++++++++++++<<<+++++<++++
++++++++++++++>>]>>+++++<<<<++++.++++
++++.>>...<-.>>-.<<<-------.>>>>..<<.
.<<+.>>+++.---...<<++++.>------------
---.>...<+++++++++++++++.>>>.<<<.>>++
++++++++++++++++.<<<+++++++++++++++.>
>>>-[--<<+>>]<<+.+++++++++.<<--------
---.>+[->>>+++<<<]>>>+.<+++++++++++++
++.---------.>+++++++++++++++++++.<<.
<<+++++++++++++++.>>.<<--------------
.>>+[--<+>]<--.++[->++<]>-.<++++[-<++
+++>]<+++.>>.<<+++++.>>+++[--<+>]<+..
-[->++<]>---.>+++++++++++.<+++[--<+>]
<.-..<[-]>[-]>>[-]>[-]+<+<+<+<<<[<<]>>

% 0 0 *(bcode) 0 1 ::: 1 0 0 0 (jmplist)

# Now move through the bytecode and output the machine code for each operation
# Get jmp offsets from jmplist for OPEN and CLOSE

[
% ::: 0 0 *(bcode) 0 1 ::: 1 0 0 0 (jmplist)
<+>-[-[-[-[-[-[-[-[-[[-]<->]

<[-
# CLEAR: 8839
% ::: 0 *0 0 0 (bcode) 0 1 ::: 1 0 0 0 (jmplist)
+++++++++++[->+++++>++++++++++++<<]>>++++.[-]<++.[-]<
]>]

<[-
# CLOSE: 3A390F85XXYYFFFF  where XXYY = 16 bit jmp offset
% ::: 0 *0 0 0 (bcode) 0 1 ::: 1 0 0 0 1 XX YY (jmplist)
+++++++[->++++++++<]>++.-.

0 *39 0
+++[----<+>]<.
*0f 0 0
[->+++++++++<]>--.
0 *85 0
[-]>>
[>>]>[>]+>+>+>->>.[-]<.[-]
+++++++++++++++++[-<+++++++++++++++>]<..[-]
<[<]<<[<<]<
]>]

<[-
# OPEN: 3A390F84XXYY0000  where XXYY = 16 bit jmp offset
% ::: 0 *0 0 0 (bcode) 0 1 ::: 1 0 0 0 1 XX YY (jmplist)
+++++++[->++++++++<]>++.-.

+++[---->+<]>.
[-<+++++++++>]<---.[-]>>
[>>]>[>]+>+>+>->>.[-]<.[-]..<<[<]<<[<<]<
]>]

<[-
# RIGHT(x)
# 41     if x==1
# 01E9   if x==2
# 83C1x  else
% ::: 0 *0 0 x (bcode) 0 1 ::: 1 0 0 0 (jmplist)
>+>-[-[
<+++++++++[-<+++++++++++++>]<+.>++++++[-<++++++++++>]<++.[-]>>++.[-]]
<[.++++++++++++[->++++++++++++++++++<]>-.[-]<]>]
<[++++[->+++++++++++++<]>.[-]<]<
]>]

<[-
# LEFT(x)
# 49     if x==1
# 29E9   if x==2
# 83E9x  else
% ::: 0 *0 0 x (bcode) 0 1 ::: 1 0 0 0 (jmplist)
>+>-[-[
<+++++++++[-<+++++++++++++>]<+.>++++++++++[-<++++++++++>]<++.[-]>>++.[-]]
<[++++[->++++++++<]>+.+++++[-<+++++>]<+++.[-]]>]
<[+++++++[->+++++++++<]>+.[-]<]<
]>]

<[-
# OUTPUT: 89F0CD80
% ::: 0 *0 0 0 (bcode) 0 1 ::: 1 0 0 0 (jmplist)
++++++++++[->+++++++++++++<]>+++++++.+[------<++++++++++>]<++++++++++.[------>+++++<]>+++++.-----[-----<+++>]<++++++++.[-]
]>]

<[-
# SUB(x): FE09 if x==1 8029x else
% ::: 0 *0 0 x (bcode) 0 1 ::: 1 0 0 0 (jmplist)
>+>-[<-]<[<]++++[-<++++>]<[->++++++++<]+>>
[-<<->-[->++<]>.[-]+++++++++.[-]]<<
[->.++[------------->++++<]>+.[-]>+.[-]<<<]>
]>]

<[-
# INPUT: 89F84BCD8043
% ::: 0 *0 0 0 (bcode) 0 1 ::: 1 0 0 0 (jmplist)
++++++++++[->++++++++++++++<]>---.+++[-----<+++++++++>]<----.++
[---------->+++<]>.+++++++[--<+++++>]<.[-]+++++[->+++++<]>[-<+++++>]
<+++.++++++++[-------->++++<]>-.[-]<
]>]

<[-
# ADD(x): FE01 if x==1 8001x else
% ::: 0 *0 0 x (bcode) 0 1 ::: 1 0 0 0 (jmplist)
>+>-[<-]<[<]++++[-<++++>]<[->++++++++<]+>>
[-<<->-[->++<]>.[-]+.-]<<
[>.[-]<.>>>+.[-]<<<-]>
]>

>>]
% 0 ::: *0 1 ::: 1 0 0 0 (jmplist)

# Output the final sys_exit(0) invocation and then terminate
# 89D84BCD80
<++++++++++[->++++++++++++++<]>---.+++[-------<+++++++++++>]<----.
>++++++++[-<++++>]<++[---------->+++<]>.+++++++[--<+++++>]<.[-]
+++++[->+++++<]>[-<+++++>]<+++.[-]
% ::: 0 *0 0 :::
