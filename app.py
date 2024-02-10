#ns config asetukset, tästä voi pääasiassa vain aloitusvuoron vaihtaa, uusien nappuloidne tai pelilaudan koon vaihtaminen tässä versiossa rikkoo pelin
Pelilauta = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
            [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
            [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
pelinappulat = [[chr(9817),chr(9814),chr(9816),chr(9815),chr(9813),chr(9812)],[chr(9823),chr(9820),chr(9822),chr(9821),chr(9819),chr(9818)]]

alkuvuoro = 0 #kaksinpelissä kumpi puoli aloittaa
laskenta_syvyys = 3 #Kuinka kauas tekoäly laskee siirtoja
aly = False #Käytetäänkö tekoalya(), jos ei niin tekoalyb(). a harkitsee pienemmän määrän siirtoja, mutta b laskee nopeammin

#!!! Puuttuu vielä mahdolliset erikoisliikkeet, koodin laadun tarkistaminen, yksikkötestaaminen ja tietenkin itse shakkibotti

def alku():
    """Funktion kutsuminen käynnistää sovelluksen. Funktio kutsuu kaksin tai yksinpeliin liittyvän funktion.
    """
    print("Pelistä voi poistua kirjoittamalla quit")
    print("Peli ei tunnista minkään näköisiä erikoissiirtoja")
    print("En tiedä miksi, mutta värit ovat väärinpäin eikä ole aikaa vaihtaa")
    print("Tekoälyä vastaan pelatessa voi hetkellä vain pelaaja aloittaa")
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
    """Ainoa toimiva pelimuoto, missä kaksi pelaajaa pelaa toisiaan vastaan. Tämä funktio vain vaihtaa vuoroja ja tulostaa pelilaudan tilanteen

    Returns:
        String: voi palauttaa vain 'quit' jolloin pelin suoritus pysähtyy. Jos mitään ei palauteta niin peli jatkuu
    """
    vuoro = alkuvuoro
    Pelitilanne = []
    for rivi in Pelilauta:
        Pelitilanne.append(rivi[:])
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
        if False:
            if aly == True:
                siirto = tekoalya(Pelitilanne, laskenta_syvyys, -50000, 50000, vuoro, (0, ""), vuoro)
            else:
                siirto = tekoalyb(Pelitilanne, laskenta_syvyys, -50000, 50000, vuoro, vuoro)
            print("Pelitilanne arvio: ", siirto[0]/100)
            temp2 = round((siirto[0] + 50000)/5000)
            print(chr(9633)*temp2 + chr(9632)*(10-temp2))
        arvio = arvioi_tilanne(Pelitilanne, [], vuoro)
        print("Pelikenttä arvio: ", arvio/100)
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
        if siirto == "quit" or siirto == "q":
            return "quit"
        if siirto in tilanne[1]:
            tee_siirto(Pelitilanne, siirto)
            if vuoro == 1:
                vuoro = 0
            else:
                vuoro = 1
        else:
            print("Laiton siirto")

def matti(Pelitilanne, vuoro):
    """Funktio päättelee pelitilanteen ja vuoron pohjalta 'onko_shakki' funktiota hyödyntäen pitäisikö pelin loppua.

    Args:
        Pelitilanne List: Pelilauta tapainen lista joka edustaa hetkistä pelitilannetta
        vuoro int: joko 0 jolloin on pieniä kirjaimia edustavan pelaajan vuoro ja 1 jos toisen pelaajan.

    Returns:
        Boolean: palauttaa True jos peli on loppunut ja False jos ei
    """
    mahdolliset = kone_kaikki_siirrot(Pelitilanne, vuoro)
    uusittu = []
    for siirto in mahdolliset:
        poistettu = kone_siirto(Pelitilanne, siirto)
        if not onko_shakki(Pelitilanne, vuoro):
            uusittu.append(siirto)
        kone_peru(Pelitilanne, siirto, poistettu)
    if len(uusittu) == 0:
        return True, uusittu
    else:
        lopullinen = []
        for siirto in uusittu:
            lopullinen.append(chr(siirto[0]+97) + str(siirto[1]+1) + chr(siirto[2]+97) + str(siirto[3]+1))
        return False, lopullinen
    
def tee_siirto(Pelitilanne, siirto):
    """Yksinkertaisesti siirtää jotain pelinappulaa

    Args:
        Pelitilanne list: Pelilauta tapainen listojen lista hetkisestä pelitilanteesta
        siirto string: Pelaajan tekemä siirto

    Returns:
        string: siirrettyyn ruutuun sisältävä pelinappula, tyhjään ruutuun siirtyessä siis esim. '-'
    """
    mista_x = ord(siirto[0])-97
    mista_y = int(siirto[1])-1
    mihin_x = ord(siirto[2])-97
    mihin_y = int(siirto[3])-1
    poistettu = Pelitilanne[mihin_y][mihin_x]
    Pelitilanne[mihin_y][mihin_x] = Pelitilanne[mista_y][mista_x]
    Pelitilanne[mista_y][mista_x] = "-"
    return poistettu

def kone_siirto(Pelitilanne, siirto):
    """Sama kuin 'tee_siirto' käyttäen 'kone_kaikki_siirrot' siirtoja

    Args:
        Pelitilanne list: Pelilauta tapainen listojen lista hetkisestä pelitilanteesta
        siirto string: Pelaajan tekemä siirto

    Returns:
        string: siirrettyyn ruutuun sisältävä pelinappula, tyhjään ruutuun siirtyessä siis esim. '-'
    """
    poistettu = Pelitilanne[siirto[3]][siirto[2]]
    Pelitilanne[siirto[3]][siirto[2]] = Pelitilanne[siirto[1]][siirto[0]]
    Pelitilanne[siirto[1]][siirto[0]] = "-"
    return poistettu

def kone_peru(Pelitilanne, siirto, nappula):
    """Palauttaa siirron tekemät muutokset

    Args:
        Pelitilanne list: Pelilauta tapainen listojen lista hetkisestä pelitilanteesta
        siirto string: Siirto jonka perutaan
        nappula string: Nappula joka ruudun paikalla ennen oli, esim. tyhjän ruudun ollessa '-'
    """
    Pelitilanne[siirto[1]][siirto[0]] = Pelitilanne[siirto[3]][siirto[2]]
    Pelitilanne[siirto[3]][siirto[2]] = nappula

def onko_shakki(Pelitilanne, vuoro):
    """Tarkistaa onko shakki, eli voiko vuorossa olevan pelaajan kuninkaan ruutuun hyökätä millään 
    vastustajan napilla

    Args:
        Pelitilanne list: Pelilauta tapainen listojen lista hetkisestä pelitilanteesta
        vuoro int: kenen vuoro, 0 tai 1 arvona

    Returns:
        boolean: True jos on shakki, False jos ei ole
    """
    kingi = pelinappulat[vuoro][5]
    if vuoro == 0:
        vastapuoli = kone_kaikki_siirrot(Pelitilanne, 1)
    else:
        vastapuoli = kone_kaikki_siirrot(Pelitilanne, 0)
    for y in range(8):
        for x in range(8):
            if Pelitilanne[y][x] == kingi:
                sijainti = (x,y)
    for siirto in vastapuoli:
        if siirto[2] == sijainti[0] and siirto[3] == sijainti[1]:
            return True
    return False

def arvioi_tilanne(Pelitilanne, siirrot=[], vuoro=0):
    """Funktio arvioimaan pelitilannetta, funktio on kevyt ja palauttaa siis vain tämän hetkisen pelitilanteen arvion, eli ei osaa mm. ennustaa shakkia. 
    Funktio on hetkellä myös aika yksinkertainen, se ottaa huomioon vain materiaalin, mahdollisten siirtojen ja huonossa asemassa olevien sotilaiden määrät.

    Args:
        Pelitilanne list: Pelilauta tapainen listojen lista hetkisestä pelitilanteesta
        siirrot (list, optional): Jos tekoäly haluaa arvion niin se on jo laskenut oman tilanteen mahdolliset siirrot jotka löytyy tästä. Defaults to [].
        vuoro (int, optional): Kenen vuorolla tekoäly arvioi. Defaults to 0.

    Returns:
        int: palauttaa arvion pelitilanteesta, plussaa jos pienillä kirjaimilla on voittamassa, miinusta jos häviämässä. 
    """
    materiaalipaino = 1
    sotilaspaino = 0.5
    siirtojapaino = 10
    kuninkaan_uhka_paino = 1
    doubled_p = set()
    doubled_P = set()
    isolated_p = 0
    isolated_P = 0
    blocked_p = 0
    blocked_P = 0
    advancing_p = 0
    advancing_P = 0
    kuninkaan_uhka_p = 0
    kuninkaan_uhka_P = 0
    materiaali = 0
    if len(siirrot) == 0:
        siirrotp = kone_kaikki_siirrot(Pelitilanne, 0)
        siirrotP = kone_kaikki_siirrot(Pelitilanne, 1)
    else:
        if vuoro == 0:
            siirrotp = siirrot
            siirrotP = kone_kaikki_siirrot(Pelitilanne, 1)
        else:
            siirrotp = kone_kaikki_siirrot(Pelitilanne, 0)
            siirrotP = siirrot
    for x in range(8):
        for y in range(8):
            if Pelitilanne[y][x] == "-":
                continue
            elif Pelitilanne[y][x] == chr(9817):
                materiaali += 100
                doubled_p.add(x)
                if not ((x > 0 and Pelitilanne[y-1][x-1] == chr(9817)) or (x < 7 and Pelitilanne[y-1][x+1] == chr(9817))):
                    isolated_p += 100
                if y < 7 and Pelitilanne[y+1][x] != "-":
                    blocked_p += 100
                advancing_p += 10*(6-y)-abs(10*x-35)
            elif Pelitilanne[y][x] == chr(9823):
                materiaali -= 100
                doubled_P.add(x)
                if not ((x > 0 and Pelitilanne[y-1][x-1] == chr(9823)) or (x < 7 and Pelitilanne[y-1][x+1] == chr(9823))):
                    isolated_P += 100
                if y > 0 and Pelitilanne[y-1][x] != "-":
                    blocked_P += 100
                advancing_P += 10*(y-1)-abs(10*x-35)
            elif Pelitilanne[y][x] == chr(9815):
                materiaali += 300
            elif Pelitilanne[y][x] == chr(9821):
                materiaali -= 300
            elif Pelitilanne[y][x] == chr(9816):
                materiaali += 300
            elif Pelitilanne[y][x] == chr(9822):
                materiaali -= 300
            elif Pelitilanne[y][x] == chr(9814):
                materiaali += 500
            elif Pelitilanne[y][x] == chr(9820):
                materiaali -= 500
            elif Pelitilanne[y][x] == chr(9813):
                materiaali += 900
            elif Pelitilanne[y][x] == chr(9819):
                materiaali -= 900
            elif Pelitilanne[y][x] == chr(9812):
                materiaali += 20000
                for siirto in siirrotP:
                    if siirto[2] == x and siirto[3] == y:
                        kuninkaan_uhka_p += 100
            elif Pelitilanne[y][x] == chr(9818):
                materiaali -= 20000
                for siirto in siirrotp:
                    if siirto[2] == x and siirto[3] == y:
                        kuninkaan_uhka_P += 100
    arvio = materiaali*materiaalipaino 
    arvio -= (len(doubled_P)*100-len(doubled_p)*100+isolated_P-isolated_P+blocked_p-blocked_p+(advancing_p-advancing_P))*sotilaspaino
    arvio += (len(siirrotp)-len(siirrotP))*siirtojapaino
    arvio -= (kuninkaan_uhka_P-kuninkaan_uhka_p)*kuninkaan_uhka_paino
    return arvio

def kone_kaikki_siirrot(Pelitilanne, vuoro):
    """Sama kuin kaikki_lailliset_siirrot mutta suoraviivaisempi ja ehkä vähän epäselvempi.

    Args:
        Pelitilanne list: Pelilauta tapainen listojen lista hetkisestä pelitilanteesta
        vuoro int: kenen vuoro, 0 tai 1 arvona
        
    Returns:
        list : lista kaikista laillisista siirroista. Siirrot muodossa '(3,6,3,4)' vastaa siirtoa 'd7d5'.
    """
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
                            siirrot.append((x,y,x,y-1))
                            if y == 6 and Pelitilanne[y-2][x] == "-":
                                siirrot.append((x,y,x,y-2))
                        if x > 0 and Pelitilanne[y-1][x-1] not in omat and Pelitilanne[y-1][x-1] != "-":
                            siirrot.append((x,y,x-1,y-1))
                        if x < 7 and Pelitilanne[y-1][x+1] not in omat and Pelitilanne[y-1][x+1] != "-":
                            siirrot.append((x,y,x+1,y-1))
                else:
                    if y < 7:
                        if Pelitilanne[y+1][x] == "-":
                            siirrot.append((x,y,x,y+1))
                            if y == 1 and Pelitilanne[y+2][x] == "-":
                                siirrot.append((x,y,x,y+2))
                        if x > 0 and Pelitilanne[y+1][x-1] not in omat and Pelitilanne[y+1][x-1] != "-":
                            siirrot.append((x,y,x-1,y+1))
                        if x < 7 and Pelitilanne[y+1][x+1] not in omat and Pelitilanne[y+1][x+1] != "-":
                            siirrot.append((x,y,x+1,y+1))
            elif pelinappula == omat[1]:
                #r tai R
                for i in range(x+1, 8):
                    if Pelitilanne[y][i] == "-":
                        siirrot.append((x,y,i,y))
                    elif Pelitilanne[y][i] in omat:
                        break
                    else:
                        siirrot.append((x,y,i,y))
                        break
                for i in range(x-1, -1,-1):
                    if Pelitilanne[y][i] == "-":
                        siirrot.append((x,y,i,y))
                    elif Pelitilanne[y][i] in omat:
                        break
                    else:
                        siirrot.append((x,y,i,y))
                        break
                for i in range(y+1, 8):
                    if Pelitilanne[i][x] == "-":
                        siirrot.append((x,y,x,i))
                    elif Pelitilanne[i][x] in omat:
                        break
                    else:
                        siirrot.append((x,y,x,i))
                        break
                for i in range(y-1, -1,-1):
                    if Pelitilanne[i][x] == "-":
                        siirrot.append((x,y,x,i))
                    elif Pelitilanne[i][x] in omat:
                        break
                    else:
                        siirrot.append((x,y,x,i))
                        break
            elif pelinappula == omat[2]:
                #h tai H
                if y < 6 and x < 7 and Pelitilanne[y+2][x+1] not in omat:
                    siirrot.append((x,y,x+1,y+2))
                if y < 6 and x > 0 and Pelitilanne[y+2][x-1] not in omat:
                    siirrot.append((x,y,x-1,y+2))
                if y > 1 and x < 7 and Pelitilanne[y-2][x+1] not in omat:
                    siirrot.append((x,y,x+1,y-2))
                if y > 1 and x > 0 and Pelitilanne[y-2][x-1] not in omat:
                    siirrot.append((x,y,x-1,y-2))
                if y < 7 and x < 6 and Pelitilanne[y+1][x+2] not in omat:
                    siirrot.append((x,y,x+2,y+1))
                if y < 7 and x > 1 and Pelitilanne[y+1][x-2] not in omat:
                    siirrot.append((x,y,x-2,y+1))
                if y > 0 and x < 6 and Pelitilanne[y-1][x+2] not in omat:
                    siirrot.append((x,y,x+2,y-1))
                if y > 0 and x > 1 and Pelitilanne[y-1][x-2] not in omat:
                    siirrot.append((x,y,x-2,y-1))
            elif pelinappula == omat[3]:
                #b tai B
                for i in range(1,9):
                    if x+i > 7 or y+i > 7 or Pelitilanne[y+i][x+i] in omat:
                        break
                    if Pelitilanne[y+i][x+i] == "-":
                        siirrot.append((x,y,x+i,y+i))
                    else:
                        siirrot.append((x,y,x+i,y+i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y+i > 7 or Pelitilanne[y+i][x-i] in omat:
                        break
                    if Pelitilanne[y+i][x-i] == "-":
                        siirrot.append((x,y,x-i,y+i))
                    else:
                        siirrot.append((x,y,x-i,y+i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y-i < 0 or Pelitilanne[y-i][x+i] in omat:
                        break
                    if Pelitilanne[y-i][x+i] == "-":
                        siirrot.append((x,y,x+i,y-i))
                    else:
                        siirrot.append((x,y,x+i,y-i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y-i < 0 or Pelitilanne[y-i][x-i] in omat:
                        break
                    if Pelitilanne[y-i][x-i] == "-":
                        siirrot.append((x,y,x-i,y-i))
                    else:
                        siirrot.append((x,y,x-i,y-i))
                        break
            elif pelinappula == omat[4]:
                #q tai Q
                for i in range(x+1, 8):
                    if Pelitilanne[y][i] == "-":
                        siirrot.append((x,y,i,y))
                    elif Pelitilanne[y][i] in omat:
                        break
                    else:
                        siirrot.append((x,y,i,y))
                        break
                for i in range(x-1, -1,-1):
                    if Pelitilanne[y][i] == "-":
                        siirrot.append((x,y,i,y))
                    elif Pelitilanne[y][i] in omat:
                        break
                    else:
                        siirrot.append((x,y,i,y))
                        break
                for i in range(y+1, 8):
                    if Pelitilanne[i][x] == "-":
                        siirrot.append((x,y,x,i))
                    elif Pelitilanne[i][x] in omat:
                        break
                    else:
                        siirrot.append((x,y,x,i))
                        break
                for i in range(y-1, -1,-1):
                    if Pelitilanne[i][x] == "-":
                        siirrot.append((x,y,x,i))
                    elif Pelitilanne[i][x] in omat:
                        break
                    else:
                        siirrot.append((x,y,x,i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y+i > 7 or Pelitilanne[y+i][x+i] in omat:
                        break
                    if Pelitilanne[y+i][x+i] == "-":
                        siirrot.append((x,y,x+i,y+i))
                    else:
                        siirrot.append((x,y,x+i,y+i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y+i > 7 or Pelitilanne[y+i][x-i] in omat:
                        break
                    if Pelitilanne[y+i][x-i] == "-":
                        siirrot.append((x,y,x-i,y+i))
                    else:
                        siirrot.append((x,y,x-i,y+i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y-i < 0 or Pelitilanne[y-i][x+i] in omat:
                        break
                    if Pelitilanne[y-i][x+i] == "-":
                        siirrot.append((x,y,x+i,y-i))
                    else:
                        siirrot.append((x,y,x+i,y-i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y-i < 0 or Pelitilanne[y-i][x-i] in omat:
                        break
                    if Pelitilanne[y-i][x-i] == "-":
                        siirrot.append((x,y,x-i,y-i))
                    else:
                        siirrot.append((x,y,x-i,y-i))
                        break
            elif pelinappula == omat[5]:
                #k tai K
                if x < 7 and Pelitilanne[y][x+1] not in omat:
                    siirrot.append((x,y,x+1,y))
                if x > 0 and Pelitilanne[y][x-1] not in omat:
                    siirrot.append((x,y,x-1,y))
                if y < 7 and Pelitilanne[y+1][x] not in omat:
                    siirrot.append((x,y,x,y+1))
                if y > 1 and Pelitilanne[y-1][x] not in omat:
                    siirrot.append((x,y,x,y-1))
                if y < 7 and x < 7 and Pelitilanne[y+1][x+1] not in omat:
                    siirrot.append((x,y,x+1,y+1))
                if y < 7 and x > 0 and Pelitilanne[y+1][x-1] not in omat:
                    siirrot.append((x,y,x-1,y+1))
                if y > 0 and x < 7 and Pelitilanne[y-1][x+1] not in omat:
                    siirrot.append((x,y,x+1,y-1))
                if y > 0 and x > 0 and Pelitilanne[y-1][x-1] not in omat:
                    siirrot.append((x,y,x-1,y-1))
    return siirrot

def yksinpeli():
    """Yksinpeli shakkibottia vastaan, en tiedä toimiiko hyvin ollenkaan

    Returns:
        string: palauttaa 'quit' jos se jossain kohtaa konsoliin vastataan
    """
    vuoro = alkuvuoro
    Pelitilanne = []
    for rivi in Pelilauta:
        Pelitilanne.append(rivi[:])
    while True:
        pelaaja = 0
        aly_vuoro = 1
        break
        valinta = input("Aloittaako pelaaja [y] vai ei [n]? ")
        if valinta == "quit" or valinta == "q":
            return "quit"
        elif valinta == "y" or valinta == "Y":
            pelaaja = 0
            aly_vuoro = 1
            break
        elif valinta == "n" or valinta == "N":
            pelaaja = 1
            aly_vuoro = 0
            break
    siirto = (0, "")
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

        arvio = arvioi_tilanne(Pelitilanne, [], vuoro)
        print("Pelikenttä arvio: ", arvio/100)

        print("Pelaajan", vuoro+1, "vuoro")
        tilanne = matti(Pelitilanne, vuoro)
        if tilanne[0]:
            print()
            if vuoro == 0:
                print("Tekoäly voitti!!!")
            else:
                print("Pelaaja voitti!!!")
            print()
            return
        else:
            print("mahdolliset siirrot ", tilanne[1])
        if vuoro == pelaaja:
            siirtop = input("Syötä siirto: ")
            if siirtop == "quit" or siirtop == "q":
                return "quit"
            if siirtop in tilanne[1]:
                tee_siirto(Pelitilanne, siirtop)
                if vuoro == 1:
                    vuoro = 0
                else:
                    vuoro = 1
            else:
                print("Laiton siirto")
        else:
            print()
            print("miettii.....")
            if aly == True:
                siirto = tekoalya(Pelitilanne, laskenta_syvyys, -50000, 50000, aly_vuoro, (0, ""), aly_vuoro)
            else:
                siirto = tekoalyb(Pelitilanne, laskenta_syvyys, -50000, 50000, aly_vuoro, aly_vuoro)
            oikea_muoto = chr(siirto[1][0]+97) + str(siirto[1][1]+1) + chr(siirto[1][2]+97) + str(siirto[1][3]+1)
            print("Valmis! siirto; ", siirto)
            if oikea_muoto in tilanne[1]:
                tee_siirto(Pelitilanne, oikea_muoto)
                if vuoro == 1:
                    vuoro = 0
                else:
                    vuoro = 1
            else:
                print("Tekoäly rikki!!! Sori, laita palautetta jossain jotenkin, mieluusti pelitilanteen kera")
                return "quit"


def tekoalya(Pelitilanne, syvyys, alpha, beta, vuoro, edellinen_siirto, ekavuoro):
    """Rekursiivinen funktio laskemaan paras siirto kun tekoälyn siirrolla tilanteen arvo maksimoidaan ja pelaajan vuorolla minimoidaan (shakkibotin suhteen).
    Eroaa toisesta tekoäly funktiosta sillä että laskee mahdollisten siirtojen arvot ensin, jolloin todennäköisesti karsitaan enemmän siirtoja ja ehkä arviointi on
    nopeampaa.

    Args:
        Pelitilanne list: Pelilauta tapainen listojen lista hetkisestä pelitilanteesta
        syvyys int: funktion laskentasyvyys, peliä ei tietenkään keretä loppuun asti laskemaan, joten näin monen siirron jälkeen lopetetaan
        alpha int: arvo jonka mukaan karsitaan vissiin pelaajalle epäotimaaliset siirrot
        beta int: arvo jolla karsitaan vissiin tekoälylle epäoptimaaliset siirrot 
        vuoro int: kenen vuoro, 0 tai 1 arvona
        edellinen_siirto tuple(int, string): sisältää edellisen (tähän pelitilanteeseen päästävän) siirron ja sille lasketun arvon

    Returns:
        tuple(int, string): palauttaa tuplen joka kuvailee parasta siirtoa ja sen arvoa
    """
    if syvyys == 0:
        return edellinen_siirto
    siirrot = kone_kaikki_siirrot(Pelitilanne, vuoro)
    arviot = []
    if False:
        for siirto in siirrot:
            nappula = kone_siirto(Pelitilanne, siirto)
            arviot.append((arvioi_tilanne(Pelitilanne, siirrot, vuoro), siirto))
            kone_peru(Pelitilanne, siirto, nappula)
    else:
        for siirto in siirrot:
            nappula = kone_siirto(Pelitilanne, siirto)
            arviot.append((arvioi_tilanne(Pelitilanne, siirrot, vuoro)*(-1), siirto))
            kone_peru(Pelitilanne, siirto, nappula)
    if vuoro == 1:
        arviot.sort(reverse=True)
        arvo = (-30000,"")
        for siirto in arviot:
            nappula = kone_siirto(Pelitilanne, siirto[1])
            temp = tekoalya(Pelitilanne, syvyys-1, alpha, beta, 0, (siirto[0], siirto[1]), ekavuoro)
            kone_peru(Pelitilanne, siirto[1], nappula)
            if temp[0] > arvo[0]:
                arvo = (temp[0], siirto[1])
            alpha = max(arvo[0], alpha)
            if arvo[0] >= beta:
                break
        return arvo
    else:
        arviot.sort()
        arvo = (30000, "")
        for siirto in arviot:
            nappula = kone_siirto(Pelitilanne, siirto[1])
            temp = tekoalya(Pelitilanne, syvyys-1, alpha, beta, 0, (siirto[0], siirto[1]), ekavuoro)
            if temp[0] < arvo[0]:
                arvo = (temp[0], siirto[1])
            kone_peru(Pelitilanne, siirto[1], nappula)
            beta = max(arvo[0], beta)
            if arvo[0] <= alpha:
                break
        return arvo
    
def tekoalyb(Pelitilanne, syvyys, alpha, beta, vuoro, ekavuoro):
    """Yksinkertaisempi versio toisesta tekoälystä, huonompi karsimaan valintoja, mutta nopeampi laskemaan, sillä vain siirtojen ketjun lopussa oleva tilanne arvioidaan

    Args:
        samat kuin edellisessä, vain 'edellinen_siirto' puuttuu

    Returns:
        tuple(int, string): palauttaa tuplen joka kuvailee parasta siirtoa ja sen arvoa
    """
    if syvyys == 0:
        return arvioi_tilanne(Pelitilanne, [], vuoro)*(-1), ""
        if ekavuoro == 0:
            return arvioi_tilanne(Pelitilanne, [], vuoro), ""
        else:
            return arvioi_tilanne(Pelitilanne, [], vuoro)*(-1), ""
    siirrot = kone_kaikki_siirrot(Pelitilanne, vuoro)
    if vuoro == 1:
        arvo = (-30000,"")
        for siirto in siirrot:
            nappula = kone_siirto(Pelitilanne, siirto)
            temp = tekoalyb(Pelitilanne, syvyys-1, alpha, beta, 0, ekavuoro)
            kone_peru(Pelitilanne, siirto, nappula)
            if temp[0] > arvo[0]:
                arvo = (temp[0], siirto)
            alpha = max(arvo[0], alpha)
            if arvo[0] > beta:
                break
        return arvo
    else:
        arvo = (30000, "")
        for siirto in siirrot:
            nappula = kone_siirto(Pelitilanne, siirto)
            temp = tekoalyb(Pelitilanne, syvyys-1, alpha, beta, 1, ekavuoro)
            kone_peru(Pelitilanne, siirto, nappula)
            if temp[0] < arvo[0]:
                arvo = (temp[0], siirto)
            beta = max(arvo[0], beta)
            if arvo[0] < alpha:
                break
        return arvo


### Vanhat funktiot tallella varmuuden vuoksi


def laillinen_siirto(Pelitilanne, siirto, vuoro):
    """Otettu pois käytöstä!
    Vanha kuvaus:
    Tarkistaa syötetyn siirron. Oikean muodon lisäksi, siirron pitää olla mahdollista suorittaa kyseisellä 
    pelinappulalla (tarkistus kaikki_lailliset_siirrot funktion listaa vastaan) ja jos on shakissa niin siirron
    pitää pistää pois shakista.

    Args:
        Pelitilanne list: Pelilauta tapainen listojen lista hetkisestä pelitilanteesta
        siirto string: Siirron pitää olla muotoa alku x, alku y, loppu x, loppu y, eli esim. 'd7d5'. Pitää myös poistua mahdollisesta shakista
        vuoro int: kenen vuoro, 0 tai 1 arvona

    Returns:
        boolean: true vai false onko laillinen siirto
    """
    if siirto[0] not in ("a",chr(9815),"c","d","e","f","g",chr(9816)) or siirto[2] not in ("a",chr(9815),"c","d","e","f","g",chr(9816)):
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

def kaikki_lailliset_siirrot(Pelitilanne, vuoro, automaatti):
    """Otettu pois käytöstä
    Vanha kuvaus:
    Pelin toiminnallisuuden tärkein funktio, laskee listaan kaikki vuorossa olevan pelaajan 'mahdolliset' siirrot.
    Funktio ei kuitenkaan huomioi shakki tilannetta, joka tarkistetaan 'laillinen_siirto' funktiolla. Tämän funktion
    takia myöskään pelilaudan kokoa ei voi muuttaa sillä laudan rajat on hetkellä kovakoodattu siirtoihin.

    Args:
        Pelitilanne list: Pelilauta tapainen listojen lista hetkisestä pelitilanteesta
        vuoro int: kenen vuoro, 0 tai 1 arvona
        automaatti boolean: True jos lasketaan shakkibotille, False muuten. Nopeampi laskenta joka ei pitäisi shakkibotin toimintaa haitata.

    Returns:
        list : lista kaikista laillisista siirroista. Siirrot muodossa 'd7d5'. Tämä saattaa muuttua jos tarvitsen lisätehoa shakkibotin laskentaan
    """
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
                for i in range(x+1, 8):
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
                for i in range(y+1, 8):
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
                for i in range(x+1, 8):
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
                for i in range(y+1, 8):
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

def peru_siirto(Pelitilanne, siirto, nappula):
    """Otettu pois käytöstä!
    Vanha kuvaus:
    Palauttaa siirron tekemät muutokset

    Args:
        Pelitilanne list: Pelilauta tapainen listojen lista hetkisestä pelitilanteesta
        siirto string: Siirto jonka perutaan
        nappula string: Nappula joka ruudun paikalla ennen oli, esim. tyhjän ruudun ollessa '-'
    """
    mista_x = ord(siirto[0])-97
    mista_y = int(siirto[1])-1
    mihin_x = ord(siirto[2])-97
    mihin_y = int(siirto[3])-1
    Pelitilanne[mista_y][mista_x] = Pelitilanne[mihin_y][mihin_x]
    Pelitilanne[mihin_y][mihin_x] = nappula

if __name__ == "__main__":
    alku()