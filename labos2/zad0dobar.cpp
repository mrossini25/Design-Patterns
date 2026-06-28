#include <iostream>
#include <assert.h>
#include <stdlib.h>
#include <list>

class Shape {
    public :
    virtual void draw()=0;
    virtual void move(int dx, int dy)=0;
};

class Circle : public Shape {
    virtual void draw (){
        std::cout << "in draw Circle\n";
    };
    virtual void move(int dx, int dy){
        std::cout << "in move Circle\n";
    }
};

class Square : public Shape {
    virtual void draw (){
        std::cout << "in draw Square\n";
    };
    virtual void move(int dx, int dy){
        std::cout << "in move Square\n";
    }
};

class Rhomb : public Shape {
    virtual void draw (){
        std::cout << "in draw Rhomb\n";
    };
    virtual void move(int dx, int dy){
        std::cout << "in move Rhomb\n";
    }
};

void drawShapes (const std::list<Shape*>& fig) {
    std::list<Shape*>:: const_iterator it;
    for (it = fig.begin(); it != fig.end(); ++ it) {
        (*it) -> draw();
    } 
}

void moveShapes (const std::list<Shape*>& fig, int dx, int dy) {
    std::list<Shape*>:: const_iterator it;
    for (it = fig.begin(); it != fig.end(); ++ it) {
        (*it) -> move(dx, dy);
    } 
}

int main() {
    std::list<Shape*> shapes;
    shapes.push_back(new Circle());
    shapes.push_back(new Square());
    shapes.push_back(new Rhomb());
    
    drawShapes(shapes);
    moveShapes(shapes, 1, 2);

    for (auto shape : shapes) {
        delete shape;
    }
    
    return 0;
}