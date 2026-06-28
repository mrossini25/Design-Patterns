#include <stdio.h>
#include <stdlib.h>

typedef int (*PTRFUN1)(void* that);
typedef int (*PTRFUN2)(void* that, int);

class B{
  public:
    virtual int __cdecl prva()=0;
    virtual int __cdecl druga(int)=0;
  };
  
  class D: public B{
  public:
    virtual int __cdecl prva(){return 42;}
    virtual int __cdecl druga(int x){return this->prva()+x;}
  };

  void funkcija (B* pb){
    void** vTable =  *(void***)pb;
    PTRFUN1 f1 = (PTRFUN1)vTable[0];
    PTRFUN2 f2 = (PTRFUN2)vTable[1];
    int x = 2;
    printf("Prva:%d\n", f1(pb));
    printf("Druga:%d\n", f2(pb, x));
}

int main(void){
  B *pb = new D();
  funkcija(pb);
}

//var je pokazivac na objekt tipa D, kad ga castamo u void***, on postaje pokazivac na virtualnu tablicu objekta D,
//a onda ga derefernciramo s * i on postane bas virtualna tablica vTable (pokazivac na funkcije klase D)