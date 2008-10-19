/* Simple brainfuck interpreter for the awib project.
 * To change cell size, redefine CELLSIZE at compile-time.
 *
 * Usage:
 *   ./bfint <program> [EOF-behaviour]
 * where <program> is file holding program to interpret
 * and   [EOF-behaviour] is 0 to write 0 on EOF,
 *                       is 1 to write -1 on EOF,
 *                       is 2 for no change on EOF  (default).
 *
 * Mats Linander 2007-09-17
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#ifndef CELLSIZE
#define CELLSIZE char
#endif
typedef CELLSIZE cell_t;

cell_t buf[65535];
char program[65535];
char *stack[10000];
int eof_behaviour = 2;

void usage(FILE *out, char *name) {
  fprintf(out,"Usage: %s <program> [EOF-behaviour]\n",name);
  fprintf(out,"  <program>:\t\tfile holding brainfuck code to interpret\n");
  fprintf(out,"  [EOF-behaviour]:\t0 to write 0 on EOF,\n\t\t\t"
	  "1 to write -1 on EOF\n\t\t\t2 for no change on EOF (default).\n");
}


/* Pushes p onto the stack.
 * Returns 0 on success,
 * returns -1 on error.
 */
static int sp = 0;
int push( char *p ) {
  if(sp<sizeof(stack)){
    stack[sp++] = p;
    return 0;
  }
  return -1;
}

/* Pops and returns top stack element.
 * Returns NULL on error.
 */
char *pop() {
  if(sp>=0)
    return stack[--sp];
  return NULL;
}


/* Finds the closing loop bracket (']') corresponding to the opening
 * loop bracket ('[') pointed at by 'prog'.
 * Returns pointer to closing bracket on success,
 * returns NULL on error.
 */
char *jump_past(char *prog) {
  int depth = 0;

  while(1){
    if( *prog=='[' ) depth++;
    if( *prog==']' ) depth--;
    if( *prog==0 ) return NULL;
    if( depth==0 ) return prog;
    prog++;
  }
  return prog;
}


/* Runs the code in program[].
 * Returns 0 on success,
 * returns -1 on error (and prints error messages to stderr).
 */
int run() {
  cell_t *p = buf;
  cell_t *pmax = &buf[sizeof(buf)-1];
  char *ip = program;
  char *tmp;
  int c;

  while( *ip!='\0' ) {
    //fprintf(stderr,"%3d:%c\t[%3d]=%02x\n",ip-program,*ip,p-buf,*p);
    //sleep(1);
    switch(*ip) {

    case(','):
      c = getchar();
      if( c<0 ) {
	if( eof_behaviour==1 )
	  *p = -1;
	else if( eof_behaviour==0 )
	  *p = 0;
      } else
	*p = c;
      break;

    case('.'):
      putchar(*p);
      break;

    case('+'):
      *p += 1;
      break;

    case('-'):
      if(*p<-256){
	fprintf(stderr,"bad loop detected at instruction %d\n",
		ip-program);
	return -1;
      }
      *p -= 1;
      break;

    case('>'):
      p++;
      break;

    case('<'):
      p--;
      break;

    case('['):
      if( *p==0 ) {
	tmp = jump_past(ip);
	if( tmp==NULL ) {
	  fprintf(stderr,"Error: Unbalanced loop at instruction %d.\n",
		  ip-program);
	  return -1;
	}
	ip = tmp;
      }
      else
	if( push(ip)<0 ) {
	  fprintf(stderr,"Error: Stack overflow! (too many nested loops)\n");
	  return -1;
	}
      break;

    case(']'):
      tmp = pop();
      if( tmp==NULL ) {
	fprintf(stderr,"Error: Stack underflow! (mismatched \']\')\n");
	return -1;
      }
      if( *p!=0 )
	ip = tmp - 1;
      break;
    }

    if( p>pmax ){
      fprintf(stderr,"Error: Pointer moved beyond memory area! (size=%d)\n",
	      sizeof(buf));
      return -1;
    }
    if( p<buf ){
      fprintf(stderr,"Error: Pointer moved below memory area!\n");
      return -1;
    }

    ip ++;
  }

  tmp = pop();
  if( tmp!=NULL ) {
    fprintf(stderr,"Error: Loop opened at instruction %d is never closed!\n",
	    tmp-program);
    return -1;
  }

  return 0;
}

int main(int argc, char *argv[]) {
  FILE *prog_file;
  int i,c;

  /* Read program into program[], catch help-requests and whatnot. */
  if( !argv[1] ){
    usage(stderr,argv[0]);
    exit(-1);
  }
  if( !strcmp(argv[1],"--help") || !strcmp(argv[1],"-h") ){
    usage(stdout,argv[0]);
    exit(0);
  }
  prog_file = fopen(argv[1],"r");
  if( !prog_file ){
    perror("Error: Could not open program file");
    exit(-1);
  }
  for( i=0; (c=fgetc(prog_file))!=EOF && i<sizeof(program); )
    if(c=='<'||c=='>'||c==','||c=='.'||c=='-'||c=='+'||c=='['||c==']')
      program[i++] = c;
  if( i==sizeof(program) ){
    fprintf(stderr,"Error: Program is too large, maximum is %d operations.\n",
	    sizeof(program));
    exit(-1);
  }
  fclose(prog_file);

  /* Optionally change the EOF-behaviour */
  if( argv[2] ) {
    sscanf(argv[2], "%d", &eof_behaviour);
    if(eof_behaviour<0 || eof_behaviour>2){
      fprintf(stderr,"Error: bad EOF-behaviour, must be 0, 1 or 2.\n");
      exit(-1);
    }
  }

  /* Now run the program */
  return run();
}
