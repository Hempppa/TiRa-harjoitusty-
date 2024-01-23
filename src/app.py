Pelilauta = [["R","H","B","Q","K","B","H","R"],
            ["P","P","P","P","P","P","P","P"],
            ["_","_","_","_","_","_","_","_"],
            ["_","_","_","_","_","_","_","_"],
            ["_","_","_","_","_","_","_","_"],
            ["_","_","_","_","_","_","_","_"],
            ["p","p","p","p","p","p","p","p"],
            ["r","h","b","q","k","b","h","r"]]
pelinappulat = [["p","r","h","b","q","k"],["P","R","H","B","Q","K"]]



#!!! Puuttuu vielä varsinaisen siirron toteuttaminen, shakin estäminen, matin tunnistaminen sekä mahdolliset erikoisliikkeet ja tietenkin itse shakkibotti



def alku():
    while True:
        print("Pelistä voi poistua kirjoittamalla quit")
        valinta = input("Kaksinpeli (2P) vai tekoalya vastaan (1P)")
        if valinta == "quit":
            break
        if valinta == "2P":
            kaksinpeli()
        if valinta == "1P":
            yksinpeli()

def kaksinpeli():
    vuoro = 0
    

def laillinen_siirto(siirto, vuoro):
    if siirto[0] not in ("a","b","c","d","e","f","g","h") or siirto[2] not in ("a","b","c","d","e","f","g","h"):
        return False
    if siirto[1] not in (1,2,3,4,5,6,7,8) or siirto[3] not in (1,2,3,4,5,6,7,8):
        return False
    
