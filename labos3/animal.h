#define ANIMAL_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct Animal Animal;

void animalPrintGreeting(Animal* a);
void animalPrintMenu(Animal* a);

#ifdef __cplusplus
}
#endif