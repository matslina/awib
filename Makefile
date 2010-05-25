all:	awib.b

binary: awib.b
	cp awib.b awib_make_binary.c
	gcc awib_make_binary.c -o awib_make_binary.bin -O2
	./awib_make_binary.bin < awib.b > awib_make_binary2.c
	gcc awib_make_binary2.c -o awib -O2

awib.b: awib-skeleton.b 386_linux/backend.b lang_c/backend.b frontend/frontend.b lang_generic/backend.b lang_generic/dummy.b lang_generic/python.b lang_generic/go.b lang_generic/ruby.b lang_generic/tcl.b
	python util/bfpp.py --interpreter --format formats/awib-0.2 --width 70 awib-skeleton.b > awib.b

clean:
	rm -f awib.b *~ awib_make_binary* awib
