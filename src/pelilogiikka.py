PELINAPPULAT = [["p","r","n","b","q","k"],
                ["P","R","N","B","Q","K"]]
TYHJA = "-"

def matti(pelitilanne, vuoro, peliID="------"):
    """Funktio päättelee pelitilanteen ja vuoron pohjalta 'onko_shakki' funktiota hyödyntäen pitäisikö pelin loppua.

    Args:
        pelitilanne List: PELILAUTA tapainen lista joka edustaa hetkistä pelitilannetta
        vuoro int: joko 0 jolloin on pieniä kirjaimia edustavan pelaajan vuoro ja 1 jos toisen pelaajan.

    Returns:
        Boolean: palauttaa True jos peli on loppunut ja False jos ei
    """
    mahdolliset = kone_ihan_kaikki_wt_siirrot(pelitilanne, peliID)
    uusittu = []
    tasapeli = not mahdolliset[vuoro+2]
    for siirto in mahdolliset[vuoro]:
        poistettu, peliID = kone_siirto(pelitilanne, siirto, vuoro)
        if not onko_shakki(pelitilanne, vuoro, peliID):
            uusittu.append(siirto)
        kone_peru(pelitilanne, siirto, poistettu, vuoro)
    if len(uusittu) == 0:
        return True, uusittu, tasapeli
    return False, uusittu

def tee_siirto(pelitilanne, siirto, vuoro, peliID="------"):
    """Yksinkertaisesti siirtää jotain pelinappulaa

    Args:
        pelitilanne list: PELILAUTA tapainen listojen lista hetkisestä pelitilanteesta
        siirto string: Pelaajan tekemä siirto

    Returns:
        string: siirrettyyn ruutuun sisältävä pelinappula, tyhjään ruutuun siirtyessä siis esim. '-'
    """
    if len(siirto) > 4:
        mista_x = ord(siirto[0])-97
        mista_y = int(siirto[1])-1
        mihin_x = ord(siirto[2])-97
        mihin_y = int(siirto[3])-1
        poistettu = pelitilanne[mihin_y][mihin_x]
        pelitilanne[mihin_y][mihin_x] = siirto[4]
        pelitilanne[mista_y][mista_x] = TYHJA
    elif len(siirto) < 4:
        poistettu = TYHJA
        if vuoro == 0:
            if len(siirto) < 3:
                pelitilanne[7][6] = pelitilanne[7][4]
                pelitilanne[7][5] = pelitilanne[7][7]
                pelitilanne[7][4] = TYHJA
                pelitilanne[7][7] = TYHJA
                peliID = peliID[:-4] + "--" + peliID[-2:]
            else:
                pelitilanne[7][2] = pelitilanne[7][4]
                pelitilanne[7][3] = pelitilanne[7][0]
                pelitilanne[7][4] = TYHJA
                pelitilanne[7][0] = TYHJA
                peliID = peliID[:-4] + "--" + peliID[-2:]
        else:
            if len(siirto) < 3:
                pelitilanne[0][6] = pelitilanne[0][4]
                pelitilanne[0][5] = pelitilanne[0][7]
                pelitilanne[0][4] = TYHJA
                pelitilanne[0][7] = TYHJA
                peliID = peliID[:-6] + "--" + peliID[-4:]
            else:
                pelitilanne[0][2] = pelitilanne[0][4]
                pelitilanne[0][3] = pelitilanne[0][0]
                pelitilanne[0][4] = TYHJA
                pelitilanne[0][0] = TYHJA
                peliID = peliID[:-6] + "--" + peliID[-4:]
    else:
        mista_x = ord(siirto[0])-97
        mista_y = int(siirto[1])-1
        mihin_x = ord(siirto[2])-97
        mihin_y = int(siirto[3])-1
        poistettu = pelitilanne[mihin_y][mihin_x]
        pelitilanne[mihin_y][mihin_x] = pelitilanne[mista_y][mista_x]
        if pelitilanne[mista_y][mista_x] == PELINAPPULAT[vuoro][1]:
            if vuoro == 0:
                if siirto[mista_x] == 0:
                    peliID = peliID[:-3] + "-" + peliID[-2:]
                elif siirto[mista_x] == 7:
                    peliID = peliID[:-4] + "-" + peliID[-3:]
            else:
                if siirto[mista_x] == 0:
                    peliID = peliID[:-5] + "-" + peliID[-4:]
                elif siirto[mista_x] == 7:
                    peliID = peliID[:-6] + "-" + peliID[-5:]
        elif pelitilanne[mista_y][mista_x] == PELINAPPULAT[vuoro][5]:
            if vuoro == 0:
                peliID = peliID[:-4] + "--" + peliID[-2:]
            else:
                peliID = peliID[:-6] + "--" + peliID[-4:]
        pelitilanne[mista_y][mista_x] = TYHJA
    return poistettu, peliID

