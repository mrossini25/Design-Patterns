#include <stdlib.h>
#include <string.h>
#include <stdio.h>

struct Animal;

typedef const char* (*PTRFUN)(struct Animal*);

struct Animal {
    PTRFUN* vptr;
    char* name;
};

const char* parrot_name(struct Animal* this) {
    return this->name;
}

const char* parrot_greet(struct Animal* this) {
    return "Sto mu gromova!";
}

const char* parrot_menu(struct Animal* this) {
    return "brazilske orahe.";
}

PTRFUN parrot_vtable[] = { parrot_name, parrot_greet, parrot_menu };

void construct(void* memory, char* name) {
    struct Animal* a = (struct Animal*)memory;
    a->name = name;
    a->vptr = parrot_vtable;
}

size_t size_of() {
    return sizeof(struct Animal);
}

struct Animal* create(char* name) {
    struct Animal* a = (struct Animal*)malloc(sizeof(struct Animal));
    construct(a, name);
    return a;
}

