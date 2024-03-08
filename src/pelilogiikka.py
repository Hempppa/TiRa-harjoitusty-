"""Vastuussa pelikentän muokkaamiseen(kone_siirto, kone_peru) ja tarkasteluun (matti, onko_shakki, kone_ihan_kaikki_wt_siirrot) liittyvät dunktiot. 
"""
PELINAPPULAT = [["p","r","n","b","q","k"],
                ["P","R","N","B","Q","K"]]
TYHJA = "-"

def matti(pelitilanne, vuoro, edellinen_siirto=(None,None,None,None), peli_id="------"):
    """Tarkistaa onko shakkimattia tai tasapeliä, samalla palauttaa kaikki todella mahdolliset siirrot (siirrot jotka vievät pois shakista) ja
    päivittää peli_id:n käyttöliittymälle, sillä kutsutaan muutenkin kone_ihan_kaikki_wt_siirrot.

    Args:
        pelitilanne list: lista pelilaudan rivejä edustavista listoista, edustaa pelilaudan hetkistä tilaa
        vuoro int: 0 jos valkoisen vuoro ja 1 muuten_
        edellinen_siirto (tuple, optional): sisältää edellisen siirron muodossa (x1,y1,x2,y2) eli esim. (2,2,2,4). Defaults to (None,None,None,None)
        peli_id (str, optional): pelikohtainen id viimeiset kuusi merkkiä määräävät ohestalyöntiä ja tornitusta. Defaults to "------".

    Returns:
        tuple: järjestyksessä (bool; onko matti?, list: lailliset siirrot, bool: onko tasapeli mahdollinen, str: uusittu peli_id)
    """
    mahdolliset = kone_ihan_kaikki_wt_siirrot(pelitilanne, edellinen_siirto, peli_id)
    uusittu = []
    tasapeli = not mahdolliset[vuoro+2]
    for siirto in mahdolliset[vuoro]:
        poistettu, peli_id = kone_siirto(pelitilanne, siirto, vuoro)
        if not onko_shakki(pelitilanne, vuoro, siirto, peli_id):
            uusittu.append(siirto)
        kone_peru(pelitilanne, siirto, poistettu, vuoro)
    if len(uusittu) == 0:
        return True, uusittu, tasapeli, mahdolliset[4]
    return False, uusittu, tasapeli, mahdolliset[4]

def kone_siirto(pelitilanne, siirto, vuoro, peli_id="------"):
    """Tekee siirron pelilaudalle. 
    Normi siirrot muodossa (x1,y1,x2,y2), 
    tornitus '00' / '000', tai (0,0) / (0,0,0)
    ohestalyönti (x1,y1,x2,y2,'en'), 
    korotus (x1,y1,x2,y2,'Q')

    Args:
        pelitilanne list: lista pelilaudan rivejä edustavista listoista
        siirto tuple: siirto joka toteutetaan. Ylläolevan tapaiset sallittu
        vuoro int: 0 jos valkoisen vuoro, muuten 1
        peli_id (str, optional): pelikohtainen id joka määrää ohestalyöntiä ja tornitusta. Defaults to "------".

    Returns:
        tuple: (str: poistettu nappula, str: päivitetty id)
    """
    if len(siirto) > 4:
        if siirto[4] == "en":
            if vuoro == 0:
                poistettu = pelitilanne[siirto[3]+1][siirto[2]]
                pelitilanne[siirto[3]+1][siirto[2]] = TYHJA
                pelitilanne[siirto[3]][siirto[2]] = pelitilanne[siirto[1]][siirto[0]]
                pelitilanne[siirto[1]][siirto[0]] = TYHJA
            else:
                poistettu = pelitilanne[siirto[3]-1][siirto[2]]
                pelitilanne[siirto[3]-1][siirto[2]] = TYHJA
                pelitilanne[siirto[3]][siirto[2]] = pelitilanne[siirto[1]][siirto[0]]
                pelitilanne[siirto[1]][siirto[0]] = TYHJA
        else:
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
                peli_id = peli_id[:-4] + "--" + peli_id[-2:]
            else:
                pelitilanne[7][2] = pelitilanne[7][4]
                pelitilanne[7][3] = pelitilanne[7][0]
                pelitilanne[7][4] = TYHJA
                pelitilanne[7][0] = TYHJA
                peli_id = peli_id[:-4] + "--" + peli_id[-2:]
        else:
            if len(siirto) < 3:
                pelitilanne[0][6] = pelitilanne[0][4]
                pelitilanne[0][5] = pelitilanne[0][7]
                pelitilanne[0][4] = TYHJA
                pelitilanne[0][7] = TYHJA
                peli_id = peli_id[:-6] + "--" + peli_id[-4:]
            else:
                pelitilanne[0][2] = pelitilanne[0][4]
                pelitilanne[0][3] = pelitilanne[0][0]
                pelitilanne[0][4] = TYHJA
                pelitilanne[0][0] = TYHJA
                peli_id = peli_id[:-6] + "--" + peli_id[-4:]
    else:
        poistettu = pelitilanne[siirto[3]][siirto[2]]
        pelitilanne[siirto[3]][siirto[2]] = pelitilanne[siirto[1]][siirto[0]]
        if pelitilanne[siirto[1]][siirto[0]] == PELINAPPULAT[vuoro][1]:
            if vuoro == 0:
                if siirto[0] == 0:
                    peli_id = peli_id[:-3] + "-" + peli_id[-2:]
                elif siirto[0] == 7:
                    peli_id = peli_id[:-4] + "-" + peli_id[-3:]
            else:
                if siirto[0] == 0:
                    peli_id = peli_id[:-5] + "-" + peli_id[-4:]
                elif siirto[0] == 7:
                    peli_id = peli_id[:-6] + "-" + peli_id[-5:]
        elif pelitilanne[siirto[1]][siirto[0]] == PELINAPPULAT[vuoro][5]:
            if vuoro == 0:
                peli_id = peli_id[:-4] + "--" + peli_id[-2:]
            else:
                peli_id = peli_id[:-6] + "--" + peli_id[-4:]
        pelitilanne[siirto[1]][siirto[0]] = TYHJA
    peli_id = peli_id[:-2] + "--"
    return poistettu, peli_id

