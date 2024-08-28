% (stuff) *D d 7(0) S (stuff)
% where integer S indicates which code block to output
%       16 b integer Dd is loop depth

# indentation if S le 13: 2*add(D*256 d) blank spaces
>>>>>>>+>>
-[-[-[-[-[-[-[-[-[-[-[-[-[<<->>[-<+>]]
<+>]<+>]<+>]<+>]<+>]<+>]<+>]<+>]<+>]<+>]<+>]<+>]<+<
% D d 0 0 0 0 0 *c S 0    (where c == S le 13 ? 1 : 0)
[-<<<<++++[-<++++++++>]<....<[->....<]
<[->++++++++++++++++[->................................
                       ................................<]<]>>[-]>>>>>]
<<<<<<<[-]>[-]>>>>>>
% (stuff) 7(0) *0 S 0 (stuff)

+>-[-[-[-[-[-[-[-[-[-[-[-[-[--------[--[--[-[---[--[--[---[-
[<->++++++++++++++++++++++++++++++++++++++[-]]

<[-
# footer
<<<<<<<+++++++++++++++++++++[->++++>++++
++>++>++>+++++>+++++<<<<<<]>>>----------
....<<-----.>>>>++.<--..+..<<<<+++++++++
+.>>-.<<..>>>>>>---.<+++.<<.>>-.>-----.<
----.+++++.<-.+.<.>++++.++++++++++++++++
+.<.>>-----.++++++.<----..<<<+++.>>>>>++
++.<++++.++.>+++++++.<-.<++.<++++++++.+.
>++.<---------.<--.<<.>>>....>>--.>-----
--.<++.+.---.----.<<.>>++++.+++.-------.
<<++++++++.>>+++++.+.>-.<<----..>>+++++.
<-----.<..>++++.+.>-----.+++++.+++++.<<<
.+.+++.------------.>>-.+.>----------.<<
..>>+++++.<-----.<..>++++.+.>-----.<----
-.++++++.-.<<++++++++.+..>+.<<<<.>>++.<<
.[<]>[[-]>]
]>]

<[-
# header
<<<<<<<+++++++++++++++++++[->++>++>++++>
+++>++++++>+++++<<<<<<]>>>>>+++.--.>++++
++.<<<<------.>>>.+.>-.<<+..>>+++++.<---
--.<..>++++++++++++.--------.>----.+++++
++.------.<<<<<++++++.>.>++++++.>>>-.---
-.+++.<<<<<.>.>+++++.>>-.>+++++.<++.>---
-.<+++++++++.<+.<<<<++++++++++..>>+++.>+
+++.++++++.>>>+++++++..+++.<------.<<<<-
---.>>>>--.>-.<.--.<<++++.-.-----.>>+++.
<<++.>>----.>-----.<<<.+.>>>+++.<<<+++.>
>+.<<<<+.>>--------.<<<.>>.>--.++++++.>>
>..+++.<++++.<<<<-.>>>>--.>-.<.--.<<++++
.-.-----.>>>-.<++.-.<<<<+.>>--.<<<.>>>++
+++++++.>>>+.<<<<---.>>>--.+++.>.<<+.<--
------------------.<<+++.>.>+++++.>++.<<
<----.>>>>>-.<.-.<<<.>>>>----.<<----.<<.
>-----.<<++++.>.>>>>++++.<+.-.<<<.>>>>++
.<<.<<.>+++++.<<---.>.<++++.>>>++++.<<.>
>>>------.<-----.<----..<-----.>>>----.<
++++.++.>+++++++.<-.<++.<<<-----.+.>>>++
.<<<<.>>>>>+++.>----.---.<-----.>.<<<<<<
.>>....>.>----.<<.>.>>>.----.+++.<<<<<++
+.<.>>....>+++++.>.<<.>.>>.>+++++.<++.>-
---.<<<<<.<.>>>>>+++++++.<<<<<.>>....>>>
>+++++++.-------.<-------.<<<.>>>-------
.++++++++.-.<<<.>>>----.<<<.>>+++.<<.<++
+++.+.+++++.++++.<.>>....>>>----.>.<++++
++++.<<<.>>>-------.++++++++.-.<<<.>>>>-
--.<+.>++++.<<<<.>>.<<.>++++.<<---------
--.>>>>.<-----.+++.<<.<.>>>>+++.<<<<+.-.
+.-..>>++.>.<<<<.[[-]>]
]>]

<[-
# post_RMUL2
++++++[->+++++++<]>-..>+++[-<++++++>]<.
+[------<+>]<.[-]
]>]

<[-
# post_LMUL2
++++++[->+++++++<]>-..>+++[-<++++++>]<.
+[------<+>]<.[-]
]>]

<[-
# post_SET
++++++++++[->++++++<]>-.+[------<+>]<.[-]
]>]

<[-
# post_RIGHT
++++++++++[->++++++<]>-.+[------<+>]<.[-]
]>]

<[-
# post_LEFT
++++++++++[->++++++<]>-.+[------<+>]<.[-]
]>]

<[-
# post_SUB
++++++[->+++++++<]>-.>+++[-<++++++>]<.+
[------<+>]<.[-]
]>]

<[-
# post_ADD
++++++[->+++++++<]>-.>+++[-<++++++>]<.+
[------<+>]<.[-]
]>]

<[-
# code_RMUL2
<<<<<<+++++++++++++++++++++++++[->++>+>
++++>+++++>++++<<<<<]>+++++++++.>+++++++
.>--.>--------.>++.<<-------.>-.<++.<.<+
+.>.>+++++.>+.>.<<-------.>-.<++.<++++++
++++++++.>>+++.-----.<++++.>--..>+++.<--
.>--.<<--.++.+++..<------.>--.>+++++++.>
-.<<-------.>-----.<++.<++++++.>>+++++++
.-----.<++++.>--..>+++.<--.>--.<<--.>-.+
+++++++.>+++++.<<<------.<[[-]>]
]>]

<[-
# code_RMUL1
<<<<<<++++++++++++++++++++[->++>+++>++>+
++++>+++++<<<<<]>>>>++++++++.>+.<+++++++
+.<--------.>.<.<+.>.>----.<.<<+++.
[[-]>]
]>]

<[-
# code_LMUL2
<<<<<<+++++++++++++++++++++++++[->++>+>
++++>+++++>++++<<<<<]>+++++++++.>+++++++
.>--.>--------.>++.<<-------.>-.<++.<.<+
+.>.>+++++.>+.>.<<-------.>-.<++.<++++++
++++++++.>>+++.-----.<++++.>--..>+++.<--
.>--.<<--.++.+++..<------.>--.>+++++++.>
-.<<-------.>-----.<++.<++++++.>>+++++++
.-----.<++++.>--..>+++.<--.>--.<<--.>-.+
+++++++.>+++++.<<<------.<
[[-]>]
]>]

<[-
# code_LMUL1
<<<<<<++++++++++++++++++++++[->+++++>++>
+++++>+>+++<<<<<]>--.-------.>>++++++.>+
+++++++++.<.>.>-----.<.<----.>.<<+.<
[[-]>]
]>]

<[-
# code_SET
<<<<<++++++++++++++++++++++++++++++[->++
>+>+++>++++<<<<]>>>++++++++.>---.<++++.-
----------.>-----.<++.<++.<+.>.<[[-]>]
]>]

<[-
# code_CLOSE
++++++++++[->++++++++++++<]>+++++.[-]+++
+++++++.[-]<
]>]

<[-
# code_OPEN
<<<<<+++++++++++++++++++++++++++++++[->+
+++>+++>+>++<<<<]>-----.>+++++++++++.+.+
++.-------.>+.<---.<--.>++++.-----------
.<-----.>++.>.+.>-.<-.>-------------.<.<
<+++++++++++.<++++++++++.[[-]>]
]>]

<[-
# code_RIGHT
<<<<<++++++++++++++++++++++++++++[->+>++
>++++>+<<<<]>>>.>++++.+++++++++++.<<++++
+.<++++.[[-]>]
]>]

<[-
# code_LEFT
<<<<<++++++++++++++++++++++++++++[->++++
>+>++>++<<<<]>.>++++.>-----------.>+++++
.<<.<[[-]>]
]>]

<[-
# code_OUTPUT
<<<<<<+++++++++++++++++++++[->+++>++>+++
++>+++++>++<<<<<]>>>++++++.<++++.>++++++
++.-----.>.<++.>----.>--.--.<---.<+.>+++
+.-----------.<-----.<..>.<---.++++++.>>
++.>+++.<<<<.----.<++++++++++.[[-]>]
]>]

<[-
# code_SUB
<<<<<++++++++++++++++++++++++++++++[->++
>+>+++>++++<<<<]>>>++++++++.>---.<++++.-
----------.>-----.<++.<++.<+.>.>+++++.>+
++++.<++++.-----------.>-----.<++.<+++++
+++++++++.>>+++++++.-----.<++++.>--..---
----.+++++.<++++++.--------.>+++++.++.<+
++.<------.<[[-]>]
]>]

<[-
# code_INPUT
<<<<<<+++++++++++++++++++++[->+++>++>+++
++>+++++>++<<<<<]>>>.<++++.>+++++++++.>-
---.----.+++.>--.--.<<-----.++++++++.-.>
>------.<--.<+.>++++.-----------.<-----.
<..>.<---.++++++.>>++.<<--------.<.----.
<++++++++++.[[-]>]
]>]

<[-
# code_ADD
<<<<<++++++++++++++++++++++++++++++[->++
++>+++>+>++<<<<]>>++++++++.<---.>++++.--
---------.<-----.>++.>++.>+.<.<+++++.<++
+++.>++++.-----------.<-----.>++.>++++++
++++++++.<<+++++++.-----.>++++.<--..----
---.+++++.-------.>--.++.+++..>------.<<
[[-]>]
]<<<<<<<

% (stuff) *0 9(0) (stuff)
