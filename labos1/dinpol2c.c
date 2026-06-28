#include <stdio.h>
#include <stdlib.h>

typedef struct Unary_Function Unary_Function;

typedef double (*PTRFUN)(Unary_Function*, double);

typedef struct Unary_Function {
    int lb;
    int ub;
    PTRFUN* vTable;
} Unary_Function;

typedef struct {
    Unary_Function base;
} Square;

typedef struct {
    Unary_Function base;
    double a;
    double b;
} Linear;

double value_at_square(Unary_Function* uf, double x) {
    return x*x;
}

double value_at_linear(Unary_Function* uf, double x) {
    Linear* ln = (Linear*)uf;
    return ln->a*x + ln->b;
}

double negative_value_at_virtual(Unary_Function* uf, double x) { 
    return -uf->vTable[0](uf, x); 
}

PTRFUN squareVTable[] = {value_at_square, negative_value_at_virtual};
PTRFUN linearVTable[] = {value_at_linear, negative_value_at_virtual};

double negative_value_at(Unary_Function* uf, double x) {
    return uf->vTable[1](uf, x);
}

void tabulate(Unary_Function* uf) {
    for (int x = uf->lb; x <= uf->ub; x++) {
        printf("f(%d)=%lf\n", x, uf->vTable[0](uf, x));
    }
}

int same_functions_for_ints(Unary_Function* f1, Unary_Function* f2, double tolerance) {
    if (f1->lb != f2->lb) return 0;
    if (f1->ub != f2->ub) return 0;
    
    for (int x = f1->lb; x <= f1->ub; x++) {
        double delta = f1->vTable[0](f1, x) - f2->vTable[0](f2, x);
        if(delta < 0) delta = -delta;
        if (delta > tolerance) return 0;
    }
    return 1;
}

void constructSquare(Square* sq, int lb, int ub) {
    sq->base.lb = lb;
    sq->base.ub = ub;
    sq->base.vTable = squareVTable;
}

void constructLinear(Linear* ln, int lb, int ub, double a_coef, double b_coef) {
    ln->base.lb = lb;
    ln->base.ub = ub;
    ln->a = a_coef;
    ln->b = b_coef;
    ln->base.vTable = linearVTable;
}

Square* createSquare(int lb, int ub) {
    Square* sq = (Square*)malloc(sizeof(Square));
    constructSquare(sq, lb, ub);
    return sq;
}

Linear* createLinear(int lb, int ub, double a_coef, double b_coef) {
    Linear* ln = (Linear*)malloc(sizeof(Linear));
    constructLinear(ln, lb, ub, a_coef, b_coef);
    return ln;
}

int main() {
    Unary_Function* f1 = (Unary_Function*) createSquare(-2, 2);
    tabulate(f1);
    
    Unary_Function* f2 = (Unary_Function*) createLinear(-2, 2, 5, -2);
    tabulate(f2);
    
    printf("f1 == f2: %s\n", same_functions_for_ints(f1, f2, 1E-6) ? "DA" : "NE");
    printf("neg_val f2(1) = %lf\n", negative_value_at(f2, 1.0));
    
    free(f1);
    free(f2);
    return 0;
}