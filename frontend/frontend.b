# This is the awib frontend
# Please refer to the documentation in the full source distribution
# of awib for details regarding this file


## Phase 1
## Target identification
##

% *T     (where T = index of target platform)

# read bytes until EOF or bf instruction or '@' is reached
>>>>+[>[-],+
% T 0 0 0 1 *inc(X) 0 0 0  (where X is byte read)
[->+>+<<]>>[-<<+>>]+<
% T 0 0 0 1 inc(X) *inc(X) 1 0
[-[>+++++[-<------->]+<-[-[-[-[--------------[--[-->>+<<[>>-<++
[-<--------->]+<[--[>+++++++++[-<++++++++++>]<[-]]]]]]]]]]]<->]
>[-<<<->>>]<<<]
% T 0 0 0 *0 X 0 0 d
% if( X=='@' ) d=1 else if(EOF) X=0 else X = a bf instruction

# if '@' was encountered then read a string at most 20 bytes long
# whitespace and EOF and bf all terminate the string when read
>>>>[->++++++++++++++++++++<<<<[-]>>>+[
% T 0 0 0 0 (target) 0 0 0 *1 C (where C = sub(20 strlen(target)))
-<,+[-<+<+>>]+<<->
% T 0 0 0 0 (target) X *X 1 0 C
[-[---------[-[---[>++++[-<---->]+<+[-----------[-[-[-[--------------
[--[>++[-<--------->]+<--[--[>+++++++++[-<++++++++++>]<[-]]]]]]]]]]]]]]]
+>[-<->]
% T 0 0 0 0 (target) X c *0 0 C (where c=(X EOF or bf or whitespace ? 0 : 1))
>>[->+<]
<<<[->>>+>->+<[>-]>[>]<[-<<->>]<<<<<]>>>
% T 0 0 0 0 (target) X 0 0 0 *c D
% where c=(string terminated ? 0 : 1) and D=(c==1 ? sub(C 1) : C)
]

# if string was ended due to strlen exceeding limit then read one char extra
+>[<-]<[<]>[-<<<,>>>>]
% T 0 0 0 0 (target) X 0 0 0 *0 D

# now check if the read target string matches any known target string
# and overwrite the target index T accordingly
# we take care not to overwrite the last read X as it may be bf and should
# be passed on to the bytecode compiler below
<<<<+[->+<]>[-<<[<]<<<+>>>>[>]>]++++++++++++++++++++>>>>[-<<<<->>>>]<<<++++
<<<[<]<<<->>>>[>]>>
% T X 0 0 0 (target) 0 s *4 0 0   (where s = strlen(target))
[[->+>+<<]>[-<+>]+>-[-[-[-[<->[-]]

<[-
# build target string for backend index 4
% T X 0 0 0 (target) 0 s 4 *0 0
>>+++++++[->+++++++<]+++++++++>
[->++>++>++>++>++>++>++>++>++<<<<<<<<<]>
++++++++++>->++++++++++++>+++++>--->++++++++>->++++++++++++++++++++>-
<<<<<<<<<<<<
% T X 0 0 0 (target) 0 s 4 *0 0 9 0 "lang_java" 0
]>]

<[-
# build target string for backend index 3
% T X 0 0 0 (target) 0 s 3 *0 0
>>+++++++[->+++++++<]++++++++++>
[->++>++>++>++>++>++>++>++>++>++<<<<<<<<<<]>
++++++++++>->++++++++++++>+++++>--->++>+++++++++++++++++++>+++++++++++>
+++++++++++>+++++++++++++++++++++++<<<<<<<<<<<<<
% T X 0 0 0 (target) 0 s 3 *0 0 10 0 "lang_dummy" 0
]>]

<[-
# build target string for backend index 2
% T X 0 0 0 (target) 0 s 2 *0 0
>>+++++++[->+++++++<]++++++>[->++>++>++>++>++>++<<<<<<]
>++++++++++>->++++++++++++>+++++>--->+<<<<<<<<<
% T X 0 0 0 (target) 0 s 2 *0 0 6 0 "lang_c" 0
]>]

<[-
# build target string for backend index 1
% T X 0 0 0 (target) 0 s 1 *0 0
>>+++++++[->+++++++<]+++++++++>[->+>+>+>++>++>++>++>++>++<<<<<<<<<]
>++>+++++++>+++++>--->++++++++++>+++++++>++++++++++++>+++
++++++++++++++++>++++++++++++++++++++++<<<<<<<<<<<<
% T X 0 0 0 (target) 0 s 1 *0 0 9 0 "386_linux" 0
]
% T X 0 0 0 (target) 0 s i *0 0 S 0 (string) 0
% where S = strlen(string) and i is the backend index of the target (string)

# if (target) equals (string) then set T=i and break else decrease s and retry
<<[->>+>>-<<<<]>>[-<<+>>]>+>[<++++[->++++<]>[-]]<
% T X 0 0 0 (target) 0 s i 0 *e 0 0 (string) 0  (where e=(S==s ? 1 : 0))
[-
<+<<<<[<]>
% T X 0 0 0 *(target) 0 s i 1 0 0 0 (string) 0
[
% T X 0 (target) 0 0 *(F target) 0 s i c 0 (1sled) 0 0 (G string) 0
% where c = (strings equal so far ? 1 : 0 ) and (1sled) is a (initially empty)
% sequence of cells holding 1 and F/G first cells of respective block
[-<+<+>>]<[>>[>]>>>>>[>]>+>[<-]<[<]>[-<<[<]<[-]<<<<[<]<[-]+>>[>]>>>>>[>]>>+<]>-<<<[<]<<<<<[<]<-]
% T X 0 (target F) *0 0 (target) 0 s i c 0 (1sled) 0 0 sub(G F) (string) 0
>>[>]>>>>>[>]>>[[-]<<<[<]<[-]>>[>]>>]<<+[<]<<<<<[<]>
% T X 0 (target F) 0 0 *(target) 0 s i c 0 (1sled) 1 0 0 (string)
]
% T X 0 (target) 0 0 *0 s i c  0 (1sled) 0
<<<[[->>+<<]<]>>>[>]>>>>>[>]<[-<]<
% T X 0 0 0 (target) 0 s i *c  0
# if c==1 then we have a match and write T=i and set i=1
[-<<<<[<]<<<<[-]>>>>>[>]>>[-<<<[<]<<<<+>>>>>[>]>>]+>]>
% T X 0 0 0 (target) 0 s i 0 *0
]

# remove (string) if string lengths didn't match and then sub 1 from i
>>>[>]<[[-]<]<<
<<-]

% T X 0 0 0 (target) 0 s *0 0 0
<[-]<<[[-]<]<<<+[->>>>+<<<<]>>>>->>>
% T 0 0 0 0 X 0 0 *0
]

