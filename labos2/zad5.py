from abc import ABC, abstractmethod
import time


class Izvor(ABC):
    @abstractmethod
    def ucitajBrojeve(self):
        pass   

class TipkovnickiIzvor(Izvor):
    def ucitajBrojeve(self):
        try:
            return int(input("Unesite broj: "))
        except ValueError:
            return -1

class DatotecniIzvor(Izvor):
    def __init__(self, filename):
        self.file = open(filename, 'r')
        self.brojevi = [int(line) for line in self.file.readlines()]
        self.index = 0
        
    def ucitajBrojeve(self):
        if self.index < len(self.brojevi):
            broj = self.brojevi[self.index]
            self.index += 1
            return broj
        else:
            return -1
    
    
class Akcija(ABC):
    @abstractmethod
    def izvrsi(self, kolekcija):
        pass
    
class IspisSume(Akcija):
    def izvrsi(self, kolekcija):
        print(f"Suma: {sum(kolekcija)}")
        
class IspisProsjek(Akcija):
    def izvrsi(self, kolekcija):
        print(f"Prosjek: {sum(kolekcija)/len(kolekcija)}")
        
class IspisMedijan(Akcija):
    def izvrsi(self, kolekcija):
        brojEl = len(kolekcija)
        if brojEl % 2 == 0:
            medijan = (kolekcija[brojEl // 2 -1] + kolekcija[brojEl // 2]) / 2
        else:
            medijan = kolekcija[brojEl // 2]
        print(f"Medijan: {medijan}")

class ZapisUDatoteku(Akcija):
    def izvrsi(self, kolekcija):
        with open('izlaz.txt', 'w') as f:
            f.write(f"{kolekcija} - {time.strftime('%d-%m-%Y %H:%M:%S')}\n")


class SlijedBrojeva:
    def __init__(self, izvor: Izvor):
        self.izvor = izvor
        self.kolekcija = []
        self.akcije = []

    def dodaj_akciju(self, akcija):
        self.akcije.append(akcija)
    
    def kreni(self):
        while True:
            broj = self.izvor.ucitajBrojeve()
            if broj == -1:
                break
            self.kolekcija.append(broj)
            for akcija in self.akcije:
                akcija.izvrsi(self.kolekcija)
            time.sleep(1)
   
#slijed = SlijedBrojeva(DatotecniIzvor("brojevi.txt"))
slijed = SlijedBrojeva(TipkovnickiIzvor())

slijed.dodaj_akciju(IspisSume())
slijed.dodaj_akciju(IspisProsjek())
slijed.dodaj_akciju(IspisMedijan())
slijed.dodaj_akciju(ZapisUDatoteku())

slijed.kreni()