def kone_peru(pelitilanne, siirto, nappula, vuoro):
    """Peruuttaa kone_siirto tekemät muutokset

    Args:
        pelitilanne list: lista pelilaudan riveistä
        siirto str: siirto jonka vaikutus perutaan
        nappula str: nappula joka siirron mukana poistettiin
        vuoro int: 0 jos valkoisen vuoro, muuten 1
    """
    if len(siirto) > 4:
        if siirto[4] == "en":
            if vuoro == 0:
                pelitilanne[siirto[3]+1][siirto[2]] = nappula
                pelitilanne[siirto[1]][siirto[0]] = pelitilanne[siirto[3]][siirto[2]]
                pelitilanne[siirto[3]][siirto[2]] = TYHJA
            else:
                pelitilanne[siirto[3]-1][siirto[2]] = nappula
                pelitilanne[siirto[1]][siirto[0]] = pelitilanne[siirto[3]][siirto[2]]
                pelitilanne[siirto[3]][siirto[2]] = TYHJA
        else:
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

def onko_shakki(pelitilanne, vuoro, edellinen_siirto=(None,None,None,None), peli_id="------"):
    """Tarkistaa onko shakki, eli hyokätäänkö vuorolla osoitetun pelaajan kuningasta millään.

    Args:
        pelitilanne list: lista pelilaudan riveistä
        vuoro int: 0 jos valkoisen vuoro, muuten 1
        edellinen_siirto (tuple, optional): viimeisin kone_siirrolla suoritettu siirto ennen funktion kutsua. Defaults to (None,None,None,None).
        peli_id (str, optional): pelikohtainen id, tarvitaan mahdollisten siirtojen laskemiseen. Defaults to "------".

    Returns:
        bool: True jos on shakki ja False muuten
    """
    kingi = PELINAPPULAT[vuoro][5]
    temp = kone_ihan_kaikki_wt_siirrot(pelitilanne, edellinen_siirto, peli_id)
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

