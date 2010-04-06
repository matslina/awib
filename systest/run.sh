#!/bin/bash

set -e

ALL_TARGETS="lang_c 386_linux lang_ruby lang_go"
ALL_TEST_CASES=$(ls -1 *.b | cut -f1 -d.|xargs)
AWIB_BUILD="../awib.b"
ALL_METHODS="bfint gcc bash"

BFINT_DIR="../util"
BUILD_DIR=".build"
CELL_SIZES="8 16 32 64"
EOF_BEHAVIOURS="0 1 2"

# parse cmd line args and figure out what to do
targets=""
cell_sizes=""
test_cases=""
methods=""
awib_build=""
while getopts "ht:c:s:b:m:" opt; do

    case $opt in

	h)
	    echo >&2 -e "Usage: $0 [options]"
	    echo >&2 -e "\t-h\tprint this message"
	    echo >&2 -e "\t-t T\ttest for compile target T ($ALL_TARGETS)"
	    echo >&2 -e "\t-c C\trun test case C ($ALL_TEST_CASES)"
	    echo >&2 -e "\t-a A\tuse awib build A ($AWIB_BUILD)"
	    echo >&2 -e "\t-m M\tuse method M to run awib ($ALL_METHODS)"
	    exit 0
	    ;;

	t)
	    if ! echo "$ALL_TARGETS" | grep "$OPTARG" > /dev/null; then
		echo >&2 "unknown target $OPTARG"
		exit 1
	    fi
	    targets="$targets $OPTARG"
	    ;;

	c)
	    if ! echo "$ALL_TEST_CASES" | grep "$OPTARG" >/dev/null; then
		echo >&2 "unknown test case $OPTARG"
		exit 1
	    fi
	    test_cases="$test_cases $OPTARG"
	    ;;

	m)
	    if ! echo "$ALL_METHODS" | grep "$OPTARG" >/dev/null; then
		echo >&2 "unknown method $OPTARG"
		exit 1
	    fi
	    methods="$methods $OPTARG"
	    ;;

	b)
	    awib_build="$OPTARG"
	    ;;

    esac
done
test -z "$targets" && targets="$ALL_TARGETS"
test -z "$test_cases" && test_cases="$ALL_TEST_CASES"
test -z "$methods" && methods="$ALL_METHODS"
test -z "$awib_build" && awib_build="$AWIB_BUILD"

# sanity check
for test_case in $test_cases; do
    if ! [ -f ${test_case}.b ]; then
	echo >&2 "no such test case: $test_case"
	exit 1
    fi
done
if ! [ -f $awib_build ]; then
    echo >&2 "no such file: $awib_build"
fi
if echo "$methods" | grep "bfint" >/dev/null; then
    for cell_size in $cell_sizes; do
	if ! [ -x $BFINT_DIR/bfint$cell_size ]; then
	    echo >&2 "missing bfint: $BFINT_DIR/bfint$cell_size"
	    exit 1
	fi
    done
fi

# prepare
test -d $BUILD_DIR && rm -r $BUILD_DIR
mkdir $BUILD_DIR
if echo "$methods" | grep "gcc" >/dev/null; then
    cp $awib_build $BUILD_DIR/awib.c
    gcc $BUILD_DIR/awib.c -o $BUILD_DIR/awib 2>/dev/null >/dev/null
fi

function compile {
    testcase=$1
    method=$2
    target=$3

    out=$BUILD_DIR/$testcase
    test -f $out && rm $out

    case $method in

	bfint)
	    for cell_size in $CELL_SIZES; do
		for eof_behaviour in $EOF_BEHAVIOURS; do
		    (echo "@$target"; cat ${testcase}.b) |
		    $BFINT_DIR/bfint$cell_size $awib_build $eof_behaviour > $out.$cell_size.$eof_behaviour
		    if [ -f $out ] && ! cmp $out $out.$cell_size.$eof_behaviour; then
			echo >&2 "output differs from ($prev_cs, $prev_eb) to ($cell_size, $eof_behaviour)"
			return 1
		    fi
		    mv $out.$cell_size.$eof_behaviour $out
		    prev_cs=$cell_size
		    prev_eb=$eof_behaviour
		done
	    done
	    ;;

	gcc)
	    if ! [ -x $BUILD_DIR/awib.bin ]; then
		cp $awib_build $BUILD_DIR/awib.c
		gcc $BUILD_DIR/awib.c -o $BUILD_DIR/awib.bin -O2 2>/dev/null
	    fi
	    (echo "@$target"; cat ${testcase}.b) |
	    $BUILD_DIR/awib.bin > $out
	    ;;

	bash)
	    (echo "@$target"; cat ${testcase}.b) |
	    bash $awib_build > $out
	    ;;
    esac

    case $target in

        lang_c)
	    mv $out $out.c
	    gcc $out.c -o $out 2>/dev/null >/dev/null
            ;;

        386_linux)
	    chmod +x $out
	    ;;

	lang_ruby)
	    chmod +x $out
            ;;

	lang_go)
	    mv $out $out.go
	    8g -o $out.8 $out.go
	    8l -o $out $out.8
	    ;;

    esac

    return 0
}

for method in $methods; do
    for testcase in $test_cases; do
	input="/dev/null"
	if [ -f $testcase.in ]; then
	    input=$testcase.in
	fi
	expected_output="/dev/null"
	if [ -f $testcase.out ]; then
	    expected_output=$testcase.out
	fi

	for target in $targets; do
	    echo -ne "$(date +%y%m%d_%k%M%S): $method $testcase $target \t"
	    compile $testcase $method $target
	    $BUILD_DIR/$testcase < $input > $BUILD_DIR/$testcase.out
	    if ! cmp $BUILD_DIR/$testcase.out $expected_output; then
		echo "FAIL"
		exit 1
	    fi
	    echo "WIN"
	done
    done
done
echo "$(date +%y%m%d_%k%M%S): all good in the hood"
