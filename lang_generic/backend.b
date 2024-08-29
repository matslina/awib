% 22(0) *T (code) 0 M m
% where T = target index and Mm = maximum loop depth


# move T; add header and footer codes
[-<<<<<<<<<<<<<<<<<+>>>>>>>>>>>>>>>>>]
>[>>]>[-]>[-]<++++++[-<++++++>]<+[<<]>++++++[-<++++++>]<
% T 15(0) *36 0 (code) 37 0

# iterate over the code
[
% T D d 13(0) *P Q (code)   (where Dd (ie add(mul(D 256) d)) is loop depth)
[-<+<+>>]<<<<<<<<<<<<<<
[->>+>>+<<<<]<
[->>+>>+<<<<]<
[->+>+<<]+>

# run language definition according to T with S=P
% 1 *T T D d D d 7(0) P P 0 Q (code)

---[-[-[-[-[<->++++[-]]

<[->>>>>
# T=7: lang_tcl
% (stuff) *D d 7(0) S (stuff)
#include(tcl.b)
<<<<<]>]

<[->>>>>
# T=6: lang_ruby
% (stuff) *D d 7(0) S (stuff)
#include(ruby.b)
<<<<<]>]

<[-
# T=5: (null)
# A Python backend lived here once upon a time
]>]

<[->>>>>
# T=4: lang_go
% (stuff) *D d 7(0) S (stuff)
#include(go.b)
<<<<<]>]

<[->>>>>
# T=3: lang_rust
% (stuff) *D d 7(0) S (stuff)
#include(rust.b)

<<<<<]

>>>>>>>>>>>>>>>>

% 0 0 T D d 10(0) P *0 Q (code)
# if P in {ADD SUB LEFT RIGHT SET LMUL1 LMUL2 RMUL1 RMUL2} then output(itoa(Q))
<[->+<<+>]+++++++++>
-[<->--[<->--[<->-[<->---[<->-[<->-[<->-[<->-[<->+++++++++++++[-]]]]]]]]]]<
% 0 0 T D d 9(0) P *c 0 Q (code)   (where c gt 0 iff P in that set)

[[-]<[-<<<+>>>]>>>
 # itoa
 % 5(0) *n
 <<++++++++++>>[-<<-<+>[<-]<[<]>[->++++++++++>+<<]>>>]++++++++++<<[->>-<<]
 <++++++++++>>[-<<-<+>[<-]<[<]>[->++++++++++>+<<]>>>]++++++++++<<[->>-<<]
 <++++++[->++++++++<]>>[<[->+>+<<]>.[-]>.[-]<]
 >[<<[->>+<<]>>.[-]]<<[-]>>++++++[->++++++++<]>.[-]
 % 5(0) *0
 <<<<<<[->>>+<<<]>>>>
]
% 0 0 T D d 9(0) P *0 0 0 (code)

# if P gt 13 then remove P and move on
# else update depth Dd; set P = add(P 20); process again
>+<<-[-[-[-[-[-[-[-[-[-[-[-[-[
[->+<]>>-<<]>+<]>+<]>+<]>+<]>+<]>+<]>+<]>+<]>+<]>+<]>+<]>+<]>+>
% 0 0 T D d 10(0) P *c 0 (code)    (where c == P le 13 ? 1 : 0)
[
# copy and add 20 to P
+++++++++++++++++++<[->+<<<<<<<<<+>>>>>>>>]<<<<<<<<<
% 0 0 T D d 0 *0 P 8(0) add(P 20) 0 (code)
# if P is OPEN: inc Dd
# if P is CLOSE: dec Dd
+>-------[-[<->++++++++[-]]
<[-<<<
{ 16b dec >>+<[>-<[->>+<<]]>>[-<<+>>]<<->[-<+
          <->++++++++[->++++++++<]>[-<++++>]<->]<< }
>>>]>]
<[-<<<
{ 16b inc >>>++++++++[-<++++++++>]<[->++++<]<
          [->+>-<<]>+[-<+>]+>-[<->[-]]<[-<[-]<+>>]<< }
>>>]
% 0 0 T D d 0 *0 0 8(0) add(P 20) 0 (code)   (with Dd updated)
# move back T D d
<<<<[-<<+>>]>[-<<+>>]>[-<<+>>]>>>>>>>>>>
% T D d 11(0) *0 0 add(P 20) 0 (code)
]
% ::: T D d 10(0) Q *0 0 (code)   (where Q == P gt 13 ? P : 0)
<[-]>>>
]
