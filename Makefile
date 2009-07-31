all:	awib

awib: awib-skeleton.b 386_linux/backend.b lang_c/backend.b frontend/frontend.b
	python util/bfpp.py --interpreter --format formats/awib-0.1 awib-skeleton.b > awib.b

clean:
	touch awib.b awib.b~
	rm awib.b *~
