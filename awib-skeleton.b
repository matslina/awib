[ This is the awib skeleton. The frontend and the backends are to be
  inserted into the code as indicated by the comments.
]

>>>>>>>+
% 7(0) *T 0    (where T = index of target platform)

#include(frontend/frontend.b)

% 7(0) T *0 b (code) 0 M m
% where b = (bytecode OK ? 1 : 0) and Mm = maximum loop depth

// If bytecode is OK then run backend T on bytecode

>[<<[-[-[[-]>>-<<]

>>[->
// T=2: lang_c
% 10(0) *(code) 0 M m

#include(lang_c/backend.b)

% ::: 0 0 *0 0 0
<]<<]

>>[->
// T=1: 386_linux
% 3(0) 7(0) *(bcode) 0 M m

#include(386_linux/backend.b)

% ::: 0 *0 0 :::
<]<<]
]
