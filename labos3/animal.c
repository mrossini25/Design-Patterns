#include "animal.h"
#include <stdio.h>

struct Animal;

typedef char const* (*PTRFUN) (struct Animal *);

struct Animal{
  PTRFUN* vptr;
  // vtable entries:
  // 0: char const* name(void* this);
  // 1: char const* greet();
  // 2: char const* menu();
};

void animalPrintGreeting(struct Animal* a) {
    printf("%s pozdravlja: %s\n", a->vptr[0](a), a->vptr[1](a));
}

void animalPrintMenu(struct Animal* a) {
    printf("%s voli %s\n", a->vptr[0](a), a->vptr[2](a));
}