def kaikki_lailliset_siirrot(Pelilauta, vuoro, automaatti):
    siirrot = []
    omat = pelinappulat[vuoro]
    for y in range(8):
        for x in range(8):
            pelinappula = Pelilauta[y][x]
            if pelinappula == "_":
                pass
            elif pelinappula == omat[0]:
                if y == 1 and Pelilauta[y+1][x] == "_" and Pelilauta[y+2][x] == "_":
                    siirrot.append()
                    siirrot.append()
                if y < 7:
                    if Pelilauta[y+1][x] == "_":
                        siirrot.append()
                    if x > 0 and Pelilauta[y+1][x-1] not in omat:
                        siirrot.append()
                    if x < 7 and Pelilauta[y+1][x+1] not in omat:
                        siirrot.append()
            elif pelinappula == omat[1]:
                for i in range(x+1, 7):
                    if Pelilauta[y][i] == "_":
                        siirrot.append()
                    if Pelilauta[y][i] not in omat:
                        siirrot.append()
                        break
                    if Pelilauta[y][i] in omat:
                        break
                for i in range(x-1, -1):
                    if Pelilauta[y][i] == "_":
                        siirrot.append()
                    if Pelilauta[y][i] not in omat:
                        siirrot.append()
                        break
                    if Pelilauta[y][i] in omat:
                        break
                for i in range(y+1, 7):
                    if Pelilauta[i][x] == "_":
                        siirrot.append()
                    if Pelilauta[i][x] not in omat:
                        siirrot.append()
                        break
                    if Pelilauta[i][x] in omat:
                        break
                for i in range(y-1, -1):
                    if Pelilauta[i][x] == "_":
                        siirrot.append()
                    if Pelilauta[i][x] not in omat:
                        siirrot.append()
                        break
                    if Pelilauta[i][x] in omat:
                        break
            elif pelinappula == omat[2]:
                if y < 6 and x < 7 and Pelilauta[y+2][x+1] not in omat:
                    siirrot.append()
                if y < 6 and x > 0 and Pelilauta[y+2][x-1] not in omat:
                    siirrot.append()
                if y > 1 and x < 7 and Pelilauta[y-2][x+1] not in omat:
                    siirrot.append()
                if y > 1 and x > 0 and Pelilauta[y-2][x-1] not in omat:
                    siirrot.append()
                if y < 7 and x < 6 and Pelilauta[y+1][x+2] not in omat:
                    siirrot.append()
                if y < 7 and x > 1 and Pelilauta[y+1][x-2] not in omat:
                    siirrot.append()
                if y > 0 and x < 6 and Pelilauta[y-1][x+2] not in omat:
                    siirrot.append()
                if y > 0 and x > 1 and Pelilauta[y-1][x-2] not in omat:
                    siirrot.append()
            elif pelinappula == omat[3]:
                for i in range(8):
                    if x+i > 7 or y+i > 7 or Pelilauta[y+i][x+i] in omat:
                        break
                    if Pelilauta[y+i][x+i] == "_":
                        siirrot.append()
                    if Pelilauta[y+i][x+i] not in omat:
                        siirrot.append()
                        break
                for i in range(8):
                    if x-i < 0 or y+i > 7 or Pelilauta[y+i][x-i] in omat:
                        break
                    if Pelilauta[y+i][x-i] == "_":
                        siirrot.append()
                    if Pelilauta[y+i][x-i] not in omat:
                        siirrot.append()
                        break
                for i in range(8):
                    if x+i > 7 or y-i < 0 or Pelilauta[y-i][x+i] in omat:
                        break
                    if Pelilauta[y-i][x+i] == "_":
                        siirrot.append()
                    if Pelilauta[y-i][x+i] not in omat:
                        siirrot.append()
                        break
                for i in range(8):
                    if x-i < 0 or y-i < 0 or Pelilauta[y-i][x-i] in omat:
                        break
                    if Pelilauta[y-i][x-i] == "_":
                        siirrot.append()
                    if Pelilauta[y-i][x-i] not in omat:
                        siirrot.append()
                        break
            elif pelinappula == omat[4]:
                for i in range(x+1, 7):
                    if Pelilauta[y][i] == "_":
                        siirrot.append()
                    if Pelilauta[y][i] not in omat:
                        siirrot.append()
                        break
                    if Pelilauta[y][i] in omat:
                        break
                for i in range(x-1, -1):
                    if Pelilauta[y][i] == "_":
                        siirrot.append()
                    if Pelilauta[y][i] not in omat:
                        siirrot.append()
                        break
                    if Pelilauta[y][i] in omat:
                        break
                for i in range(y+1, 7):
                    if Pelilauta[i][x] == "_":
                        siirrot.append()
                    if Pelilauta[i][x] not in omat:
                        siirrot.append()
                        break
                    if Pelilauta[i][x] in omat:
                        break
                for i in range(y-1, -1):
                    if Pelilauta[i][x] == "_":
                        siirrot.append()
                    if Pelilauta[i][x] not in omat:
                        siirrot.append()
                        break
                    if Pelilauta[i][x] in omat:
                        break
                for i in range(8):
                    if x+i > 7 or y+i > 7 or Pelilauta[y+i][x+i] in omat:
                        break
                    if Pelilauta[y+i][x+i] == "_":
                        siirrot.append()
                    if Pelilauta[y+i][x+i] not in omat:
                        siirrot.append()
                        break
                for i in range(8):
                    if x-i < 0 or y+i > 7 or Pelilauta[y+i][x-i] in omat:
                        break
                    if Pelilauta[y+i][x-i] == "_":
                        siirrot.append()
                    if Pelilauta[y+i][x-i] not in omat:
                        siirrot.append()
                        break
                for i in range(8):
                    if x+i > 7 or y-i < 0 or Pelilauta[y-i][x+i] in omat:
                        break
                    if Pelilauta[y-i][x+i] == "_":
                        siirrot.append()
                    if Pelilauta[y-i][x+i] not in omat:
                        siirrot.append()
                        break
                for i in range(8):
                    if x-i < 0 or y-i < 0 or Pelilauta[y-i][x-i] in omat:
                        break
                    if Pelilauta[y-i][x-i] == "_":
                        siirrot.append()
                    if Pelilauta[y-i][x-i] not in omat:
                        siirrot.append()
                        break
            elif pelinappula == omat[5]:
                #automaatin ei tarvitse estää shakkimattia, sillä pelajaankin siirrot lasketaan optimaalisesti, eli sellaista siirtoa ei pelata/arvioida
                #Muuten tarvitsisi tarkistaa mihin kaikki nappulat voi liikkua
                if automaatti:
                    if x < 7 and Pelilauta[y][x+1] not in omat:
                        siirrot.append()
                    if x > 0 and Pelilauta[y][x-1] not in omat:
                        siirrot.append()
                    if y < 7 and Pelilauta[y+1][x] not in omat:
                        siirrot.append()
                    if y > 1 and Pelilauta[y-1][x] not in omat:
                        siirrot.append()
                    if y < 7 and x < 7 and Pelilauta[y+1][x+1] not in omat:
                        siirrot.append()
                    if y < 7 and x > 0 and Pelilauta[y+1][x-1] not in omat:
                        siirrot.append()
                    if y > 0 and x < 7 and Pelilauta[y-1][x+1] not in omat:
                        siirrot.append()
                    if y > 0 and x > 0 and Pelilauta[y-1][x-1] not in omat:
                        siirrot.append()
                else:
                    valiaika = []
                    if x < 7 and Pelilauta[y][x+1] not in omat:
                        valiaika.append()
                    if x > 0 and Pelilauta[y][x-1] not in omat:
                        valiaika.append()
                    if y < 7 and Pelilauta[y+1][x] not in omat:
                        valiaika.append()
                    if y > 1 and Pelilauta[y-1][x] not in omat:
                        valiaika.append()
                    if y < 7 and x < 7 and Pelilauta[y+1][x+1] not in omat:
                        valiaika.append()
                    if y < 7 and x > 0 and Pelilauta[y+1][x-1] not in omat:
                        valiaika.append()
                    if y > 0 and x < 7 and Pelilauta[y-1][x+1] not in omat:
                        valiaika.append()
                    if y > 0 and x > 0 and Pelilauta[y-1][x-1] not in omat:
                        valiaika.append()
                    if vuoro == 0:
                        vastapuoli = kaikki_lailliset_siirrot(Pelilauta, 1, True)
                    else:
                        vastapuoli = kaikki_lailliset_siirrot(Pelilauta, 0, True)
                    for siirto in vastapuoli:
                        if siirto[2:] in valiaika:
                            valiaika.remove(siirto[2:])


def yksinpeli():
    return

x = 2
y = 3
print(x, y)