>>>>>>>>>>>>>>>>>>>>++
% 20(0) *T 0    (where T = index of default target platform)

#include(frontend/frontend.b)

% 20(0) T *0 b (code) 0 M m
% where b = (bytecode OK ? 1 : 0) and Mm = maximum loop depth

// If bytecode is OK then run backend T on bytecode

>[<<[-[-[-[-[-[-[-[-[[-]>>-<<]

>>[+++++++
// T=8: lang_java

% 23(0) *T (code) 0 M m

#include(lang_java/backend.b)

% ::: 0 0 *0 0 0
]<<]

                 >>[-<+++++++>]<<]
               >>[-<++++++>]<<]
             >>[-<+++++>]<<]
           >>[-<++++>]<<]
         >>[-<+++>]<<]

% 20(0) *0 t 0 (code) 0 M m   (where t = (T in {3 4 5 6 7} ? T : 0))

>[[->+<]>
% 22(0) *T (code) 0 M m
// T=7: lang_tcl
// T=6: lang_ruby
// T=5: (null)
// T=4: lang_go
// T=3: lang_rust

#include(lang_generic/backend.b)

% ::: 0 0 *0 0 0
]<

>>[+
// T=2: lang_c

% 23(0) *T (code) 0 M m

#include(lang_c/backend.b)

% ::: 0 0 *0 0 0
<]<<]

>>[
// T=1: 386_linux
% 23(0) *T (bcode) 0 M m

#include(386_linux/backend.b)

% ::: 0 0 *0 0 :::
<]<<]
]