def kone_ihan_kaikki_wt_siirrot(pelitilanne, edellinen_siirto=(None,None,None,None), peli_id="------"):
    """Kummallinen nimi, mutta palauttaa valkoisen ja mustan siirrot sekä tiedon siitä onko kumpikaan kuningas shakissa sekä päivittää 
    en passant ruudun peli_idehen

    Args:
        pelitilanne list: lista pelilaudan riveistä
        edellinen_siirto (tuple, optional): viimeisin kone_siirrolla suoritettu siirto ennen funktion kutsua, en passant laskentaan. 
            Defaults to (None,None,None,None).
        peli_id (str, optional): päivitetty pelikohtainen id. Defaults to "------".

    Returns:
        list: [list: valkoisen siirrot, list: mustan siirrot, bool: onko valkoinen shakissa, bool: onko musta shakissa]
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
                    if x > 0 and pelitilanne[y+1][x-1] not in mustat:
                        if pelitilanne[y+1][x-1] == TYHJA:
                            if y+1 == 7:
                                seitseman_hyokkaykset[x-1] = True
                            elif y == 4 and edellinen_siirto == (x-1, 6, x-1, 4) and pelitilanne[4][x-1] == valkoiset[0]:
                                m_siirrot.append((x,y,x-1,y+1,"en"))
                                peli_id = peli_id[:-2] + str(x-1) + str(y+1)
                        else:
                            if pelitilanne[y+1][x-1] == valkoiset[5]:
                                v_shakki = True
                            if y+1 == 7:
                                for nappi in mustat[:5]:
                                    m_siirrot.append((x,y,x-1,y+1,nappi))
                            else:
                                m_siirrot.append((x,y,x-1,y+1))
                    if x < 7 and pelitilanne[y+1][x+1] not in mustat:
                        if pelitilanne[y+1][x+1] == TYHJA:
                            if y+1 == 7:
                                seitseman_hyokkaykset[x+1] = True
                            elif y == 4 and edellinen_siirto == (x+1, 6, x+1, 4) and pelitilanne[4][x+1] == valkoiset[0]:
                                peli_id = peli_id[:-2] + str(x+1) + str(y+1)
                                m_siirrot.append((x,y,x+1,y+1,"en"))
                        else:
                            if pelitilanne[y+1][x+1] == valkoiset[5]:
                                v_shakki = True
                            if y+1 == 7:
                                for nappi in mustat[:5]:
                                    m_siirrot.append((x,y,x+1,y+1,nappi))
                            else:
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
                    if x > 0 and pelitilanne[y-1][x-1] not in valkoiset:
                        if pelitilanne[y-1][x-1] == TYHJA:
                            if y-1 == 0:
                                nolla_hyokkaykset[x-1] = True
                            elif y == 3 and edellinen_siirto == (x-1, 1, x-1, 3) and pelitilanne[3][x-1] == mustat[0]:
                                v_siirrot.append((x,y,x-1,y-1,"en"))
                                peli_id = peli_id[:-2] + str(x-1) + str(y-1)
                        else:
                            if pelitilanne[y-1][x-1] == mustat[5]:
                                m_shakki = True
                            if y-1 == 0:
                                for nappi in valkoiset[:5]:
                                    v_siirrot.append((x,y,x-1,y-1,nappi))
                            else:
                                v_siirrot.append((x,y,x-1,y-1))
                            v_siirrot.append((x,y,x-1,y-1))
                    if x < 7 and pelitilanne[y-1][x+1] not in valkoiset:
                        if pelitilanne[y-1][x+1] == TYHJA:
                            if y-1 == 0:
                                nolla_hyokkaykset[x+1] = True
                            elif y == 3 and edellinen_siirto == (x+1, 1, x+1, 3) and pelitilanne[3][x+1] == mustat[0]:
                                v_siirrot.append((x,y,x+1,y-1,"en"))
                                peli_id = peli_id[:-2] + str(x+1) + str(y-1)
                        else:
                            if pelitilanne[y-1][x+1] == valkoiset[5]:
                                m_shakki = True
                            if y-1 == 0:
                                for nappi in valkoiset[:5]:
                                    v_siirrot.append((x,y,x+1,y-1,nappi))
                            else:
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
    #Lisää tornituksen siirrot
    if peli_id[-6] == "K" and mahdollisuudet[0] and not(nolla_hyokkaykset[4] or nolla_hyokkaykset[5] or nolla_hyokkaykset[6] or m_shakki):
        m_siirrot.append((0,0))
    if peli_id[-5] == "Q" and mahdollisuudet[1] and not(nolla_hyokkaykset[2] or nolla_hyokkaykset[3] or nolla_hyokkaykset[4] or m_shakki):
        m_siirrot.append((0,0,0))
    if peli_id[-4] == "k" and mahdollisuudet[2] and not(seitseman_hyokkaykset[4] or seitseman_hyokkaykset[5] or seitseman_hyokkaykset[6] or v_shakki):
        v_siirrot.append((0,0))
    if peli_id[-3] == "q" and mahdollisuudet[3] and not(seitseman_hyokkaykset[2] or seitseman_hyokkaykset[3] or seitseman_hyokkaykset[4] or v_shakki):
        v_siirrot.append((0,0,0))
    return (v_siirrot, m_siirrot, v_shakki, m_shakki, peli_id)
