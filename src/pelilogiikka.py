PELINAPPULAT = [["p","r","n","b","q","k"],
                ["P","R","N","B","Q","K"]]
TYHJA = "-"

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
        pelitilanne[mihin_y][mihin_x] = siirto[4]
    else:
        pelitilanne[mihin_y][mihin_x] = pelitilanne[mista_y][mista_x]
    pelitilanne[mista_y][mista_x] = TYHJA
    return poistettu

def kone_siirto(pelitilanne, siirto, vuoro=None):
    """Sama kuin 'tee_siirto' käyttäen 'kone_kaikki_siirrot' siirtoja
    """
    poistettu = pelitilanne[siirto[3]][siirto[2]]
    if len(siirto) > 5:
        pelitilanne[siirto[3]][siirto[2]] = siirto[4]
    else:
        pelitilanne[siirto[3]][siirto[2]] = pelitilanne[siirto[1]][siirto[0]]
    pelitilanne[siirto[1]][siirto[0]] = TYHJA
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
                pelitilanne[siirto[3]-1][siirto[2]] = nappula
            else:
                pelitilanne[siirto[3]+1][siirto[2]] = nappula
            pelitilanne[siirto[1]][siirto[0]] = pelitilanne[siirto[3]][siirto[2]]
            pelitilanne[siirto[3]][siirto[2]] = TYHJA
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
            if pelinappula == TYHJA:
                pass
            elif pelinappula == omat[0]:
                #p tai P
                if vuoro == 0:
                    if y > 0:
                        if pelitilanne[y-1][x] == TYHJA:
                            if y-1 == 0:
                                for nappi in PELINAPPULAT[0]:
                                    siirrot.append((x,y,x,y-1,nappi))
                            else:
                                siirrot.append((x,y,x,y-1))
                            if y == 6 and pelitilanne[y-2][x] == TYHJA:
                                siirrot.append((x,y,x,y-2))
                        if x > 0 and pelitilanne[y-1][x-1] not in omat and pelitilanne[y-1][x-1] != TYHJA:
                                siirrot.append((x,y,x-1,y-1))
                        if x < 7 and pelitilanne[y-1][x+1] not in omat and pelitilanne[y-1][x+1] != TYHJA:
                                siirrot.append((x,y,x+1,y-1))
                else:
                    if y < 7:
                        if pelitilanne[y+1][x] == TYHJA:
                            if y+1 == 7:
                                for nappi in PELINAPPULAT[1]:
                                    siirrot.append((x,y,x,y-1,nappi))
                            else:
                                siirrot.append((x,y,x,y+1))
                            if y == 1 and pelitilanne[y+2][x] == TYHJA:
                                siirrot.append((x,y,x,y+2))
                        if x > 0 and pelitilanne[y+1][x-1] not in omat and pelitilanne[y+1][x-1] != TYHJA:
                                siirrot.append((x,y,x-1,y+1))
                        if x < 7 and pelitilanne[y+1][x+1] not in omat and pelitilanne[y+1][x+1] != TYHJA:
                                siirrot.append((x,y,x+1,y+1))
            elif pelinappula == omat[1]:
                #r tai R
                for i in range(x+1, 8):
                    if pelitilanne[y][i] == TYHJA:
                        siirrot.append((x,y,i,y))
                    elif pelitilanne[y][i] in omat:
                        break
                    else:
                        siirrot.append((x,y,i,y))
                        break
                for i in range(x-1, -1,-1):
                    if pelitilanne[y][i] == TYHJA:
                        siirrot.append((x,y,i,y))
                    elif pelitilanne[y][i] in omat:
                        break
                    else:
                        siirrot.append((x,y,i,y))
                        break
                for i in range(y+1, 8):
                    if pelitilanne[i][x] == TYHJA:
                        siirrot.append((x,y,x,i))
                    elif pelitilanne[i][x] in omat:
                        break
                    else:
                        siirrot.append((x,y,x,i))
                        break
                for i in range(y-1, -1,-1):
                    if pelitilanne[i][x] == TYHJA:
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
                    if pelitilanne[y+i][x+i] == TYHJA:
                        siirrot.append((x,y,x+i,y+i))
                    else:
                        siirrot.append((x,y,x+i,y+i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y+i > 7 or pelitilanne[y+i][x-i] in omat:
                        break
                    if pelitilanne[y+i][x-i] == TYHJA:
                        siirrot.append((x,y,x-i,y+i))
                    else:
                        siirrot.append((x,y,x-i,y+i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y-i < 0 or pelitilanne[y-i][x+i] in omat:
                        break
                    if pelitilanne[y-i][x+i] == TYHJA:
                        siirrot.append((x,y,x+i,y-i))
                    else:
                        siirrot.append((x,y,x+i,y-i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y-i < 0 or pelitilanne[y-i][x-i] in omat:
                        break
                    if pelitilanne[y-i][x-i] == TYHJA:
                        siirrot.append((x,y,x-i,y-i))
                    else:
                        siirrot.append((x,y,x-i,y-i))
                        break
            elif pelinappula == omat[4]:
                #q tai Q
                for i in range(x+1, 8):
                    if pelitilanne[y][i] == TYHJA:
                        siirrot.append((x,y,i,y))
                    elif pelitilanne[y][i] in omat:
                        break
                    else:
                        siirrot.append((x,y,i,y))
                        break
                for i in range(x-1, -1,-1):
                    if pelitilanne[y][i] == TYHJA:
                        siirrot.append((x,y,i,y))
                    elif pelitilanne[y][i] in omat:
                        break
                    else:
                        siirrot.append((x,y,i,y))
                        break
                for i in range(y+1, 8):
                    if pelitilanne[i][x] == TYHJA:
                        siirrot.append((x,y,x,i))
                    elif pelitilanne[i][x] in omat:
                        break
                    else:
                        siirrot.append((x,y,x,i))
                        break
                for i in range(y-1, -1,-1):
                    if pelitilanne[i][x] == TYHJA:
                        siirrot.append((x,y,x,i))
                    elif pelitilanne[i][x] in omat:
                        break
                    else:
                        siirrot.append((x,y,x,i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y+i > 7 or pelitilanne[y+i][x+i] in omat:
                        break
                    if pelitilanne[y+i][x+i] == TYHJA:
                        siirrot.append((x,y,x+i,y+i))
                    else:
                        siirrot.append((x,y,x+i,y+i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y+i > 7 or pelitilanne[y+i][x-i] in omat:
                        break
                    if pelitilanne[y+i][x-i] == TYHJA:
                        siirrot.append((x,y,x-i,y+i))
                    else:
                        siirrot.append((x,y,x-i,y+i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y-i < 0 or pelitilanne[y-i][x+i] in omat:
                        break
                    if pelitilanne[y-i][x+i] == TYHJA:
                        siirrot.append((x,y,x+i,y-i))
                    else:
                        siirrot.append((x,y,x+i,y-i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y-i < 0 or pelitilanne[y-i][x-i] in omat:
                        break
                    if pelitilanne[y-i][x-i] == TYHJA:
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

def kone_ihan_kaikki_siirrot(pelitilanne):
    """Uudempi ja parempi versio kaikkien mahdollisten siirtojen laskemiseen.

    Args:
        pelitilanne list: PELILAUTA tapainen listojen lista hetkisestä pelitilanteesta
        vuoro int: kenen vuoro, 0 tai 1 arvona
    
    Returns:
        list : lista kaikista laillisista siirroista. Siirrot muodossa '(3,6,3,4)' vastaa siirtoa 'd7d5'.
    """
    v_siirrot = []
    m_siirrot = []
    valkoiset = PELINAPPULAT[0]
    mustat = PELINAPPULAT[1]
    v_shakki = False
    m_shakki = False
    for y in range(8):
        for x in range(8):
            pelinappula = pelitilanne[y][x]
            if pelinappula == TYHJA:
                pass
            elif pelinappula == mustat[0]:
                if y < 7:
                    if pelitilanne[y+1][x] == TYHJA:
                        m_siirrot.append((x,y,x,y+1))
                        if y == 1 and pelitilanne[y+2][x] == TYHJA:
                            m_siirrot.append((x,y,x,y+2))
                    if x > 0 and pelitilanne[y+1][x-1] not in mustat and pelitilanne[y+1][x-1] != TYHJA:
                            if pelitilanne[y+1][x-1] == valkoiset[5]:
                                v_shakki = True
                            m_siirrot.append((x,y,x-1,y+1))
                    if x < 7 and pelitilanne[y+1][x+1] not in mustat and pelitilanne[y+1][x+1] != TYHJA:
                            if pelitilanne[y+1][x+1] == valkoiset[5]:
                                v_shakki = True
                            m_siirrot.append((x,y,x+1,y+1))
            elif pelinappula == mustat[1]:
                #r tai R
                for i in range(x+1, 8):
                    if pelitilanne[y][i] in mustat:
                        break
                    if pelitilanne[y][i] == TYHJA:
                        m_siirrot.append((x,y,i,y))
                    else:
                        if pelitilanne[y][i] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,i,y))
                        break
                for i in range(x-1, -1,-1):
                    if pelitilanne[y][i] in mustat:
                        break
                    if pelitilanne[y][i] == TYHJA:
                        m_siirrot.append((x,y,i,y))
                    else:
                        if pelitilanne[y][i] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,i,y))
                        break
                for i in range(y+1, 8):
                    if pelitilanne[i][x] in mustat:
                        break
                    if pelitilanne[i][x] == TYHJA:
                        m_siirrot.append((x,y,x,i))
                    else:
                        if pelitilanne[i][x] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,x,i))
                        break
                for i in range(y-1, -1,-1):
                    if pelitilanne[i][x] in mustat:
                        break
                    if pelitilanne[i][x] == TYHJA:
                        m_siirrot.append((x,y,x,i))
                    else:
                        if pelitilanne[i][x] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,x,i))
                        break
            elif pelinappula == mustat[2]:
                #h tai H
                if y < 6 and x < 7 and pelitilanne[y+2][x+1] not in mustat:
                    if pelitilanne[y+2][x+1] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x+1,y+2))
                if y < 6 and x > 0 and pelitilanne[y+2][x-1] not in mustat:
                    if pelitilanne[y+2][x-1] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x-1,y+2))
                if y > 1 and x < 7 and pelitilanne[y-2][x+1] not in mustat:
                    if pelitilanne[y-2][x+1] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x+1,y-2))
                if y > 1 and x > 0 and pelitilanne[y-2][x-1] not in mustat:
                    if pelitilanne[y-2][x-1] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x-1,y-2))
                if y < 7 and x < 6 and pelitilanne[y+1][x+2] not in mustat:
                    if pelitilanne[y+1][x+2] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x+2,y+1))
                if y < 7 and x > 1 and pelitilanne[y+1][x-2] not in mustat:
                    if pelitilanne[y+1][x-2] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x-2,y+1))
                if y > 0 and x < 6 and pelitilanne[y-1][x+2] not in mustat:
                    if pelitilanne[y-1][x+2] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x+2,y-1))
                if y > 0 and x > 1 and pelitilanne[y-1][x-2] not in mustat:
                    if pelitilanne[y-1][x-2] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x-2,y-1))
            elif pelinappula == mustat[3]:
                #b tai B
                for i in range(1,9):
                    if x+i > 7 or y+i > 7 or pelitilanne[y+i][x+i] in mustat:
                        break
                    if pelitilanne[y+i][x+i] == TYHJA:
                        m_siirrot.append((x,y,x+i,y+i))
                    else:
                        if pelitilanne[y+i][x+i] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,x+i,y+i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y+i > 7 or pelitilanne[y+i][x-i] in mustat:
                        break
                    if pelitilanne[y+i][x-i] == TYHJA:
                        m_siirrot.append((x,y,x-i,y+i))
                    else:
                        if pelitilanne[y+i][x-i] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,x-i,y+i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y-i < 0 or pelitilanne[y-i][x+i] in mustat:
                        break
                    if pelitilanne[y-i][x+i] == TYHJA:
                        m_siirrot.append((x,y,x+i,y-i))
                    else:
                        if pelitilanne[y-i][x+i] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,x+i,y-i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y-i < 0 or pelitilanne[y-i][x-i] in mustat:
                        break
                    if pelitilanne[y-i][x-i] == TYHJA:
                        m_siirrot.append((x,y,x-i,y-i))
                    else:
                        if pelitilanne[y-i][x-i] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,x-i,y-i))
                        break
            elif pelinappula == mustat[4]:
                #q tai Q
                for i in range(x+1, 8):
                    if pelitilanne[y][i] in mustat:
                        break
                    if pelitilanne[y][i] == TYHJA:
                        m_siirrot.append((x,y,i,y))
                    else:
                        if pelitilanne[y][i] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,i,y))
                        break
                for i in range(x-1, -1,-1):
                    if pelitilanne[y][i] in mustat:
                        break
                    if pelitilanne[y][i] == TYHJA:
                        m_siirrot.append((x,y,i,y))
                    else:
                        if pelitilanne[y][i] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,i,y))
                        break
                for i in range(y+1, 8):
                    if pelitilanne[i][x] in mustat:
                        break
                    if pelitilanne[i][x] == TYHJA:
                        m_siirrot.append((x,y,x,i))
                    else:
                        if pelitilanne[i][x] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,x,i))
                        break
                for i in range(y-1, -1,-1):
                    if pelitilanne[i][x] in mustat:
                        break
                    if pelitilanne[i][x] == TYHJA:
                        m_siirrot.append((x,y,x,i))
                    else:
                        if pelitilanne[i][x] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,x,i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y+i > 7 or pelitilanne[y+i][x+i] in mustat:
                        break
                    if pelitilanne[y+i][x+i] == TYHJA:
                        m_siirrot.append((x,y,x+i,y+i))
                    else:
                        if pelitilanne[y+i][x+i] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,x+i,y+i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y+i > 7 or pelitilanne[y+i][x-i] in mustat:
                        break
                    if pelitilanne[y+i][x-i] == TYHJA:
                        m_siirrot.append((x,y,x-i,y+i))
                    else:
                        if pelitilanne[y+i][x-i] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,x-i,y+i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y-i < 0 or pelitilanne[y-i][x+i] in mustat:
                        break
                    if pelitilanne[y-i][x+i] == TYHJA:
                        m_siirrot.append((x,y,x+i,y-i))
                    else:
                        if pelitilanne[y-i][x+i] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,x+i,y-i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y-i < 0 or pelitilanne[y-i][x-i] in mustat:
                        break
                    if pelitilanne[y-i][x-i] == TYHJA:
                        m_siirrot.append((x,y,x-i,y-i))
                    else:
                        if pelitilanne[y-i][x-i] == valkoiset[5]:
                            v_shakki = True
                        m_siirrot.append((x,y,x-i,y-i))
                        break
            elif pelinappula == mustat[5]:
                #k tai K
                if x < 7 and pelitilanne[y][x+1] not in mustat:
                    if pelitilanne[y][x+1] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x+1,y))
                if x > 0 and pelitilanne[y][x-1] not in mustat:
                    if pelitilanne[y][x-1] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x-1,y))
                if y < 7 and pelitilanne[y+1][x] not in mustat:
                    if pelitilanne[y+1][x] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x,y+1))
                if y > 0 and pelitilanne[y-1][x] not in mustat:
                    if pelitilanne[y-1][x] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x,y-1))
                if y < 7 and x < 7 and pelitilanne[y+1][x+1] not in mustat:
                    if pelitilanne[y+1][x+1] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x+1,y+1))
                if y < 7 and x > 0 and pelitilanne[y+1][x-1] not in mustat:
                    if pelitilanne[y+1][x-1] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x-1,y+1))
                if y > 0 and x < 7 and pelitilanne[y-1][x+1] not in mustat:
                    if pelitilanne[y-1][x+1] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x+1,y-1))
                if y > 0 and x > 0 and pelitilanne[y-1][x-1] not in mustat:
                    if pelitilanne[y-1][x-1] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x-1,y-1))
            elif pelinappula == valkoiset[0]:
                #p
                if y > 0:
                    if pelitilanne[y-1][x] == TYHJA:
                        if y-1 == 0:
                            for nappi in PELINAPPULAT[0]:
                                v_siirrot.append((x,y,x,y-1,nappi))
                        else:
                            v_siirrot.append((x,y,x,y-1))
                        if y == 6 and pelitilanne[y-2][x] == TYHJA:
                            v_siirrot.append((x,y,x,y-2))
                    if x > 0 and pelitilanne[y-1][x-1] not in valkoiset and pelitilanne[y-1][x-1] != TYHJA:
                            if pelitilanne[y-1][x-1] == mustat[5]:
                                m_shakki = True
                            v_siirrot.append((x,y,x-1,y-1))
                    if x < 7 and pelitilanne[y-1][x+1] not in valkoiset and pelitilanne[y-1][x+1] != TYHJA:
                            if pelitilanne[y-1][x+1] == mustat[5]:
                                m_shakki = True
                            v_siirrot.append((x,y,x+1,y-1))
            elif pelinappula == valkoiset[1]:
                #r tai R
                for i in range(x+1, 8):
                    if pelitilanne[y][i] in valkoiset:
                        break
                    if pelitilanne[y][i] == TYHJA:
                        v_siirrot.append((x,y,i,y))
                    else:
                        if pelitilanne[y][i] == valkoiset[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,i,y))
                        break
                for i in range(x-1, -1,-1):
                    if pelitilanne[y][i] in valkoiset:
                        break
                    if pelitilanne[y][i] == TYHJA:
                        v_siirrot.append((x,y,i,y))
                    else:
                        if pelitilanne[y][i] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,i,y))
                        break
                for i in range(y+1, 8):
                    if pelitilanne[i][x] in valkoiset:
                        break
                    if pelitilanne[i][x] == TYHJA:
                        v_siirrot.append((x,y,x,i))
                    else:
                        if pelitilanne[i][x] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,x,i))
                        break
                for i in range(y-1, -1,-1):
                    if pelitilanne[i][x] in valkoiset:
                        break
                    if pelitilanne[i][x] == TYHJA:
                        v_siirrot.append((x,y,x,i))
                    else:
                        if pelitilanne[i][x] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,x,i))
                        break
            elif pelinappula == valkoiset[2]:
                #h tai H
                if y < 6 and x < 7 and pelitilanne[y+2][x+1] not in valkoiset:
                    if pelitilanne[y+2][x+1] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x+1,y+2))
                if y < 6 and x > 0 and pelitilanne[y+2][x-1] not in valkoiset:
                    if pelitilanne[y+2][x-1] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x-1,y+2))
                if y > 1 and x < 7 and pelitilanne[y-2][x+1] not in valkoiset:
                    if pelitilanne[y-2][x+1] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x+1,y-2))
                if y > 1 and x > 0 and pelitilanne[y-2][x-1] not in valkoiset:
                    if pelitilanne[y-2][x-1] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x-1,y-2))
                if y < 7 and x < 6 and pelitilanne[y+1][x+2] not in valkoiset:
                    if pelitilanne[y+1][x+2] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x+2,y+1))
                if y < 7 and x > 1 and pelitilanne[y+1][x-2] not in valkoiset:
                    if pelitilanne[y+1][x-2] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x-2,y+1))
                if y > 0 and x < 6 and pelitilanne[y-1][x+2] not in valkoiset:
                    if pelitilanne[y-1][x+2] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x+2,y-1))
                if y > 0 and x > 1 and pelitilanne[y-1][x-2] not in valkoiset:
                    if pelitilanne[y-1][x-2] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x-2,y-1))
            elif pelinappula == valkoiset[3]:
                #b tai B
                for i in range(1,9):
                    if x+i > 7 or y+i > 7 or pelitilanne[y+i][x+i] in valkoiset:
                        break
                    if pelitilanne[y+i][x+i] == TYHJA:
                        v_siirrot.append((x,y,x+i,y+i))
                    else:
                        if pelitilanne[y+i][x+i] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,x+i,y+i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y+i > 7 or pelitilanne[y+i][x-i] in valkoiset:
                        break
                    if pelitilanne[y+i][x-i] == TYHJA:
                        v_siirrot.append((x,y,x-i,y+i))
                    else:
                        if pelitilanne[y+i][x-i] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,x-i,y+i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y-i < 0 or pelitilanne[y-i][x+i] in valkoiset:
                        break
                    if pelitilanne[y-i][x+i] == TYHJA:
                        v_siirrot.append((x,y,x+i,y-i))
                    else:
                        if pelitilanne[y-i][x+i] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,x+i,y-i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y-i < 0 or pelitilanne[y-i][x-i] in valkoiset:
                        break
                    if pelitilanne[y-i][x-i] == TYHJA:
                        v_siirrot.append((x,y,x-i,y-i))
                    else:
                        if pelitilanne[y-i][x-i] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,x-i,y-i))
                        break
            elif pelinappula == valkoiset[4]:
                #q tai Qfor i in range(x+1, 8):
                for i in range(x+1, 8):
                    if pelitilanne[y][i] in valkoiset:
                        break
                    if pelitilanne[y][i] == TYHJA:
                        v_siirrot.append((x,y,i,y))
                    else:
                        if pelitilanne[y][i] == valkoiset[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,i,y))
                        break
                for i in range(x-1, -1,-1):
                    if pelitilanne[y][i] in valkoiset:
                        break
                    if pelitilanne[y][i] == TYHJA:
                        v_siirrot.append((x,y,i,y))
                    else:
                        if pelitilanne[y][i] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,i,y))
                        break
                for i in range(y+1, 8):
                    if pelitilanne[i][x] in valkoiset:
                        break
                    if pelitilanne[i][x] == TYHJA:
                        v_siirrot.append((x,y,x,i))
                    else:
                        if pelitilanne[i][x] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,x,i))
                        break
                for i in range(y-1, -1,-1):
                    if pelitilanne[i][x] in valkoiset:
                        break
                    if pelitilanne[i][x] == TYHJA:
                        v_siirrot.append((x,y,x,i))
                    else:
                        if pelitilanne[i][x] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,x,i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y+i > 7 or pelitilanne[y+i][x+i] in valkoiset:
                        break
                    if pelitilanne[y+i][x+i] == TYHJA:
                        v_siirrot.append((x,y,x+i,y+i))
                    else:
                        if pelitilanne[y+i][x+i] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,x+i,y+i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y+i > 7 or pelitilanne[y+i][x-i] in valkoiset:
                        break
                    if pelitilanne[y+i][x-i] == TYHJA:
                        v_siirrot.append((x,y,x-i,y+i))
                    else:
                        if pelitilanne[y+i][x-i] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,x-i,y+i))
                        break
                for i in range(1,9):
                    if x+i > 7 or y-i < 0 or pelitilanne[y-i][x+i] in valkoiset:
                        break
                    if pelitilanne[y-i][x+i] == TYHJA:
                        v_siirrot.append((x,y,x+i,y-i))
                    else:
                        if pelitilanne[y-i][x+i] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,x+i,y-i))
                        break
                for i in range(1,9):
                    if x-i < 0 or y-i < 0 or pelitilanne[y-i][x-i] in valkoiset:
                        break
                    if pelitilanne[y-i][x-i] == TYHJA:
                        v_siirrot.append((x,y,x-i,y-i))
                    else:
                        if pelitilanne[y-i][x-i] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,x-i,y-i))
                        break
            elif pelinappula == valkoiset[5]:
                #k tai K
                if x < 7 and pelitilanne[y][x+1] not in valkoiset:
                    if pelitilanne[y][x+1] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x+1,y))
                if x > 0 and pelitilanne[y][x-1] not in valkoiset:
                    if pelitilanne[y][x-1] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x-1,y))
                if y < 7 and pelitilanne[y+1][x] not in valkoiset:
                    if pelitilanne[y+1][x] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x,y+1))
                if y > 0 and pelitilanne[y-1][x] not in valkoiset:
                    if pelitilanne[y-1][x] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x,y-1))
                if y < 7 and x < 7 and pelitilanne[y+1][x+1] not in valkoiset:
                    if pelitilanne[y+1][x+1] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x+1,y+1))
                if y < 7 and x > 0 and pelitilanne[y+1][x-1] not in valkoiset:
                    if pelitilanne[y+1][x-1] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x-1,y+1))
                if y > 0 and x < 7 and pelitilanne[y-1][x+1] not in valkoiset:
                    if pelitilanne[y-1][x+1] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x+1,y-1))
                if y > 0 and x > 0 and pelitilanne[y-1][x-1] not in valkoiset:
                    if pelitilanne[y-1][x-1] == mustat[5]:
                        m_shakki = True
                    v_siirrot.append((x,y,x-1,y-1))
    return (v_siirrot, m_siirrot, v_shakki, m_shakki)