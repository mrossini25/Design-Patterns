def mymax(iterable, key=lambda x: x):
    
    max_x = max_key = None
    
    for x in iterable:
        current_key = key(x)
        if max_key is None or current_key > max_key:
            max_x = x
            max_key = current_key
    
    return max_x


print("Najveci element:", mymax([1, 3, 2]))

print("Najduza rijec:", mymax(["jabuka", "banana", "tresnja", "lubenica"], key = lambda x: len(x)))
print("Najveci element:", mymax(["jabuka", "banana", "tresnja", "lubenica"]))

D = {'burek':8, 'buhtla':5}
najskuplji = mymax(D, key=D.get)
print("Najskuplji proizvod:", najskuplji)

lista_osoba = [("marko", "polo"), ("nikola", "tesla"), ("benjamin", "franklin"), ("luka", "modric"), ("ivan", "gundulic")]
posljednja_osoba = mymax(lista_osoba)
print(posljednja_osoba)