#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int gt_int(const void *a, const void *b) {
  int x = *(const int*)a;
  int y = *(const int*)b;
  return x > y ? 1 : 0;
}

int gt_char(const void *a, const void *b) {
  char x = *(const char*)a;
  char y = *(const char*)b;
  return x > y ? 1 : 0;
}

int gt_str(const void *a, const void *b) {
  const char* x = *(const char**)a;
  const char* y = *(const char**)b;
  return strcmp(x, y) > 0 ? 1 : 0;
}

const void* mymax(
  const void *base, size_t nmemb, size_t size,
  int (*compar)(const void *, const void *)) 
{
  const char *ptr = (const char*)base;
  const void *max = ptr;
  for (size_t i = 1; i < nmemb; i++) {
      if (compar(ptr + i * size, max) > 0) {
          max = ptr + i * size;
      }
  }
  return max;
}

int main() {
  int x = 5;
  int y = 3;
  //printf("%d", gt_int(&x, &y)); 

  int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
  char arr_char[]="Suncana strana ulice";
  const char* arr_str[] = {
    "Gle", "malu", "vocku", "poslije", "kise",
    "Puna", "je", "kapi", "pa", "ih", "njise"
  };

  size_t n1 = sizeof(arr_int) / sizeof(arr_int[0]);
  const int* maxInt = (const int*)mymax(arr_int, n1, sizeof(int), gt_int);
  printf("Najveci int element: %d\n", *maxInt);

  size_t n2 = sizeof(arr_char) / sizeof(arr_char[0]);
  const char* maxChar = (const char*)mymax(arr_char, n2, sizeof(char), gt_char);
  printf("Najveci char element: %c\n", *maxChar);

  size_t n3 = sizeof(arr_str) / sizeof(arr_str[0]);
  const char** maxStr = (const char**)mymax(arr_str, n3, sizeof(const char*), gt_str);
  printf("Najveci str element: %s\n", *maxStr);
}