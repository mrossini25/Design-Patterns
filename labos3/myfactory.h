#define MYFACTORY_H
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef void* (*ConstructFunc)(void*, const char*);
typedef size_t (*SizeOfFunc)();

void* myfactory(char const* libname, char const* ctorarg, void* memory);

#ifdef __cplusplus
}
#endif
