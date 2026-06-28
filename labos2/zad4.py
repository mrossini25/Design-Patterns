from abc import ABC, abstractmethod
import random


class Generiraj(ABC):
    @abstractmethod
    def generirajBrojeve(self, *args):
        pass
    
class PercentileStrategija(ABC):
    @abstractmethod
    def odrediPercentil(self, podaci, percentil):
        pass
    
class DistributionTester:
    def __init__(self, distribucija: Generiraj, strategija: PercentileStrategija = None):
        self.distribucija = distribucija
        self.strategija = strategija

    def postaviStrategiju(self, strategija: PercentileStrategija):
        self.strategija = strategija

    def generirajBr(self, *args):
        podaci = self.distribucija.generirajBrojeve(*args)
        
        print("Generirani brojevi:", podaci)
        for p in range(10, 100, 10):
            percentil = self.strategija.odrediPercentil(podaci, p)
            print(f"{p}%: {percentil}")
        return podaci
    
    def pronadiPercentil(self, podaci, percentil):
        return self.strategija.odrediPercentil(podaci, percentil)
    
class Slijedno(Generiraj):
    def generirajBrojeve(self, *args):
        brojevi = []
        a = args[0]
        b = args[1]
        korak = args[2]
        for i in range(a, b + 1, korak):
            brojevi.append(i)
        
        return brojevi
    
class Slucajno(Generiraj):
    def generirajBrojeve(self, *args):
        brojevi = []
        srednjaVr = args[0]
        sd = args[1]
        n = args[2]
        for _ in range(n):
            brojevi.append(round(srednjaVr + sd * (sum(random.random() for _ in range(12)) - 6)))
        brojevi = sorted(brojevi)
        return brojevi
    
class Fibonacci(Generiraj):
    def generirajBrojeve(self, *args):
        brojevi = []
        ukupniBroj = args[0]
        broj = 1
        for i in range(ukupniBroj):
            brojevi.append(broj)
            if i != 0: 
                broj += brojevi[i - 1]
        return brojevi

class NearestRankPercentile(PercentileStrategija):
    def odrediPercentil(self, podaci, p):
        if not podaci:
            return None
        podaci = sorted(podaci)
        N = len(podaci)
        n_p = p * N / 100 + 0.5
        index = int(round(n_p)) - 1
        index = max(0, min(index, N - 1))
        return podaci[index]

class InterpolatedPercentile(PercentileStrategija):
    def odrediPercentil(self, podaci, p):
        data_sorted = sorted(podaci)
        N = len(podaci)
        if N == 0:
            return None

        percentiles = [100 * (i + 0.5) / N for i in range(N)]

        if p <= percentiles[0]:
            return data_sorted[0]
        if p >= percentiles[-1]:
            return data_sorted[-1]

        for i in range(N - 1):
            p1, p2 = percentiles[i], percentiles[i+1]
            if p1 <= p <= p2:
                v1, v2 = data_sorted[i], data_sorted[i+1]
                interpolated = v1 + N * (p - p1) * (v2 - v1) / 100
                return interpolated

        return None


if __name__ == "__main__":
    uniformna = DistributionTester(Slijedno(), NearestRankPercentile())
    uniformna.generirajBr(1, 10, 2)
    
    uniformna = DistributionTester(Slucajno(), InterpolatedPercentile())
    uniformna.generirajBr(50, 5, 10)
    
    uniformna = DistributionTester(Fibonacci(), NearestRankPercentile())
    uniformna.generirajBr(10)
    