% T 0 0 0 0 X 0 0 *0
<<<+[->>>>>>>+<<<<<<<]>>>>>>>-
% T 11(0) *X 0 0



## Phase 2
## Bytecode compilation
##

% T 11(0) *X    (where X is user input)
# if read char X is not EOF then enter main loop
+[[-<+>]>+<]>[-<<->>]<<
[
% T 8(0) (code) 0 0 *X (cells left of code ignored for a while hereafter)

# check if X is brainfuck
[->+>+<<]>[-<+>]++++++[->-------<]+>-
[-[-[-[--------------[--[<+++[->-----
--<]+>-[--[<->>+++++++[-<++++++++++++
+>]<++[-]]]]]]]]]<<
% (code) 0 0 *X isbf(X) 0 0

# if bf then add to bytecode
>[-
++++++[-<------->]+<
% (code) 0 0 *sub(X 42) 1 0 0

[-[-[-[-[--------------[--[-----------------------------[

# CLOSING BRACKET
# if this closes OPEN SUB(1) then overwrite with CLEAR
# else append CLOSE
-->-<<<
<<<<[->>>>+>+<<<<<]>>>>>[-<<<<<+>>>>>]<<<[->>>+>+<<<<]>>>>[-<<<<+>>>>]<<<
[->>>+>+<<<<]>>>>[-<<<<+>>>>]+
% (code) P Q R *1 0   (where P0 QR could be OPEN SUB(1))
<-            [+[-]>[-]<]
<---        [+++[-]>>[-]<<]
<-------[+++++++[-]>>>[-]<<<]
++++++++>>>[-<<<[-]<-<---<<++>>>]
% (code) CLOSE/CLEAR 0 *0 0 0
]

# OPENING BRACKET
# if previous op was CLEAR or CLOSE or if this is the first op
# then ignore this loop
>[-
% (code) 0 0 0 *0 0 0
<<+++<+<<[>>>-<-]>>[->>]<<+<<--------[>>>-<-]>>[->>]<<+<<-
[>>>-<-]>>[->>]<<<<+++++++++>>+++++++>[->+<]>
% (code) OPEN *c 0 0 0 (where c = (should this loop be ignored ? 1 : 0))
[>>>>>+<<<<<[
% (code) OPEN *1 0 0 0 L l
>>+<,[>-]>[>]<[-<<->>]+<+[>-]>[>]<[-<<->>]<-
% (code) OPEN c *X 0 0 L l  (where c = (EOF reached ? 0 : 1) and X = byte read)
>+++++++++[-<---------->]+<-[>-]>[>]<[->>
{ 16b inc >>>++++++++[-<++++++++>]<[->++++<]<
          [->+>-<<]>+[-<+>]+>-[<->[-]]<[-<[-]<+>>]<< }
<<]+<--[>-]>[>]<[->>
{ 16b dec >>+<[>-<[->>+<<]]>>[-<<+>>]<<->[-<+
          <->++++++++[->++++++++<]>[-<++++>]<->]<< }
<<]+++++++++[-<++++++++++>]<++++[-]
>>>
{ 16b iszero >>+<[>-]>[>]<<<[[->>>+<<<]>>[-]<<]>>>[-<<<+>>>]<<< }
# if Ll=0 then delete OPEN and set c=0 to break
>>[-<<<<<<[-]<<------->>>>>>]<<<<<<
]]
% (code) *0 0 0 0 L l  (where Ll is nonzero iff EOF occurred prematurely)
>>>>[-]>[-]<<<
% (code) 0 0 *0 0
]<]

# MOVE RIGHT
# if previous op is RIGHT(i) and i is not 127 then overwrite with RIGHT(inc(i))
# else append RIGHT(1)
>[
-<<<<<[->>+>+<<<]>>[-<<+>>]<[->+>>+<<<]>[-<+>]
% (code) *0 P i 0      (where P(i) = previous op)
++++++++[->>----------------<<]>>+
[<<++++++++[->>++++++++++++++++<<]+>>[-]]<------[<[-]>++++++[-]]
<[->>+<<]++++++>+>[-<-<------<+>]>>
]<
% (code) RIGHT(?) 0 *0 0 0
]

# MOVE LEFT
# if previous op is LEFT(i) and i is not 127 then overwrite with LEFT(inc(i))
# else append LEFT(1)
>[
-<<<<<[->>+>+<<<]>>[-<<+>>]<[->+>>+<<<]>[-<+>]
% (code) *0 P i 0      (where P(i) = previous op)
++++++++[->>----------------<<]>>+
[<<++++++++[->>++++++++++++++++<<]+>>[-]]<-----[<[-]>+++++[-]]
<[->>+<<]+++++>+>[-<-<-----<+>]>>
]<
% (code) LEFT(?) 0 *0 0 0
]

# OUTPUT
>[
<<<++++>>>->
]<
% (code) OUTPUT 0 *0 0 0
]

# SUB
#if previous op is SUB(i)
#   if i is 255 then remove previous op
#   else overwrite with SUB(inc(i))
#else append SUB(1)
>[
-<<<<<[->>+>+<<<]>>[-<<+>>]<[->+>>+<<<]>[-<+>]
% (code) *0 P i 0        (where P(i) = previous op)
>---[<+++>+++[-]+>[-]>]>
[<++++++++++++++++[->----------------<]>+>+<
[<<<+>>++++++++++++++++[->++++++++++++++++<]>[-]>-<]
>[-<<<<[-]<--->>>]<]
]<
% (code) SUB(?) 0 *0 0 0
]

# INPUT
>[
<<<++>>>->
]<
% (code) INPUT 0 *0 0 0
]

# ADD
#if previous op is ADD(i)
#   if i is 255 then remove previous op
#   else overwrite with ADD(inc(i))
#else append ADD(1)
>[
-<<<<<[->>+>+<<<]>>[-<<+>>]<[->+>>+<<<]>[-<+>]
% (code) *0 P i 0        (where P(i) = previous op)
>-[<+>+[-]+>[-]>]>
[<++++++++++++++++[->----------------<]>+>+<
[<<<+>>++++++++++++++++[->++++++++++++++++<]>[-]>-<]
>[-<<<<[-]<->>>]<]
]<
% (code) ADD(?) 0 *0 0 0
]

# reduce sequences of ADD SUB  and LEFT RIGHT
<<[[->+<]>>+<<]>[-<+>]<<<[[->>>+<<<]>>>>+<<<<]>>>[-<<<+>>>]+>--[<->++[-]]<
% (code) *c 0 0    (where c = (previous two ops carry arguments ? 1 : 0))
[-<<[->>+>+<<<]>>[-<<+>>]<<<<[->>>>+>+<<<<<]>>>>[-<<<<+>>>>]+>
% (code) 1 *S 0    (where S = sum of previous two ops)
----[-------[<->+++++++++++[-]]]<
% (code) *c 0 0    (where c = (previous ops ADD/SUB or LEFT/RIGHT ? 1 : 0))
[-<-<[-]+<-[>-<[->>+<<]]>>[-<<+>>]<[-<<[-]]]
% (code) *0 0 0
]

>>>]

% 8(0) (code) 0 0 X *0    (where X may be the last byte read)
# read next byte and and break if EOF
<[-]>
,+[[-<+>]>+<]>[-<<->>]<<
]
<<<<[<<]
% 6(0) *0 0 (code)





