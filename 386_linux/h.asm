;;; This file holds the asm-stuff for the awib i386-backend
;;; Compile with 'nasm -f bin h.asm'
;;;
;;; 2007-10-26  Made jump from CLOSE conditional for performance reasons
;;; 2007-08-25  Modifications for the new awib rewrite
;;; Mats Linander - 2003-04-27
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
USE32				; 32 bit mode (nasm defaults to 16 on -f bin)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; ELF header starts here
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
ELF_start:
	db	0x7f,"ELF"	; Magic number (ELF identifier)
	db	0x01		; architecture:	 32 bit
	db	0x01		; byte order:	little endian
	db	0x01		; ELF version:	current
	db	3,0		; OS/ABI extensions, (GNU/Linux)
times 7	db	0		; 7 byte zero padding
	dw	2		; type:	executable file
	dw	3		; machine:	 Intel 80386
	dd	1		; ELF version:	current
	dd	code_start	; entry point
	dd	phdroffset	; program header offset
	dd	0		; section header:	Nope
	dd	0		; processor specific flags:	None
	dw	ELFsize		; ELF header size
	dw	phdrsize	; size of a program header
	dw	1		; number of entries in program header table
	dw	0x28		; size of section header entry (0x28 is ok)
	dw	0		; number of entries in section header table
	dw	0		; section header index thing? nope
ELF_end:
ELFsize	equ	ELF_end-ELF_start ; size of elf header
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; ELF header END
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Program header starts here
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
p_hdr_start:
	dd	1		; this header specifies a loadable segment
	dd	0		; offset to segment
	dd	0		; segment virtual address (don't care)
	dd	0		; physical address (don't care)
	dd	fsize		; size of file
	dd	fsize		; required memory
	dd	4|2|1		; segment flags, 1=exec 2=write 4=read
	dd	0		; alignment something
p_hdr_end:
phdrsize: equ	p_hdr_end-p_hdr_start ; size of program header
phdroffset: equ	p_hdr_start-ELF_start ; offset to program header
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;  Program header END
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Code starts here
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
code_start:
;;; Allocate memory area by calling mmap2
	mov	eax,0xc0	; sys_mmap
	xor	ebx,ebx		; *start=0
	mov	ecx,0xffff	; length=0xffff
	mov	edx,3		; prot=PROT_READ|PROT_WRITE
	mov	esi,0x22	; flags=MAP_ANONYMOUS|MAP_PRIVATE
	xor	edi,edi		; fd=0
	xor	ebp,ebp		; offset=0
	int	0x80

;;; Initialize cells to zero (0)
	mov	edx,eax		; save address in edx
	xchg	eax,edi		; edi:=&p  eax:=0
	cld			; clear direction flag for stosb
	rep	stosb		; stosb al to [edi] ecx times

;;; Prepare registers for exeution of bf-code
	mov	ecx,edx		; ecx = p
	mov	ebx,eax		; ebx = 1
	inc	ebx
	mov	edx,ebx		; edx = 1
	mov	edi,ebx		; edi = 3
	inc	edi
	inc	edi
	mov	esi,edi		; esi = 4
	inc	esi
	xor	eax,eax		; eax = 0
	inc	ebp
	inc	ebp

	jmp over


;;; The compiled bytecode is inserted here! It must be terminated
;;; by an exit(0)-call.
;;;
;;; Below are implementations of each bytecode operation. For these
;;; to work, the following conditions must hold prior to and after
;;; each operation:
;;;	ebx = 1
;;;	ecx = p  (address of memory area)
;;;	edx = 1
;;;	edi = 3
;;;	esi = 4
;;;	ebp = 2

;;; RIGHT(1)
	inc	ecx
;;; RIGHT(2)
	add	ecx,ebp
;;; RIGHT(i)	2<i<=127
	add	ecx,byte 127

;;; LEFT(1)
	dec	ecx
;;; LEFT(2)
	sub	ecx,ebp
;;; LEFT(i)	2<i<=127
	sub	ecx,byte 127

;;; ADD(1)
	inc	byte [ecx]
;;; ADD(i)	1<i<=255
	add	byte [ecx],255

;;; SUB(1)
	dec	byte [ecx]
;;; SUB(i)   1<i<=255
	sub	byte [ecx],255

;;; OUTPUT
	mov	eax,esi		; eax=esi=4 (sys_write)
	int	0x80		; write edx bytes from [ecx] to fd ebx

;;; INPUT
	mov	eax,edi		; eax=edi=3 (sys_read)
	dec	ebx		; ebx-1==0 (stdin)
	int	0x80		; read edx bytes to [ecx] from fd ebx
	inc	ebx		; restore ebx

;;; CLEAR
	mov	[ecx],bh

;;; OPEN
	cmp	bh,[ecx]
	je	near word $+12	; jump past CLOSE if *p==0

;;; CLOSE
	cmp	bh,[ecx]
	jne	near word $-2 	; jump to start of loop body if *p!=0

over:
;;; Here's the final syscall for exit(0)
	mov	eax,ebx
	dec	ebx
	int	0x80

	fsize	equ	$-$$		; size of this file
