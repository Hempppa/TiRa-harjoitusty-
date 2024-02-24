"""
Koko shakkisovellus hetkellä samassa tiedostossa, saattaa myöhemmin erotella 'käyttöliittymän', pelilogiikan ja tekoälyn omiin
"""
import time
#ns config asetukset, tästä voi pääasiassa vain aloitusvuoron vaihtaa, uusien nappuloidne tai
#pelilaudan koon vaihtaminen tässä versiossa rikkoo pelin
PELILAUTA = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
            [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
            [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
PELINAPPULAT = [[chr(9817),chr(9814),chr(9816),chr(9815),chr(9813),chr(9812)],
                [chr(9823),chr(9820),chr(9822),chr(9821),chr(9819),chr(9818)]]

ALKUVUORO = 0 #kaksinpelissä kumpi puoli aloittaa
LASKENTA_SYVYYS = 4 #Kuinka kauas tekoäly laskee siirtoja, kannattaa varmaan pitää välillä 3 -- 5

#!!! Puuttuu vielä mahdolliset erikoisliikkeet

def alku():
    """Funktion kutsuminen käynnistää sovelluksen. Funktio kutsuu kaksin tai yksinpeliin liittyvän funktion.
    """
    print("Pelistä voi poistua kirjoittamalla quit")
    print("Peli ei tunnista minkään näköisiä erikoissiirtoja")
    print("hetkellä jos tekoäly aloittaa sillä kestää merkittävästi kauemmin laskea siirto")
    while True:
        valinta = input("Kaksinpeli (2p) vai tekoalya vastaan (1p): ")
        if valinta in ("quit", "q"):
            break
        if valinta in ("2p", "2P", "2"):
            if kaksinpeli() == "quit":
                break
        if valinta in ("1p", "1P", "1"):
            if yksinpeli() == "quit":
                break

def matti(pelitilanne, vuoro):
    """Funktio päättelee pelitilanteen ja vuoron pohjalta 'onko_shakki' funktiota hyödyntäen pitäisikö pelin loppua.

    Args:
        pelitilanne List: PELILAUTA tapainen lista joka edustaa hetkistä pelitilannetta
        vuoro int: joko 0 jolloin on pieniä kirjaimia edustavan pelaajan vuoro ja 1 jos toisen pelaajan.

    Returns:
        Boolean: palauttaa True jos peli on loppunut ja False jos ei
    """
    mahdolliset = kone_kaikki_siirrot(pelitilanne, vuoro)
    uusittu = []
    for siirto in mahdolliset:
        poistettu = kone_siirto(pelitilanne, siirto)
        if not onko_shakki(pelitilanne, vuoro):
            uusittu.append(siirto)
        kone_peru(pelitilanne, siirto, poistettu)
    if len(uusittu) == 0:
        return True, uusittu
    return False, uusittu

def tee_siirto(pelitilanne, siirto):
    """Yksinkertaisesti siirtää jotain pelinappulaa

    Args:
        pelitilanne list: PELILAUTA tapainen listojen lista hetkisestä pelitilanteesta
        siirto string: Pelaajan tekemä siirto

    Returns:
        string: siirrettyyn ruutuun sisältävä pelinappula, tyhjään ruutuun siirtyessä siis esim. '-'
    """
    mista_x = ord(siirto[0])-97
    mista_y = int(siirto[1])-1
    mihin_x = ord(siirto[2])-97
    mihin_y = int(siirto[3])-1
    poistettu = pelitilanne[mihin_y][mihin_x]
    pelitilanne[mihin_y][mihin_x] = pelitilanne[mista_y][mista_x]
    pelitilanne[mista_y][mista_x] = "-"
    return poistettu

def kone_siirto(pelitilanne, siirto):
    """Sama kuin 'tee_siirto' käyttäen 'kone_kaikki_siirrot' siirtoja
    """
    poistettu = pelitilanne[siirto[3]][siirto[2]]
    pelitilanne[siirto[3]][siirto[2]] = pelitilanne[siirto[1]][siirto[0]]
    pelitilanne[siirto[1]][siirto[0]] = "-"
    return poistettu

def kone_peru(pelitilanne, siirto, nappula):
    """Palauttaa siirron tekemät muutokset

    Args:
        pelitilanne list: PELILAUTA tapainen listojen lista hetkisestä pelitilanteesta
        siirto string: Siirto jonka perutaan
        nappula string: Nappula joka ruudun paikalla ennen oli, esim. tyhjän ruudun ollessa '-'
    """
    pelitilanne[siirto[1]][siirto[0]] = pelitilanne[siirto[3]][siirto[2]]
    pelitilanne[siirto[3]][siirto[2]] = nappula

def onko_shakki(pelitilanne, vuoro):
    """Tarkistaa onko shakki, eli voiko vuorossa olevan pelaajan kuninkaan ruutuun hyökätä millään
    vastustajan napilla

    Args:
        pelitilanne list: PELILAUTA tapainen listojen lista hetkisestä pelitilanteesta
        vuoro int: kenen vuoro, 0 tai 1 arvona

    Returns:
        boolean: True jos on shakki, False jos ei ole
    """
    kingi = PELINAPPULAT[vuoro][5]
    if vuoro == 0:
        vastapuoli = kone_kaikki_siirrot(pelitilanne, 1)
    else:
        vastapuoli = kone_kaikki_siirrot(pelitilanne, 0)
    for y in range(8):
        for x in range(8):
            if pelitilanne[y][x] == kingi:
                sijainti = (x,y)
    for siirto in vastapuoli:
        if siirto[2] == sijainti[0] and siirto[3] == sijainti[1]:
            return True
    return False

def arvioi_tilanne(pelitilanne, siirrot=None, vuoro=0):
    """Funktio arvioimaan pelitilannetta, funktio on kevyt ja palauttaa siis vain tämän hetkisen pelitilanteen arvion,
    eli ei osaa mm. ennustaa shakkia. Funktio on hetkellä myös aika yksinkertainen, se ottaa huomioon vain materiaalin,
    mahdollisten siirtojen ja huonossa asemassa olevien sotilaiden määrät sekä shakki tilanteen.

    Args:
        pelitilanne list: PELILAUTA tapainen listojen lista hetkisestä pelitilanteesta
        siirrot (list, optional): Jos tekoäly on jo laskenut oman tilanteen mahdolliset siirrot niin ei tarvitse laskea uudestaan. Defaults to [].
        vuoro (int, optional): Kenen vuorolla tekoäly arvioi. Defaults to 0.

    Returns:
        int: palauttaa arvion pelitilanteesta, plussaa jos valkoinen on voittamassa, miinusta jos häviämässä.
    """
    materiaalipaino = 1
    sotilaspaino = 0.5
    siirtoja_paino = 10
    kuninkaan_uhka_paino = 0.5
    doubled_v = set()
    doubled_b = set()
    isolated_v = 0
    isolated_b = 0
    blocked_v = 0
    blocked_b = 0
    advancing_v = 0
    advancing_b = 0
    kuninkaan_uhka_v = 0
    kuninkaan_uhka_b = 0
    materiaali = 0
    if siirrot is None:
        siirrot_v = kone_kaikki_siirrot(pelitilanne, 0)
        siirrot_b = kone_kaikki_siirrot(pelitilanne, 1)
    else:
        if vuoro == 0:
            siirrot_v = siirrot
            siirrot_b = kone_kaikki_siirrot(pelitilanne, 1)
        else:
            siirrot_v = kone_kaikki_siirrot(pelitilanne, 0)
            siirrot_b = siirrot
    for x in range(8):
        for y in range(8):
            if pelitilanne[y][x] == "-":
                continue
            if pelitilanne[y][x] == chr(9817):
                materiaali += 100
                doubled_v.add(x)
                if not ((x > 0 and pelitilanne[y-1][x-1] == chr(9817)) or (x < 7 and pelitilanne[y-1][x+1] == chr(9817))):
                    isolated_v += 100
                if y < 7 and pelitilanne[y+1][x] != "-":
                    blocked_v += 100
                advancing_v += 10*(6-y)-abs(10*x-35)
            elif pelitilanne[y][x] == chr(9823):
                materiaali -= 100
                doubled_b.add(x)
                if not ((x > 0 and pelitilanne[y-1][x-1] == chr(9823)) or (x < 7 and pelitilanne[y-1][x+1] == chr(9823))):
                    isolated_b += 100
                if y > 0 and pelitilanne[y-1][x] != "-":
                    blocked_b += 100
                advancing_b += 10*(y-1)-abs(10*x-35)
            elif pelitilanne[y][x] == chr(9815):
                materiaali += 300
            elif pelitilanne[y][x] == chr(9821):
                materiaali -= 300
            elif pelitilanne[y][x] == chr(9816):
                materiaali += 300
            elif pelitilanne[y][x] == chr(9822):
                materiaali -= 300
            elif pelitilanne[y][x] == chr(9814):
                materiaali += 500
            elif pelitilanne[y][x] == chr(9820):
                materiaali -= 500
            elif pelitilanne[y][x] == chr(9813):
                materiaali += 900
            elif pelitilanne[y][x] == chr(9819):
                materiaali -= 900
            elif pelitilanne[y][x] == chr(9812):
                materiaali += 20000
                for siirto in siirrot_b:
                    if siirto[2] == x and siirto[3] == y:
                        kuninkaan_uhka_v += 100
            elif pelitilanne[y][x] == chr(9818):
                materiaali -= 20000
                for siirto in siirrot_v:
                    if siirto[2] == x and siirto[3] == y:
                        kuninkaan_uhka_b += 100
    arvio = materiaali*materiaalipaino
    arvio -= (len(doubled_b)*100-len(doubled_v)*100+isolated_v-isolated_b+blocked_v-blocked_b+advancing_v-advancing_b)*sotilaspaino
    arvio += (len(siirrot_v)-len(siirrot_b))*siirtoja_paino
    arvio -= (kuninkaan_uhka_b-kuninkaan_uhka_v)*kuninkaan_uhka_paino
    return arvio

def kone_kaikki_siirrot(pelitilanne, vuoro):
    """Uudempi ja parempi versio kaikkien mahdollisten siirtojen laskemiseen.

    Args:
        pelitilanne list: PELILAUTA tapainen listojen lista hetkisestä pelitilanteesta
        vuoro int: kenen vuoro, 0 tai 1 arvona

    Returns:
        list : lista kaikista laillisista siirroista. Siirrot muodossa '(3,6,3,4)' vastaa siirtoa 'd7d5'.
    """
    siirrot = []
    omat = PELINAPPULAT[vuoro]
    for y in range(8):
        for x in range(8):
            pelinappula = pelitilanne[y][x]
            if pelinappula == "-":
                pass
            elif pelinappula == omat[0]:
                #p tai P
                if vuoro == 0:
                    if y > 0:
                        if pelitilanne[y-1][x] == "-":
                            siirrot.append((x,y,x,y-1))
                            if y == 6 and pelitilanne[y-2][x] == "-":
                                siirrot.append((x,y,x,y-2))
                        if x > 0 and pelitilanne[y-1][x-1] not in omat and pelitilanne[y-1][x-1] != "-":
                            siirrot.append((x,y,x-1,y-1))
                        if x < 7 and pelitilanne[y-1][x+1] not in omat and pelitilanne[y-1][x+1] != "-":
                            siirrot.append((x,y,x+1,y-1))
                else:
                    if y < 7:
                        if pelitilanne[y+1][x] == "-":
                            siirrot.append((x,y,x,y+1))
                            if y == 1 and pelitilanne[y+2][x] == "-":
                                siirrot.append((x,y,x,y+2))
                        if x > 0 and pelitilanne[y+1][x-1] not in omat and pelitilanne[y+1][x-1] != "-":
                            siirrot.append((x,y,x-1,y+1))
                        if x < 7 and pelitilanne[y+1][x+1] not in omat and pelitilanne[y+1][x+1] != "-":
                            siirrot.append((x,y,x+1,y+1))
            elif pelinappula == omat[1]:
                #r tai R
                for i in range(x+1, 8):
                    if pelitilanne[y][i] == "-":
                        siirrot.append((x,y,i,y))
                    elif pelitilanne[y][i] in omat:
                        break
                    else:
                        siirrot.append((x,y,i,y))
                        break
                for i in range(x-1, -1,-1):
                    if pelitilanne[y][i] == "-":
                        siirrot.append((x,y,i,y))
                    elif pelitilanne[y][i] in omat:
                        break
                    else:
                        siirrot.append((x,y,i,y))
                        break
                for i in range(y+1, 8):
                    if pelitilanne[i][x] == "-":
                        siirrot.append((x,y,x,i))
                    elif pelitilanne[i][x] in omat:
                        break
                    else:
                        siirrot.append((x,y,x,i))
                        break
                for i in range(y-1, -1,-1):
                    if pelitilanne[i][x] == "-":
                        siirrot.append((x,y,x,i))
                    elif pelitilanne[i][x] in omat:
                        break
                    else:
                        siirrot.append((x,y,x,i))
                        break
            elif pelinappula == omat[2]:
                #h tai H
                if y < 6 and x < 7 and pelitilanne[y+2][x+1] not in omat:
                    siirrot.append((x,y,x+1,y+2))
                if y < 6 and x > 0 and pelitilanne[y+2][x-1] not in omat:
                    siirrot.append((x,y,x-1,y+2))
                if y > 1 and x < 7 and pelitilanne[y-2][x+1] not in omat:
                    siirrot.append((x,y,x+1,y-2))
                if y > 1 and x > 0 and pelitilanne[y-2][x-1] not in omat:
                    siirrot.append((x,y,x-1,y-2))
                if y < 7 and x < 6 and pelitilanne[y+1][x+2] not in omat:
                    siirrot.append((x,y,x+2,y+1))
                if y < 7 and x > 1 and pelitilanne[y+1][x-2] not in omat:
                    siirrot.append((x,y,x-2,y+1))
                if y > 0 and x < 6 and pelitilanne[y-1][x+2] not in omat:
                    siirrot.append((x,y,x+2,y-1))
                if y > 0 and x > 1 and pelitilanne[y-1][x-2] not in omat:
                    siirrot.append((x,y,x-2,y-1))
            elif pelinappula == omat[3]:
                #b tai B
                for i in range(1,9):
                    if x+i > 7 or y+i > 7 or pelitilanne[y+i][x+i] in omat:
                        break
                    if pelitilanne[y+i][x+i] == "-":
                        siirrot.append((x,y,x+i,y+i))
                    else:
                        siirrot.append((x,y,x+i,y+i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y+i > 7 or pelitilanne[y+i][x-i] in omat:
                        break
                    if pelitilanne[y+i][x-i] == "-":
                        siirrot.append((x,y,x-i,y+i))
                    else:
                        siirrot.append((x,y,x-i,y+i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y-i < 0 or pelitilanne[y-i][x+i] in omat:
                        break
                    if pelitilanne[y-i][x+i] == "-":
                        siirrot.append((x,y,x+i,y-i))
                    else:
                        siirrot.append((x,y,x+i,y-i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y-i < 0 or pelitilanne[y-i][x-i] in omat:
                        break
                    if pelitilanne[y-i][x-i] == "-":
                        siirrot.append((x,y,x-i,y-i))
                    else:
                        siirrot.append((x,y,x-i,y-i))
                        break
            elif pelinappula == omat[4]:
                #q tai Q
                for i in range(x+1, 8):
                    if pelitilanne[y][i] == "-":
                        siirrot.append((x,y,i,y))
                    elif pelitilanne[y][i] in omat:
                        break
                    else:
                        siirrot.append((x,y,i,y))
                        break
                for i in range(x-1, -1,-1):
                    if pelitilanne[y][i] == "-":
                        siirrot.append((x,y,i,y))
                    elif pelitilanne[y][i] in omat:
                        break
                    else:
                        siirrot.append((x,y,i,y))
                        break
                for i in range(y+1, 8):
                    if pelitilanne[i][x] == "-":
                        siirrot.append((x,y,x,i))
                    elif pelitilanne[i][x] in omat:
                        break
                    else:
                        siirrot.append((x,y,x,i))
                        break
                for i in range(y-1, -1,-1):
                    if pelitilanne[i][x] == "-":
                        siirrot.append((x,y,x,i))
                    elif pelitilanne[i][x] in omat:
                        break
                    else:
                        siirrot.append((x,y,x,i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y+i > 7 or pelitilanne[y+i][x+i] in omat:
                        break
                    if pelitilanne[y+i][x+i] == "-":
                        siirrot.append((x,y,x+i,y+i))
                    else:
                        siirrot.append((x,y,x+i,y+i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y+i > 7 or pelitilanne[y+i][x-i] in omat:
                        break
                    if pelitilanne[y+i][x-i] == "-":
                        siirrot.append((x,y,x-i,y+i))
                    else:
                        siirrot.append((x,y,x-i,y+i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y-i < 0 or pelitilanne[y-i][x+i] in omat:
                        break
                    if pelitilanne[y-i][x+i] == "-":
                        siirrot.append((x,y,x+i,y-i))
                    else:
                        siirrot.append((x,y,x+i,y-i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y-i < 0 or pelitilanne[y-i][x-i] in omat:
                        break
                    if pelitilanne[y-i][x-i] == "-":
                        siirrot.append((x,y,x-i,y-i))
                    else:
                        siirrot.append((x,y,x-i,y-i))
                        break
            elif pelinappula == omat[5]:
                #k tai K
                if x < 7 and pelitilanne[y][x+1] not in omat:
                    siirrot.append((x,y,x+1,y))
                if x > 0 and pelitilanne[y][x-1] not in omat:
                    siirrot.append((x,y,x-1,y))
                if y < 7 and pelitilanne[y+1][x] not in omat:
                    siirrot.append((x,y,x,y+1))
                if y > 0 and pelitilanne[y-1][x] not in omat:
                    siirrot.append((x,y,x,y-1))
                if y < 7 and x < 7 and pelitilanne[y+1][x+1] not in omat:
                    siirrot.append((x,y,x+1,y+1))
                if y < 7 and x > 0 and pelitilanne[y+1][x-1] not in omat:
                    siirrot.append((x,y,x-1,y+1))
                if y > 0 and x < 7 and pelitilanne[y-1][x+1] not in omat:
                    siirrot.append((x,y,x+1,y-1))
                if y > 0 and x > 0 and pelitilanne[y-1][x-1] not in omat:
                    siirrot.append((x,y,x-1,y-1))
    return siirrot

def yksinpeli():
    """Yksinpeli shakkibottia vastaan. Funktio on ikään kuin käyttöliittymää vain

    Returns:
        string: palauttaa 'quit' jos se jossain kohtaa konsoliin vastataan
    """
    vuoro = ALKUVUORO
    pelitilanne = []
    for rivi in PELILAUTA:
        pelitilanne.append(rivi[:])
    while True:
        valinta = input("Aloittaako pelaaja [y] vai ei [n]? ")
        if valinta in ("quit", "q"):
            return "quit"
        if valinta in ("y", "Y"):
            pelaaja = 0
            aly_vuoro = 1
            break
        if valinta in ("n", "N"):
            pelaaja = 1
            aly_vuoro = 0
            break
    siirto = (0, "")
    while True:
        print()
        print("  --------------------")
        for y in range(8):
            rivi = str(y+1) + " |"
            for x in range(8):
                if pelitilanne[y][x] == "-":
                    if (x+y)%2 == 0:
                        rivi += " " + chr(9633)
                    else:
                        rivi += " " + chr(9639)
                else:
                    rivi +=  " " + pelitilanne[y][x]
            print(rivi + "  |")
        print("  --------------------")
        print("    a b c d e f g h")
        print()

        arvio = arvioi_tilanne(pelitilanne, [], vuoro)
        print("Pelikenttä arvio: ", arvio/100)

        print("Pelaajan", vuoro+1, "vuoro")
        tilanne = matti(pelitilanne, vuoro)
        if tilanne[0]:
            print()
            if vuoro == 0:
                print("Tekoäly voitti!!!")
            else:
                print("Pelaaja voitti!!!")
            print()
            return ""
        siedettavammat = []
        for siirto in tilanne[1]:
            siedettavammat.append(chr(siirto[0]+97) + str(siirto[1]+1) + chr(siirto[2]+97) + str(siirto[3]+1))
        print("mahdolliset siirrot ", siedettavammat)
        if vuoro == pelaaja:
            siirtop = input("Syötä siirto: ")
            if siirtop in ("quit", "q"):
                return "quit"
            if siirtop in siedettavammat:
                tee_siirto(pelitilanne, siirtop)
                if vuoro == 1:
                    vuoro = 0
                else:
                    vuoro = 1
            else:
                print("Laiton siirto")
        else:
            print()
            print("miettii.....")
            alku_aika = time.time()
            if aly_vuoro == 1:
                siirto = tekoalya(pelitilanne, LASKENTA_SYVYYS, -50000, 50000, aly_vuoro, (0, ""))
            else:
                siirto = tekoalyb(pelitilanne, LASKENTA_SYVYYS, -50000, 50000, aly_vuoro, (0, ""))
            loppu_aika = time.time()
            print("Valmis! siirto; ", siirto[0], siirto[1])
            print("Aikaa miettimiseen kului: ", loppu_aika-alku_aika, "s")
            if siirto[1] in tilanne[1]:
                kone_siirto(pelitilanne, siirto[1])
                if vuoro == 1:
                    vuoro = 0
                else:
                    vuoro = 1
            else:
                print("Tekoäly rikki!!! Sori, laita palautetta jossain jotenkin, mieluusti pelitilanteen kera")
                return "quit"

def kaksinpeli():
    """Pelimuoto missä kaksi pelaajaa pelaa toisiaan vastaan. Tämä funktio vain vaihtaa vuoroja ja tulostaa pelilaudan tilanteen

    Returns:
        String: voi palauttaa vain 'quit' jolloin pelin suoritus pysähtyy. Jos mitään ei palauteta niin peli jatkuu
    """
    vuoro = ALKUVUORO
    pelitilanne = []
    for rivi in PELILAUTA:
        pelitilanne.append(rivi[:])
    while True:
        print()
        print("  ----------------------------")
        for y in range(8):
            rivi = str(y+1) + " | "
            for x in range(8):
                rivi += " " + pelitilanne[y][x] + " "
            print(rivi + " | ")
        print("  ----------------------------")
        print("     a"," b"," c"," d"," e"," f"," g"," h")
        print()
        arvio = arvioi_tilanne(pelitilanne, [], vuoro)
        print("Pelikenttä arvio: ", arvio/100)
        print("Pelaajan", vuoro+1, "vuoro")
        tilanne = matti(pelitilanne, vuoro)
        siedettavammat = []
        for siirto in tilanne[1]:
            siedettavammat.append(chr(siirto[0]+97) + str(siirto[1]+1) + chr(siirto[2]+97) + str(siirto[3]+1))
        if tilanne[0]:
            print()
            if vuoro == 0:
                print("Pelaaja 2 voitti!!!")
            else:
                print("Pelaaja 1 voitti!!!")
            print()
            return ""
        print("mahdolliset siirrot ", siedettavammat)
        siirto = input("Syötä siirto: ")
        if siirto in ("quit", "q"):
            return "quit"
        if siirto in siedettavammat:
            tee_siirto(pelitilanne, siirto)
            if vuoro == 1:
                vuoro = 0
            else:
                vuoro = 1
        else:
            print("Laiton siirto")

def tekoalya(pelitilanne, syvyys, alpha, beta, vuoro, edellinen_siirto):
    """Rekursiivinen funktio laskemaan paras siirto kun tekoälyn siirrolla tilanteen arvo maksimoidaan ja pelaajan vuorolla minimoidaan
    (shakkibotin suhteen). laskee mahdollisten siirtojen arvot joka askeleella, jolloin todennäköisesti karsitaan enemmän siirtoja.

    Args:
        pelitilanne list: PELILAUTA tapainen listojen lista hetkisestä pelitilanteesta
        syvyys int: funktion laskentasyvyys, näin monen siirron jälkeen palautetaan lopullinen tilannearvio
        alpha int: arvo jonka mukaan karsitaan vissiin pelaajalle epäotimaaliset siirrot
        beta int: arvo jolla karsitaan vissiin tekoälylle epäoptimaaliset siirrot
        vuoro int: kenen vuoro, 0 tai 1 arvona
        edellinen_siirto tuple(int, string): sisältää edellisen (tähän pelitilanteeseen päästävän) siirron ja sille lasketun arvon

    Returns:
        tuple(int, string): palauttaa tuplen joka kuvailee parasta siirtoa ja sen arvoa
    """
    if syvyys == 0 or not (-10000 < edellinen_siirto[0] and edellinen_siirto[0] < 10000):
        return edellinen_siirto
    siirrot = kone_kaikki_siirrot(pelitilanne, vuoro)
    arviot = []
    for siirto in siirrot:
        nappula = kone_siirto(pelitilanne, siirto)
        arviot.append((arvioi_tilanne(pelitilanne, siirrot, vuoro)*(-1), siirto))
        kone_peru(pelitilanne, siirto, nappula)
    if vuoro == 1:
        arviot.sort(reverse=True)
        arvo = (-50000,"")
        for siirto in arviot:
            nappula = kone_siirto(pelitilanne, siirto[1])
            temp = tekoalya(pelitilanne, syvyys-1, alpha, beta, 0, (siirto[0], siirto[1]))
            kone_peru(pelitilanne, siirto[1], nappula)
            if temp[0] > arvo[0]:
                arvo = (temp[0], siirto[1])
            alpha = max(arvo[0], alpha)
            if arvo[0] >= beta:
                break
        return arvo
    else:
        arviot.sort()
        arvo = (50000, "")
        for siirto in arviot:
            nappula = kone_siirto(pelitilanne, siirto[1])
            temp = tekoalya(pelitilanne, syvyys-1, alpha, beta, 1, (siirto[0], siirto[1]))
            if temp[0] < arvo[0]:
                arvo = (temp[0], siirto[1])
            kone_peru(pelitilanne, siirto[1], nappula)
            beta = max(arvo[0], beta)
            if arvo[0] <= alpha:
                break
        return arvo

def tekoalyb(pelitilanne, syvyys, alpha, beta, vuoro, edellinen_siirto):
    """Sama kuin tekoalya mutta pelaa valkoisilla napeilla, varmaan lopullisessa versiossa yhdistän nämä.
    """
    if syvyys == 0 or not (-10000 < edellinen_siirto[0] and edellinen_siirto[0] < 10000):
        return edellinen_siirto
    siirrot = kone_kaikki_siirrot(pelitilanne, vuoro)
    arviot = []
    for siirto in siirrot:
        nappula = kone_siirto(pelitilanne, siirto)
        arviot.append((arvioi_tilanne(pelitilanne, siirrot, vuoro), siirto))
        kone_peru(pelitilanne, siirto, nappula)
    if vuoro == 0:
        arviot.sort(reverse=True)
        arvo = (-50000,"")
        for siirto in arviot:
            nappula = kone_siirto(pelitilanne, siirto[1])
            temp = tekoalyb(pelitilanne, syvyys-1, alpha, beta, 1, (siirto[0], siirto[1]))
            kone_peru(pelitilanne, siirto[1], nappula)
            if temp[0] > arvo[0]:
                arvo = (temp[0], siirto[1])
            alpha = max(arvo[0], alpha)
            if arvo[0] >= beta:
                break
        return arvo
    else:
        arviot.sort()
        arvo = (50000, "")
        for siirto in arviot:
            nappula = kone_siirto(pelitilanne, siirto[1])
            temp = tekoalyb(pelitilanne, syvyys-1, alpha, beta, 0, (siirto[0], siirto[1]))
            if temp[0] < arvo[0]:
                arvo = (temp[0], siirto[1])
            kone_peru(pelitilanne, siirto[1], nappula)
            beta = max(arvo[0], beta)
            if arvo[0] <= alpha:
                break
        return arvo

if __name__ == "__main__":
    alku()