## Phase 3
## Code verification
##

# move code leftwards and ensure that all OPEN/CLOSE are balanced
# in the process we calculate the maximum loop (ie OPEN/CLOSE) depth
% 6(0) *0 0 (code)
<+<<+>>>>>[
% 0 0 (code) M m D d 0 0 *P p (code) 0 c
% where Pp is first op of right code block
%       Dd holds current loop depth (starting at 1)
%       Mm holds the max loop depth yet encountered
%       c = (unbalanced code ? 1 : 0)
<<<[->>+<<]<[->>+<<]<[->>+<<]<[->>+<<]>>>>>>>[-<<<<<<+>>>>>>]<
[->+<<<<<<<+>>>>>>]+>
% 0 0 (code) P p M m D d 1 *P (code) 0 c
-------[-[<->++++++++[-]]
<[-<<
# P is CLOSE; decrease Dd and leave Mm as it was
  { 16b dec >>+<[>-<[->>+<<]]>>[-<<+>>]<<->[-<+<->++++++
            ++[->++++++++<]>[-<++++>]<->]<< }
>>]>]
<[
# P is OPEN; if Mm==Dd then Mm=Dd=inc(Dd) else Dd=inc(Dd)
% (code) P p M m D d *1 0 (code) 0 c  (note: p=0 since P=OPEN)
<<[-<<->>>>>+<<<]<<[[->>+<<]>>>>-<<<<]
% (code) P p *0 m sub(M D) d e D (code) 0 c  (where e=(M==D ? 1 : 0))
>>>[-<<-<+>>>]<<[[->>+<<]>>>[-]<<<]
% (code) P p d *0 sub(M D) sub(m d) e D (code) 0 c  (where e=(Mm==Dd ? 1 : 0))
>>[-<<+>>]<<<[->+>>+<<<]>>[-<<+>>]>>>[-<<<+<<+>>>>>]<[-<<<<<+>>>>>]<<
% (code) P e M m *D d 0 0 (code) 0 c   (where e = (Mm==Dd ? 1 : 0))
  { 16b inc >>>++++++++[-<++++++++>]<[->++++<]<[->+>-<<]
            >+[-<+>]+>-[<->[-]]<[-<[-]<+>>]<< }
<<<[->[-]>[-]>[-<+<+>>]<[->+<]>>[->+<<<+>>]>[-<+>]<<<<<]>>>>>
]
% 0 0 (code P p) M m D d *0 0 (code) 0 c  (where Dd is properly updated)
<< { 16b iszero [[->>+<<]>>>+<<<]>>[-<<+>>]<[[->+<]>>+<<]>[-<+>]+>[<->[-]]<<< }
>>[-<+>>>[>>]>[-]+<<<[<<]]>>
% 0 0 (code P p) M m D d 0 0 *(code) 0 c  (where c is properly updated)
]
% 0 0 (code) M m D d 0 0 *0 c
<<<<
{ 16b dec >>+<[>-<[->>+<<]]>>[-<<+>>]<<->[-<+<->++++++
          ++[->++++++++<]>[-<++++>]<->]<< }
{ 16b isnonzero >[>>+<]>[<]<<[[->>+<<]>>>+<<<]>>[-<<+>>]>[[-]<+>]<<< }
>>[->>>[-]+<<<]<[-]<[-]<[->+<]<[->+<]>>>>>>>[-<<<<+>>>>]<<<<
<<<<<[<<]>+>[>>]>>>
% 0 1 (code) 0 M m *c 0 0 0

# if c==1 output string "Error: unbalanced brackets!\n"
[-<<<[<<]>->[>>]
+++++++++++[->++++++>++++++++++>+++<<<]>
% (code) 0 *66 110 33
+++.>++++..---.+++.<-----------.>>-.<+++.-------.
------------.-.+++++++++++.-----------.+++++++++++++.
-----------.++.-.>.<--.++++++++++++++++.-----------------.
++.++++++++.------.+++++++++++++++.-.>+.---[--->+<]>.[-]<<[-]<[-]>]
<<<<<[<<]
% T *0 b (code) 0 M m
% where b = (bytecode OK ? 1 : 0) and Mm = maximum loop depth
