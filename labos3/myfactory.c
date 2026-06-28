#include "myfactory.h"

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>

typedef void* (*ConstructFunc)(void*, const char*);
typedef size_t (*SizeOfFunc)();

void* myfactory(char const* libname, char const* ctorarg, void* custom_memory) {
  char path[512];
    snprintf(path, sizeof(path), "./%s.dll", libname);

    HMODULE hLib = LoadLibrary(path);
    if (!hLib) return NULL;

    SizeOfFunc size_of = (SizeOfFunc)GetProcAddress(hLib, "size_of");
    ConstructFunc construct = (ConstructFunc)GetProcAddress(hLib, "construct");

    if (!size_of || !construct) {
        FreeLibrary(hLib);
        return NULL;
    }

    void* memory = custom_memory;
    if (!memory) {
        memory = malloc(size_of());
    }

    construct(memory, ctorarg);
    return memory;
}
