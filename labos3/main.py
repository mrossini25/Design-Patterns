import os
from myfactory import myfactory

def printGreeting(pet):
    print(f"{pet.name()} pozdravlja: {pet.greet()}")

def printMenu(pet):
    print(f"{pet.name()} voli {pet.menu()}")

def test():
  pets=[]
  for mymodule in os.listdir('plugins'):
    moduleName, moduleExt = os.path.splitext(mymodule)
    if moduleExt=='.py':
      ljubimac=myfactory(moduleName)('Ljubimac '+str(len(pets)))
      pets.append(ljubimac)

  for pet in pets:
    printGreeting(pet)
    printMenu(pet)
    
if __name__ == '__main__':
    test()