def kone_siirto(pelitilanne, siirto, vuoro, peliID="------"):
    """Sama kuin 'tee_siirto' käyttäen 'kone_kaikki_siirrot' siirtoja
    """
    if len(siirto) > 4:
        poistettu = pelitilanne[siirto[3]][siirto[2]]
        pelitilanne[siirto[3]][siirto[2]] = siirto[4]
        pelitilanne[siirto[1]][siirto[0]] = TYHJA
    elif len(siirto) < 4:
        poistettu = TYHJA
        if vuoro == 0:
            if len(siirto) < 3:
                pelitilanne[7][6] = pelitilanne[7][4]
                pelitilanne[7][5] = pelitilanne[7][7]
                pelitilanne[7][4] = TYHJA
                pelitilanne[7][7] = TYHJA
                peliID = peliID[:-4] + "--" + peliID[-2:]
            else:
                pelitilanne[7][2] = pelitilanne[7][4]
                pelitilanne[7][3] = pelitilanne[7][0]
                pelitilanne[7][4] = TYHJA
                pelitilanne[7][0] = TYHJA
                peliID = peliID[:-4] + "--" + peliID[-2:]
        else:
            if len(siirto) < 3:
                pelitilanne[0][6] = pelitilanne[0][4]
                pelitilanne[0][5] = pelitilanne[0][7]
                pelitilanne[0][4] = TYHJA
                pelitilanne[0][7] = TYHJA
                peliID = peliID[:-6] + "--" + peliID[-4:]
            else:
                pelitilanne[0][2] = pelitilanne[0][4]
                pelitilanne[0][3] = pelitilanne[0][0]
                pelitilanne[0][4] = TYHJA
                pelitilanne[0][0] = TYHJA
                peliID = peliID[:-6] + "--" + peliID[-4:]
    else:
        poistettu = pelitilanne[siirto[3]][siirto[2]]
        pelitilanne[siirto[3]][siirto[2]] = pelitilanne[siirto[1]][siirto[0]]
        if pelitilanne[siirto[1]][siirto[0]] == PELINAPPULAT[vuoro][1]:
            if vuoro == 0:
                if siirto[0] == 0:
                    peliID = peliID[:-3] + "-" + peliID[-2:]
                elif siirto[0] == 7:
                    peliID = peliID[:-4] + "-" + peliID[-3:]
            else:
                if siirto[0] == 0:
                    peliID = peliID[:-5] + "-" + peliID[-4:]
                elif siirto[0] == 7:
                    peliID = peliID[:-6] + "-" + peliID[-5:]
        elif pelitilanne[siirto[1]][siirto[0]] == PELINAPPULAT[vuoro][5]:
            if vuoro == 0:
                peliID = peliID[:-4] + "--" + peliID[-2:]
            else:
                peliID = peliID[:-6] + "--" + peliID[-4:]
        pelitilanne[siirto[1]][siirto[0]] = TYHJA
    return poistettu, peliID

