#include <stdlib.h>
#include <string.h>
#include <stdio.h>

struct Animal;

typedef const char* (*PTRFUN)(struct Animal*);

struct Animal {
    PTRFUN* vptr;
    char* name;
};

const char* tiger_name(struct Animal* this) {
    return this->name;
}

const char* tiger_greet(struct Animal* this) {
    return "Mijau!";
}

const char* tiger_menu(struct Animal* this) {
    return "mlako mlijeko.";
}

PTRFUN tiger_vtable[] = { tiger_name, tiger_greet, tiger_menu };

void construct(void* memory, char* name) {
    struct Animal* a = (struct Animal*) memory;
    a->name = name;
    a->vptr = tiger_vtable;
}

size_t size_of() {
    return sizeof(struct Animal);
}

struct Animal* create(char* name) {
    struct Animal* a = (struct Animal*)malloc(sizeof(struct Animal));
    construct(a, name);
    return a;
}

