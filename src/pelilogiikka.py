PELINAPPULAT = [[chr(9817),chr(9814),chr(9816),chr(9815),chr(9813),chr(9812)],
                [chr(9823),chr(9820),chr(9822),chr(9821),chr(9819),chr(9818)]]

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
        kone_peru(pelitilanne, siirto, poistettu, vuoro)
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
    if len(siirto) > 5:
        if siirto[4] == "e":
            if pelitilanne[mista_y][mista_x] == chr(9817):
                poistettu = chr(9823)
                pelitilanne[siirto[3]-1][siirto[2]] = "-"
            else:
                poistettu = chr(9817)
                pelitilanne[siirto[3]+1][siirto[2]] = "-"
            pelitilanne[mihin_y][mihin_x] = pelitilanne[mista_y][mista_x]
        else:
            pelitilanne[mihin_y][mihin_x] = siirto[4]
    else:
        pelitilanne[mihin_y][mihin_x] = pelitilanne[mista_y][mista_x]
    pelitilanne[mista_y][mista_x] = "-"
    return poistettu

def kone_siirto(pelitilanne, siirto, vuoro=None):
    """Sama kuin 'tee_siirto' käyttäen 'kone_kaikki_siirrot' siirtoja
    """
    poistettu = pelitilanne[siirto[3]][siirto[2]]
    if len(siirto) > 5:
        if siirto[4] == "en":
            if vuoro == 0:
                poistettu = chr(9823)
                pelitilanne[siirto[3]-1][siirto[2]] = "-"
            else:
                poistettu = chr(9817)
                pelitilanne[siirto[3]+1][siirto[2]] = "-"
            pelitilanne[siirto[3]][siirto[2]] = pelitilanne[siirto[1]][siirto[0]]
        else:
            pelitilanne[siirto[3]][siirto[2]] = siirto[4]
    else:
        pelitilanne[siirto[3]][siirto[2]] = pelitilanne[siirto[1]][siirto[0]]
    pelitilanne[siirto[1]][siirto[0]] = "-"
    return poistettu

def kone_peru(pelitilanne, siirto, nappula, vuoro):
    """Palauttaa siirron tekemät muutokset

    Args:
        pelitilanne list: PELILAUTA tapainen listojen lista hetkisestä pelitilanteesta
        siirto string: Siirto jonka perutaan
        nappula string: Nappula joka ruudun paikalla ennen oli, esim. tyhjän ruudun ollessa '-'
    """
    if len(siirto) > 5:
        if siirto[4] == "en":
            if vuoro == 0:
                poistettu = chr(9823)
                pelitilanne[siirto[3]-1][siirto[2]] = nappula
            else:
                poistettu = chr(9817)
                pelitilanne[siirto[3]+1][siirto[2]] = nappula
            pelitilanne[siirto[1]][siirto[0]] = pelitilanne[siirto[3]][siirto[2]]
            pelitilanne[siirto[3]][siirto[2]] = "-"
        else:
            pelitilanne[siirto[1]][siirto[0]] = PELINAPPULAT[vuoro][0]
            pelitilanne[siirto[3]][siirto[2]] = nappula
    else:
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

def kone_kaikki_siirrot(pelitilanne, vuoro, edellinen_siirto=(0,0,0,0)):
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
                            if y-1 == 0:
                                for nappi in PELINAPPULAT[0]:
                                    siirrot.append((x,y,x,y-1,nappi))
                            else:
                                siirrot.append((x,y,x,y-1))
                            if y == 6 and pelitilanne[y-2][x] == "-":
                                siirrot.append((x,y,x,y-2))
                        if x > 0 and pelitilanne[y-1][x-1] not in omat:
                            if pelitilanne[y-1][x-1] == "-":
                                if y == 3 and edellinen_siirto[0] == x-1 and edellinen_siirto[2] == x-1 and edellinen_siirto[1] == 1 and edellinen_siirto[3] == 3 and pelitilanne[x-1][3] == chr(9823):
                                    siirrot.append(x,y,x-1,2,"en")
                            else:
                                siirrot.append((x,y,x-1,y-1))
                        if x < 7 and pelitilanne[y-1][x+1] not in omat:
                            if pelitilanne[y-1][x+1] == "-":
                                if y == 3 and edellinen_siirto[0] == x+1 and edellinen_siirto[2] == x+1 and edellinen_siirto[1] == 1 and edellinen_siirto[3] == 3 and pelitilanne[x+1][3] == chr(9823):
                                    siirrot.append(x,y,x+1,2,"en")
                            else:
                                siirrot.append((x,y,x+1,y-1))
                else:
                    if y < 7:
                        if pelitilanne[y+1][x] == "-":
                            siirrot.append((x,y,x,y+1))
                            if y == 1 and pelitilanne[y+2][x] == "-":
                                siirrot.append((x,y,x,y+2))
                        if x > 0 and pelitilanne[y+1][x-1] not in omat and pelitilanne[y+1][x-1] != "-":
                            if pelitilanne[y+1][x-1] == "-":
                                if y == 4 and edellinen_siirto[0] == x-1 and edellinen_siirto[2] == x-1 and edellinen_siirto[1] == 6 and edellinen_siirto[3] == 4 and pelitilanne[x-1][4] == chr(9817):
                                    siirrot.append(x,y,x-1,5,"en")
                            else:
                                siirrot.append((x,y,x-1,y+1))
                            siirrot.append((x,y,x-1,y+1))
                        if x < 7 and pelitilanne[y+1][x+1] not in omat and pelitilanne[y+1][x+1] != "-":
                            if pelitilanne[y+1][x+1] == "-":
                                if y == 4 and edellinen_siirto[0] == x+1 and edellinen_siirto[2] == x+1 and edellinen_siirto[1] == 6 and edellinen_siirto[3] == 4 and pelitilanne[x-1][4] == chr(9817):
                                    siirrot.append(x,y,x+1,5,"en")
                            else:
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