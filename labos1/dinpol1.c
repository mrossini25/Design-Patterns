#include <stdio.h>
#include <stdlib.h>

typedef char const* (*PTRFUN)();

char const* dogGreet(void){
    return "vau!";
}
char const* dogMenu(void){
    return "kuhanu govedinu";
}
char const* catGreet(void){
    return "mijau!";
}
char const* catMenu(void){
    return "konzerviranu tunjevinu";
}

PTRFUN dogVTable[] = {dogGreet, dogMenu};
PTRFUN catVTable[] = {catGreet, catMenu};

struct Animal {
    char* name;
    PTRFUN* vTable;
};

void animalPrintGreeting(struct Animal* a) {
    printf("%s pozdravlja: %s\n", a->name, a->vTable[0]());
}

void animalPrintMenu(struct Animal* a) {
    printf("%s voli %s\n", a->name, a->vTable[1]());
}

void constructDog(struct Animal* a, char* name) {
    a->name = name;
    a->vTable = dogVTable;
}

void constructCat(struct Animal* a, char* name) {
    a->name = name;
    a->vTable = catVTable;
}

struct Animal* createDog(char* name) {
    struct Animal* a = (struct Animal*)malloc(sizeof(struct Animal));
    constructDog(a, name);
    return a;
}

struct Animal* createCat(char* name) {
    struct Animal* a = (struct Animal*)malloc(sizeof(struct Animal));
    constructCat(a, name);
    return a;
}

struct Animal* createNDogs(int n, char** names) {
    struct Animal* dogs = (struct Animal*)malloc(n * sizeof(struct Animal));
    
    for (int i = 0; i < n; i++) {
        constructDog(&dogs[i], names[i]);
    }
    
    return dogs;
}

void testAnimals(void) {
    struct Animal* p1 = createDog("Hamlet");
    struct Animal* p2 = createCat("Ofelija");
    struct Animal* p3 = createDog("Polonije");

    animalPrintGreeting(p1);
    animalPrintGreeting(p2);
    animalPrintGreeting(p3);

    animalPrintMenu(p1);
    animalPrintMenu(p2);
    animalPrintMenu(p3);

    free(p1); 
    free(p2); 
    free(p3);
}

void testHeapStack(void) {
    struct Animal* h1 = createDog("heapPas");
    struct Animal* h2 = createCat("heapMacka");
    struct Animal s1;
    struct Animal s2;
    constructDog(&s1, "stackPas");
    constructCat(&s2, "stackMacka");

    printf("\nObjekti na gomili :\n");
    animalPrintGreeting(h1);
    animalPrintGreeting(h2);
    animalPrintMenu(h1);
    animalPrintMenu(h2);

    printf("\nObjekti na stogu:\n");
    animalPrintGreeting(&s1);
    animalPrintGreeting(&s2);
    animalPrintMenu(&s1);
    animalPrintMenu(&s2);

    // Oslobađanje memorije samo za objekte na gomili!
    free(h1);
    free(h2);
}

void testNDogs(void) {
    char* dogNames[] = {"Pas1", "Pas2", "Pas3", "Pas4"};
    int n = sizeof(dogNames)/sizeof(dogNames[0]);
    
    struct Animal* dogs = createNDogs(n, dogNames);
    
    printf("\nKreirani psi:\n");
    for (int i = 0; i < n; i++) {
        animalPrintGreeting(&dogs[i]);
        animalPrintMenu(&dogs[i]);
    }

    free(dogs);
}

int main() {
    testAnimals();
    testHeapStack();
    testNDogs();
    return 0;
}
