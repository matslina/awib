% 9(0) T *(code) 0 M m
% where T = target index and Mm = maximum loop depth

# move T; add header and footer codes
<[-<<<<<<<<<+>>>>>>>>>]>[>>]>[-]>[-]<++++++++[-<++++>]<<<[<<]>++++++++[-<++++>]<-
% T 7(0) *31 0 (code) 32 0

# iterate over the code
[
% T 7(0) *P Q (code)

# copy P and T
[-<+<+>>]<<[->>+<<]<<<<<<[->+>+<<]>>[-<<+>>]

# run language definition according to T with S=P
% T T *0 0 0 0 0 P *P Q (code)
+<---[-[>-<++++[-]]

>[->>>>>
# T=4: lang_java
% (stuff) 5(0) *S (stuff)
#include(java.b)
<<<<<]<]

>[->>>>>
# T=3: lang_dummy
% (stuff) 5(0) *S (stuff)
#include(dummy.b)
<<<<<]<

# if P in {ADD SUB LEFT RIGHT} then output(itoa(Q))
% T *0 0 0 0 0 0 0 P Q (code)
>>>>>>>[-<+<+>>]++++<-[>-<--[>-<--[>-<-[>-<++++++[-]]]]]>[-<+>]<<[->>+<<]>
% T 0 0 0 0 0 0 *c P Q (code)   (where c gt 0 iff P in {ADD SUB LEFT RIGHT})
[[-]>>[-<<+>>]<<<<
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
>>>>>
% T 0 0 0 0 0 0 *0 P 0 (code)
]

# if P le 9 then remove P and move on; else set P = add(P 20)
>[-<+<+>>]++++++++++++++++++++<<
-[-[-[-[-[-[-[-[-[[-]<+>]]]]]]]]]<
% T 0 0 0 0 *c 0 P 20 0 (code)   (where c == P le 9 ? 1 : 0)
[-<<<<<[->>+<<]>>>>>>>[-]>[-]<]>>[->+<]

>]
