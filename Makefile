
LD_FLAGS=-llua5.2

CC_FLAGS=-I/usr/include/lua5.2/


all: main.o
	gcc -o render main.o $(LD_FLAGS)
 
main.o: main.c
	gcc $(CC_FLAGS) -c -o main.o main.c

