Pelilauta = [["R","H","B","Q","K","B","H","R"],
            ["P","P","P","P","p","P","P","P"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["p","p","p","p","p","p","p","p"],
            ["r","h","b","q","k","b","h","r"]]
pelinappulat = [["p","r","h","b","q","k"],["P","R","H","B","Q","K"]]
alkuvuoro = 0


#!!! Puuttuu vielä mahdolliset erikoisliikkeet, koodin laadun tarkistaminen, yksikkötestaaminen, kunnollinen koodin dokumentointi ja tietenkin itse shakkibotti

def alku():
    print("Pelistä voi poistua kirjoittamalla quit")
    print("Peli ei tunnista minkään näköisiä erikoissiirtoja")
    print("vain kaksinpeli toimii hetkellä")
    while True:
        valinta = input("Kaksinpeli (2p) vai tekoalya vastaan (1p): ")
        if valinta == "quit" or valinta == "q":
            break
        if valinta == "2p" or valinta == "2P" or valinta == "2":
            if kaksinpeli() == "quit":
                break
        if valinta == "1p" or valinta == "1P" or valinta == "1":
            if yksinpeli() == "quit":
                break

def kaksinpeli():
    vuoro = alkuvuoro
    Pelitilanne = Pelilauta
    while True:
        print()
        print("  ----------------------------")
        for y in range(8):
            rivi = str(y+1) + " | "
            for x in range(8):
                rivi += " " + Pelitilanne[y][x] + " "
            print(rivi + " | ")
        print("  ----------------------------")
        print("     a"," b"," c"," d"," e"," f"," g"," h")
        print()
        print("Pelaajan", vuoro+1, "vuoro")
        tilanne = matti(Pelitilanne, vuoro)
        if tilanne[0]:
            print()
            if vuoro == 0:
                print("Pelaaja 2 voitti!!!")
            else:
                print("Pelaaja 1 voitti!!!")
            print()
            return
        else:
            print("mahdolliset siirrot ", tilanne[1])
        siirto = input("Syötä siirto: ")
        if siirto == "quit":
            return "quit"
        if laillinen_siirto(Pelitilanne, siirto, vuoro):
            if vuoro == 1:
                vuoro = 0
            else:
                vuoro = 1
        else:
            print("Laiton siirto")

def matti(Pelitilanne, vuoro):
    mahdolliset = kaikki_lailliset_siirrot(Pelitilanne, vuoro, False)
    uusittu = []
    for siirto in mahdolliset:
        poistettu = tee_siirto(Pelitilanne, siirto)
        if not onko_shakki(Pelitilanne, vuoro):
            uusittu.append(siirto)
        peru_siirto(Pelitilanne, siirto, poistettu)
    if len(uusittu) == 0:
        return True, uusittu
    return False, uusittu

def laillinen_siirto(Pelitilanne, siirto, vuoro):
    if siirto[0] not in ("a","b","c","d","e","f","g","h") or siirto[2] not in ("a","b","c","d","e","f","g","h"):
        return False
    if siirto[1] not in ("1","2","3","4","5","6","7","8") or siirto[3] not in ("1","2","3","4","5","6","7","8"):
        return False
    if siirto not in kaikki_lailliset_siirrot(Pelitilanne, vuoro, False):
        return False
    poistettu = tee_siirto(Pelitilanne, siirto)
    if onko_shakki(Pelitilanne, vuoro):
        peru_siirto(Pelitilanne, siirto, poistettu)
        return False
    return True
    
def tee_siirto(Pelitilanne, siirto):
    mista_x = ord(siirto[0])-97
    mista_y = int(siirto[1])-1
    mihin_x = ord(siirto[2])-97
    mihin_y = int(siirto[3])-1
    poistettu = Pelitilanne[mihin_y][mihin_x]
    Pelitilanne[mihin_y][mihin_x] = Pelitilanne[mista_y][mista_x]
    Pelitilanne[mista_y][mista_x] = "-"
    return poistettu

def peru_siirto(Pelitilanne, siirto, nappula):
    mista_x = ord(siirto[0])-97
    mista_y = int(siirto[1])-1
    mihin_x = ord(siirto[2])-97
    mihin_y = int(siirto[3])-1
    Pelitilanne[mista_y][mista_x] = Pelitilanne[mihin_y][mihin_x]
    Pelitilanne[mihin_y][mihin_x] = nappula

def onko_shakki(Pelitilanne, vuoro):
    kingi = pelinappulat[vuoro][5]
    if vuoro == 0:
        vastapuoli = kaikki_lailliset_siirrot(Pelitilanne, 1, True)
    else:
        vastapuoli = kaikki_lailliset_siirrot(Pelitilanne, 0, True)
    for y in range(8):
        for x in range(8):
            if Pelitilanne[y][x] == kingi:
                sijainti = chr(x+97)+str(y+1)
    for siirto in vastapuoli:
        if siirto[2:] == sijainti:
            return True
    return False
    
def kaikki_lailliset_siirrot(Pelitilanne, vuoro, automaatti):
    siirrot = []
    omat = pelinappulat[vuoro]
    for y in range(8):
        for x in range(8):
            pelinappula = Pelitilanne[y][x]
            if pelinappula == "-":
                pass
            elif pelinappula == omat[0]:
                #p tai P
                if vuoro == 0:
                    if y > 0:
                        if Pelitilanne[y-1][x] == "-":
                            siirrot.append(chr(x+97)+str(y+1)+chr(x+97)+str(y+1-1))
                            if y == 6 and Pelitilanne[y-2][x] == "-":
                                siirrot.append(chr(x+97)+str(y+1)+chr(x+97)+str(y+1-2))
                        if x > 0 and Pelitilanne[y-1][x-1] not in omat and Pelitilanne[y-1][x-1] != "-":
                            siirrot.append(chr(x+97)+str(y+1)+chr(x+96)+str(y+1-1))
                        if x < 7 and Pelitilanne[y-1][x+1] not in omat and Pelitilanne[y-1][x+1] != "-":
                            siirrot.append(chr(x+97)+str(y+1)+chr(x+98)+str(y+1-1))
                else:
                    if y < 7:
                        if Pelitilanne[y+1][x] == "-":
                            siirrot.append(chr(x+97)+str(y+1)+chr(x+97)+str(y+1+1))
                            if y == 1 and Pelitilanne[y+2][x] == "-":
                                siirrot.append(chr(x+97)+str(y+1)+chr(x+97)+str(y+1+2))
                        if x > 0 and Pelitilanne[y+1][x-1] not in omat and Pelitilanne[y+1][x-1] != "-":
                            siirrot.append(chr(x+97)+str(y+1)+chr(x+96)+str(y+1+1))
                        if x < 7 and Pelitilanne[y+1][x+1] not in omat and Pelitilanne[y+1][x+1] != "-":
                            siirrot.append(chr(x+97)+str(y+1)+chr(x+98)+str(y+1+1))
            elif pelinappula == omat[1]:
                #r tai R
                for i in range(x+1, 7):
                    if Pelitilanne[y][i] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(i+97)+str(y+1))
                    elif Pelitilanne[y][i] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(i+97)+str(y+1))
                        break
                    elif Pelitilanne[y][i] in omat:
                        break
                for i in range(x-1, -1,-1):
                    if Pelitilanne[y][i] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(i+97)+str(y+1))
                    elif Pelitilanne[y][i] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(i+97)+str(y+1))
                        break
                    elif Pelitilanne[y][i] in omat:
                        break
                for i in range(y+1, 7):
                    if Pelitilanne[i][x] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97)+str(i+1))
                    elif Pelitilanne[i][x] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97)+str(i+1))
                        break
                    elif Pelitilanne[i][x] in omat:
                        break
                for i in range(y-1, -1,-1):
                    if Pelitilanne[i][x] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97)+str(i+1))
                    elif Pelitilanne[i][x] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97)+str(i+1))
                        break
                    elif Pelitilanne[i][x] in omat:
                        break
            elif pelinappula == omat[2]:
                #h tai H
                if y < 6 and x < 7 and Pelitilanne[y+2][x+1] not in omat:
                    siirrot.append(chr(x+97)+str(y+1)+chr(x+98)+str(y+1+2))
                if y < 6 and x > 0 and Pelitilanne[y+2][x-1] not in omat:
                    siirrot.append(chr(x+97)+str(y+1)+chr(x+96)+str(y+1+2))
                if y > 1 and x < 7 and Pelitilanne[y-2][x+1] not in omat:
                    siirrot.append(chr(x+97)+str(y+1)+chr(x+98)+str(y+1-2))
                if y > 1 and x > 0 and Pelitilanne[y-2][x-1] not in omat:
                    siirrot.append(chr(x+97)+str(y+1)+chr(x+96)+str(y+1-2))
                if y < 7 and x < 6 and Pelitilanne[y+1][x+2] not in omat:
                    siirrot.append(chr(x+97)+str(y+1)+chr(x+99)+str(y+1+1))
                if y < 7 and x > 1 and Pelitilanne[y+1][x-2] not in omat:
                    siirrot.append(chr(x+97)+str(y+1)+chr(x+95)+str(y+1+1))
                if y > 0 and x < 6 and Pelitilanne[y-1][x+2] not in omat:
                    siirrot.append(chr(x+97)+str(y+1)+chr(x+99)+str(y+1-1))
                if y > 0 and x > 1 and Pelitilanne[y-1][x-2] not in omat:
                    siirrot.append(chr(x+97)+str(y+1)+chr(x+95)+str(y+1-1))
            elif pelinappula == omat[3]:
                #b tai B
                for i in range(1,9):
                    if x+i > 7 or y+i > 7 or Pelitilanne[y+i][x+i] in omat:
                        break
                    if Pelitilanne[y+i][x+i] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97+i)+str(y+1+i))
                    elif Pelitilanne[y+i][x+i] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97+i)+str(y+1+i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y+i > 7 or Pelitilanne[y+i][x-i] in omat:
                        break
                    if Pelitilanne[y+i][x-i] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97-i)+str(y+1+i))
                    elif Pelitilanne[y+i][x-i] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97-i)+str(y+1+i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y-i < 0 or Pelitilanne[y-i][x+i] in omat:
                        break
                    if Pelitilanne[y-i][x+i] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97+i)+str(y+1-i))
                    elif Pelitilanne[y-i][x+i] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97+i)+str(y+1-i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y-i < 0 or Pelitilanne[y-i][x-i] in omat:
                        break
                    if Pelitilanne[y-i][x-i] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97-i)+str(y+1-i))
                    elif Pelitilanne[y-i][x-i] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97-i)+str(y+1-i))
                        break
            elif pelinappula == omat[4]:
                #q tai Q
                for i in range(x+1, 7):
                    if Pelitilanne[y][i] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(i+97)+str(y+1))
                    elif Pelitilanne[y][i] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(i+97)+str(y+1))
                        break
                    elif Pelitilanne[y][i] in omat:
                        break
                for i in range(x-1, -1,-1):
                    if Pelitilanne[y][i] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(i+97)+str(y+1))
                    elif Pelitilanne[y][i] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(i+97)+str(y+1))
                        break
                    elif Pelitilanne[y][i] in omat:
                        break
                for i in range(y+1, 7):
                    if Pelitilanne[i][x] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97)+str(i+1))
                    elif Pelitilanne[i][x] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97)+str(i+1))
                        break
                    elif Pelitilanne[i][x] in omat:
                        break
                for i in range(y-1, -1,-1):
                    if Pelitilanne[i][x] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97)+str(i+1))
                    elif Pelitilanne[i][x] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97)+str(i+1))
                        break
                    elif Pelitilanne[i][x] in omat:
                        break
                for i in range(1,9):
                    if x+i > 7 or y+i > 7 or Pelitilanne[y+i][x+i] in omat:
                        break
                    if Pelitilanne[y+i][x+i] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97+i)+str(y+1+i))
                    elif Pelitilanne[y+i][x+i] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97+i)+str(y+1+i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y+i > 7 or Pelitilanne[y+i][x-i] in omat:
                        break
                    if Pelitilanne[y+i][x-i] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97-i)+str(y+1+i))
                    elif Pelitilanne[y+i][x-i] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97-i)+str(y+1+i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y-i < 0 or Pelitilanne[y-i][x+i] in omat:
                        break
                    if Pelitilanne[y-i][x+i] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97+i)+str(y+1-i))
                    elif Pelitilanne[y-i][x+i] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97+i)+str(y+1-i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y-i < 0 or Pelitilanne[y-i][x-i] in omat:
                        break
                    if Pelitilanne[y-i][x-i] == "-":
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97-i)+str(y+1-i))
                    elif Pelitilanne[y-i][x-i] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97-i)+str(y+1-i))
                        break
            elif pelinappula == omat[5]:
                #k tai K
                #automaatin ei tarvitse estää shakkimattia, sillä pelajaankin siirrot lasketaan optimaalisesti, eli sellaista siirtoa ei pelata/arvioida
                #Muuten tarvitsisi tarkistaa mihin kaikki nappulat voi liikkua
                if automaatti:
                    if x < 7 and Pelitilanne[y][x+1] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+98)+str(y+1))
                    if x > 0 and Pelitilanne[y][x-1] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+96)+str(y+1))
                    if y < 7 and Pelitilanne[y+1][x] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97)+str(y+1+1))
                    if y > 1 and Pelitilanne[y-1][x] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+97)+str(y+1-1))
                    if y < 7 and x < 7 and Pelitilanne[y+1][x+1] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+98)+str(y+1+1))
                    if y < 7 and x > 0 and Pelitilanne[y+1][x-1] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+96)+str(y+1+1))
                    if y > 0 and x < 7 and Pelitilanne[y-1][x+1] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+98)+str(y+1-1))
                    if y > 0 and x > 0 and Pelitilanne[y-1][x-1] not in omat:
                        siirrot.append(chr(x+97)+str(y+1)+chr(x+96)+str(y+1-1))
                else:
                    valiaika = []
                    if x < 7 and Pelitilanne[y][x+1] not in omat:
                        valiaika.append(chr(x+97)+str(y+1)+chr(x+98)+str(y+1))
                    if x > 0 and Pelitilanne[y][x-1] not in omat:
                        valiaika.append(chr(x+97)+str(y+1)+chr(x+96)+str(y+1))
                    if y < 7 and Pelitilanne[y+1][x] not in omat:
                        valiaika.append(chr(x+97)+str(y+1)+chr(x+97)+str(y+1+1))
                    if y > 1 and Pelitilanne[y-1][x] not in omat:
                        valiaika.append(chr(x+97)+str(y+1)+chr(x+97)+str(y+1-1))
                    if y < 7 and x < 7 and Pelitilanne[y+1][x+1] not in omat:
                        valiaika.append(chr(x+97)+str(y+1)+chr(x+98)+str(y+1+1))
                    if y < 7 and x > 0 and Pelitilanne[y+1][x-1] not in omat:
                        valiaika.append(chr(x+97)+str(y+1)+chr(x+96)+str(y+1+1))
                    if y > 0 and x < 7 and Pelitilanne[y-1][x+1] not in omat:
                        valiaika.append(chr(x+97)+str(y+1)+chr(x+98)+str(y+1-1))
                    if y > 0 and x > 0 and Pelitilanne[y-1][x-1] not in omat:
                        valiaika.append(chr(x+97)+str(y+1)+chr(x+96)+str(y+1-1))
                    if vuoro == 0:
                        vastapuoli = kaikki_lailliset_siirrot(Pelitilanne, 1, True)
                    else:
                        vastapuoli = kaikki_lailliset_siirrot(Pelitilanne, 0, True)
                    for siirto in vastapuoli:
                        if siirto[2:] in valiaika:
                            valiaika.remove(siirto[2:])
    return siirrot

def yksinpeli():
    return

alku()