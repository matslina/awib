% 22(0) T *(code) 0 M m
% where T = target index and Mm = maximum loop depth

# move T; add header and footer codes
<[-<<<<<<<<<<<<<<<<<+>>>>>>>>>>>>>>>>>]
>[>>]>[-]>[-]<++++++++[-<++++>]<[<<]>++++++++[-<++++>]<-
% T 15(0) *31 0 (code) 32 0

# iterate over the code
[
% T D d 13(0) *P Q (code)   (where Dd (ie add(mul(D 256) d)) is loop depth)
[-<+<+>>]<<<<<<<<<<<<<<
[->>+>>+<<<<]<
[->>+>>+<<<<]<
[->+>+<<]+>

# run language definition according to T with S=P
% 1 *T T D d D d 7(0) P P 0 Q (code)
---[-[<->++++[-]]

<[->>>>>
# T=4: lang_java
% (stuff) *D d 7(0) S (stuff)
#include(java.b)
<<<<<]>]

<[->>>>>
# T=3: lang_dummy
% (stuff) *D d 7(0) S (stuff)
#include(dummy.b)
<<<<<]

>>>>>>>>>>>>>>>>

% 0 0 T D d 10(0) P *0 Q (code)
# if P in {ADD SUB LEFT RIGHT} then output(itoa(Q))
<[->+<<+>]++++>-[<->--[<->--[<->-[<->++++++[-]]]]]<
% 0 0 T D d 9(0) P *c 0 Q (code)   (where c gt 0 iff P in {ADD SUB LEFT RIGHT})

[[-]>>[-<<<<+>>>>]<<<<<<
 # output D=Q in base 10
 % 0 0 0 *0 0 D
 +[->[-]>[<+>-[<+>-[<+>-[<+>-[<+>-[<+>-[<+>-[<+>-[<+>-[<[-]<<<+>>>>-
 [<<+>>[-<<<+>>>]]]]]]]]]]]]<<<[->>>+<<<]>]
 % 0 div(D 10) 0 *0 mod(D 10) 0
 >[-<<<<+>>>>]<<<[
  [->>>>+<<<<]>>
  % mod(D 10) 0 0 *0 0 div(D 10)
  +[->[-]>[<+>-[<+>-[<+>-[<+>-[<+>-[<+>-[<+>-[<+>-[<+>-[<[-]<<<+>>>>-
  [<<+>>[-<<<+>>>]]]]]]]]]]]]<<<[->>>+<<<]>]
  % mod(D 10) div(D 100) 0 *0 mod(div(D 10) 10) 0
  <<[>++++++[-<++++++++>]<.[-]]>>
  ++++++[->++++++++<]>.[-]<<<]
 % mod(D 10) *0 0 0 0 0
 ++++++[-<++++++++>]<.[-]
>>>>>>>
]
% 0 0 T D d 9(0) P *0 0 0 (code)

# if P gt 9 then remove P and move on
# else update depth Dd; set P = add(P 20); process again
>+<<-[-[-[-[-[-[-[-[-[[->+<]>>-<<]>+<]>+<]>+<]>+<]>+<]>+<]>+<]>+<]>+>
% 0 0 T D d 10(0) P *c 0 (code)    (where c == P le 9 ? 1 : 9)
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
% ::: T D d 10(0) Q *0 0 (code)   (where Q == P gt 9 ? P : 0)
<[-]>>>
]