def kone_peru(pelitilanne, siirto, nappula, vuoro):
    """Palauttaa siirron tekemät muutokset

    Args:
        pelitilanne list: PELILAUTA tapainen listojen lista hetkisestä pelitilanteesta
        siirto string: Siirto jonka perutaan
        nappula string: Nappula joka ruudun paikalla ennen oli, esim. tyhjän ruudun ollessa '-'
    """
    if len(siirto) > 4:
        pelitilanne[siirto[1]][siirto[0]] = PELINAPPULAT[vuoro][0]
        pelitilanne[siirto[3]][siirto[2]] = nappula
    elif len(siirto) < 4:
        if vuoro == 0:
            if len(siirto) < 3:
                pelitilanne[7][4] = pelitilanne[7][6]
                pelitilanne[7][7] = pelitilanne[7][5]
                pelitilanne[7][6] = TYHJA
                pelitilanne[7][5] = TYHJA
            else:
                pelitilanne[7][4] = pelitilanne[7][2]
                pelitilanne[7][0] = pelitilanne[7][3]
                pelitilanne[7][2] = TYHJA
                pelitilanne[7][3] = TYHJA
        else:
            if len(siirto) < 3:
                pelitilanne[0][4] = pelitilanne[0][6]
                pelitilanne[0][7] = pelitilanne[0][5]
                pelitilanne[0][6] = TYHJA
                pelitilanne[0][5] = TYHJA
            else:
                pelitilanne[0][4] = pelitilanne[0][2]
                pelitilanne[0][0] = pelitilanne[0][3]
                pelitilanne[0][2] = TYHJA
                pelitilanne[0][3] = TYHJA
    else:
        pelitilanne[siirto[1]][siirto[0]] = pelitilanne[siirto[3]][siirto[2]]
        pelitilanne[siirto[3]][siirto[2]] = nappula

def onko_shakki(pelitilanne, vuoro, peliID="------"):
    """Tarkistaa onko shakki, eli voiko vuorossa olevan pelaajan kuninkaan ruutuun hyökätä millään
    vastustajan napilla

    Args:
        pelitilanne list: PELILAUTA tapainen listojen lista hetkisestä pelitilanteesta
        vuoro int: kenen vuoro, 0 tai 1 arvona

    Returns:
        boolean: True jos on shakki, False jos ei ole
    """
    kingi = PELINAPPULAT[vuoro][5]
    temp = kone_ihan_kaikki_wt_siirrot(pelitilanne, peliID)
    if vuoro == 0:
        vastapuoli = temp[1]
    else:
        vastapuoli = temp[0]
    sijainti = (None, None)
    for y in range(8):
        for x in range(8):
            if pelitilanne[y][x] == kingi:
                sijainti = (x,y)
    for siirto in vastapuoli:
        if siirto[2] == sijainti[0] and siirto[3] == sijainti[1]:
            return True
    return False

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
                #-
                pass
            elif pelinappula == mustat[0]:
                #P
                if y < 7:
                    if pelitilanne[y+1][x] == TYHJA:
                        if y+1 == 7:
                            for nappi in mustat[:5]:
                                m_siirrot.append((x,y,x,y+1,nappi))
                        else:
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
                #R
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
                #N
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
                #B
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
                #Q
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
                #K
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
                            for nappi in valkoiset[:5]:
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
                #r
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
                #n
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
                #q
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
                #k
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

