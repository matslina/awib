all:	bfint

bfint: bfint8 bfint16 bfint32 bfint64
	

bfint8:	bfint.c
	gcc bfint.c -DCELLSIZE="int8_t" -o bfint8 -Wall
bfint16: bfint.c
	gcc bfint.c -DCELLSIZE="int16_t" -o bfint16 -Wall
bfint32: bfint.c
	gcc bfint.c -DCELLSIZE="int32_t" -o bfint32 -Wall
bfint64: bfint.c
	gcc bfint.c -DCELLSIZE="int64_t" -o bfint64 -Wall

clean:
	touch bfint8 bfint16 bfint32 bfint64  bfint.c~
	rm bfint8 bfint16 bfint32 bfint64 *.c~