def kone_ihan_kaikki_wt_siirrot(pelitilanne, peliID="------"):
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
    mahdollisuudet = [False]*4
    nolla_hyokkaykset = [False]*8
    seitseman_hyokkaykset = [False]*8
    for y in range(8):
        for x in range(8):
            pelinappula = pelitilanne[y][x]
            if pelinappula == TYHJA:
                #-
                pass
            elif pelinappula == mustat[0]:
                #P
                if y < 7:
                    if pelitilanne[y+1][x] == TYHJA:
                        if y+1 == 7:
                            for nappi in mustat[:5]:
                                m_siirrot.append((x,y,x,y+1,nappi))
                        else:
                            m_siirrot.append((x,y,x,y+1))
                        if y == 1 and pelitilanne[y+2][x] == TYHJA:
                            m_siirrot.append((x,y,x,y+2))
                    if x > 0 and pelitilanne[y+1][x-1] not in mustat and pelitilanne[y+1][x-1] != TYHJA:
                        if pelitilanne[y+1][x-1] == valkoiset[5]:
                            v_shakki = True
                        if y+1 == 7:
                            seitseman_hyokkaykset[x-1] = True
                        m_siirrot.append((x,y,x-1,y+1))
                    if x < 7 and pelitilanne[y+1][x+1] not in mustat and pelitilanne[y+1][x+1] != TYHJA:
                        if pelitilanne[y+1][x+1] == valkoiset[5]:
                            v_shakki = True
                        if y+1 == 7:
                            seitseman_hyokkaykset[x+1] = True
                        m_siirrot.append((x,y,x+1,y+1))
            elif pelinappula == mustat[1]:
                #R
                for i in range(x+1, 8):
                    if pelitilanne[y][i] in mustat:
                        if pelitilanne[y][i] == mustat[5]:
                            mahdollisuudet[1] = True
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
                        if pelitilanne[y][i] == mustat[5]:
                            mahdollisuudet[0] = True
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
                        if i == 7:
                            seitseman_hyokkaykset[x] = True
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
                #N
                if y < 6 and x < 7 and pelitilanne[y+2][x+1] not in mustat:
                    if pelitilanne[y+2][x+1] == valkoiset[5]:
                        v_shakki = True
                    if y+2 == 7:
                        seitseman_hyokkaykset[x+1] = True
                    m_siirrot.append((x,y,x+1,y+2))
                if y < 6 and x > 0 and pelitilanne[y+2][x-1] not in mustat:
                    if pelitilanne[y+2][x-1] == valkoiset[5]:
                        v_shakki = True
                    if y+2 == 7:
                        seitseman_hyokkaykset[x-1] = True
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
                    if y+1 == 7:
                        seitseman_hyokkaykset[x+2] = True
                    m_siirrot.append((x,y,x+2,y+1))
                if y < 7 and x > 1 and pelitilanne[y+1][x-2] not in mustat:
                    if pelitilanne[y+1][x-2] == valkoiset[5]:
                        v_shakki = True
                    if y+1 == 7:
                        seitseman_hyokkaykset[x-2] = True
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
                #B
                for i in range(1,9):
                    if x+i > 7 or y+i > 7 or pelitilanne[y+i][x+i] in mustat:
                        break
                    if pelitilanne[y+i][x+i] == TYHJA:
                        if y+i == 7:
                            seitseman_hyokkaykset[x+i] = True
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
                        if y+i == 7:
                            seitseman_hyokkaykset[x-i] = True
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
                #Q
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
                        if i == 7:
                            seitseman_hyokkaykset[x] = True
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
                        if y+i == 7:
                            seitseman_hyokkaykset[x+i] = True
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
                        if y+i == 7:
                            seitseman_hyokkaykset[x-i] = True
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
                #K
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
                    if y+1 == 7:
                        seitseman_hyokkaykset[x] = True
                    m_siirrot.append((x,y,x,y+1))
                if y > 0 and pelitilanne[y-1][x] not in mustat:
                    if pelitilanne[y-1][x] == valkoiset[5]:
                        v_shakki = True
                    m_siirrot.append((x,y,x,y-1))
                if y < 7 and x < 7 and pelitilanne[y+1][x+1] not in mustat:
                    if pelitilanne[y+1][x+1] == valkoiset[5]:
                        v_shakki = True
                    if y+1 == 7:
                        seitseman_hyokkaykset[x+1] = True
                    m_siirrot.append((x,y,x+1,y+1))
                if y < 7 and x > 0 and pelitilanne[y+1][x-1] not in mustat:
                    if pelitilanne[y+1][x-1] == valkoiset[5]:
                        v_shakki = True
                    if y+1 == 7:
                        seitseman_hyokkaykset[x-1] = True
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
                            for nappi in valkoiset[:5]:
                                v_siirrot.append((x,y,x,y-1,nappi))
                        else:
                            v_siirrot.append((x,y,x,y-1))
                        if y == 6 and pelitilanne[y-2][x] == TYHJA:
                            v_siirrot.append((x,y,x,y-2))
                    if x > 0 and pelitilanne[y-1][x-1] not in valkoiset and pelitilanne[y-1][x-1] != TYHJA:
                        if pelitilanne[y-1][x-1] == mustat[5]:
                            m_shakki = True
                        if y-1 == 0:
                            nolla_hyokkaykset[x-1] = True
                        v_siirrot.append((x,y,x-1,y-1))
                    if x < 7 and pelitilanne[y-1][x+1] not in valkoiset and pelitilanne[y-1][x+1] != TYHJA:
                        if pelitilanne[y-1][x+1] == mustat[5]:
                            m_shakki = True
                        if y-1 == 0:
                            nolla_hyokkaykset[x+1] = True
                        v_siirrot.append((x,y,x+1,y-1))
            elif pelinappula == valkoiset[1]:
                #r
                for i in range(x+1, 8):
                    if pelitilanne[y][i] in valkoiset:
                        if pelitilanne[y][i] == valkoiset[5]:
                            mahdollisuudet[3] = True
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
                        if pelitilanne[y][i] == valkoiset[5]:
                            mahdollisuudet[2] = True
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
                        if i == 0:
                            nolla_hyokkaykset[x] = True
                        v_siirrot.append((x,y,x,i))
                    else:
                        if pelitilanne[i][x] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,x,i))
                        break
            elif pelinappula == valkoiset[2]:
                #n
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
                    if y-2 == 0:
                        nolla_hyokkaykset[x+1] = True
                    v_siirrot.append((x,y,x+1,y-2))
                if y > 1 and x > 0 and pelitilanne[y-2][x-1] not in valkoiset:
                    if pelitilanne[y-2][x-1] == mustat[5]:
                        m_shakki = True
                    if y-2 == 0:
                        nolla_hyokkaykset[x-1] = True
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
                    if y-1 == 0:
                        nolla_hyokkaykset[x+2] = True
                    v_siirrot.append((x,y,x+2,y-1))
                if y > 0 and x > 1 and pelitilanne[y-1][x-2] not in valkoiset:
                    if pelitilanne[y-1][x-2] == mustat[5]:
                        m_shakki = True
                    if y-1 == 0:
                            nolla_hyokkaykset[x-2] = True
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
                        if y-i == 0:
                            nolla_hyokkaykset[x+i] = True
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
                        if y-i == 0:
                            nolla_hyokkaykset[x-i] = True
                        v_siirrot.append((x,y,x-i,y-i))
                    else:
                        if pelitilanne[y-i][x-i] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,x-i,y-i))
                        break
            elif pelinappula == valkoiset[4]:
                #q
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
                        if i == 0:
                            nolla_hyokkaykset[x] = True
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
                        if y-i == 0:
                            nolla_hyokkaykset[x+i] = True
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
                        if y-i == 0:
                            nolla_hyokkaykset[x-i] = True
                        v_siirrot.append((x,y,x-i,y-i))
                    else:
                        if pelitilanne[y-i][x-i] == mustat[5]:
                            m_shakki = True
                        v_siirrot.append((x,y,x-i,y-i))
                        break
            elif pelinappula == valkoiset[5]:
                #k
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
                    if y-1 == 0:
                        nolla_hyokkaykset[x] = True
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
                    if y-1 == 0:
                        nolla_hyokkaykset[x+1] = True
                    v_siirrot.append((x,y,x+1,y-1))
                if y > 0 and x > 0 and pelitilanne[y-1][x-1] not in valkoiset:
                    if pelitilanne[y-1][x-1] == mustat[5]:
                        m_shakki = True
                    if y-1 == 0:
                        nolla_hyokkaykset[x-1] = True
                    v_siirrot.append((x,y,x-1,y-1))
    if peliID[-6] == "K" and mahdollisuudet[0] and not(nolla_hyokkaykset[4] or nolla_hyokkaykset[5] or nolla_hyokkaykset[6] or m_shakki):
        m_siirrot.append((0,0))
    if peliID[-5] == "Q" and mahdollisuudet[1] and not(nolla_hyokkaykset[2] or nolla_hyokkaykset[3] or nolla_hyokkaykset[4] or m_shakki):
        m_siirrot.append((0,0,0))
    if peliID[-4] == "k" and mahdollisuudet[2] and not(seitseman_hyokkaykset[4] or seitseman_hyokkaykset[5] or seitseman_hyokkaykset[6] or v_shakki):
        v_siirrot.append((0,0))
    if peliID[-3] == "q" and mahdollisuudet[3] and not(seitseman_hyokkaykset[2] or seitseman_hyokkaykset[3] or seitseman_hyokkaykset[4] or v_shakki):
        v_siirrot.append((0,0,0))
    return (v_siirrot, m_siirrot, v_shakki, m_shakki)
