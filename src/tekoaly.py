from pelilogiikka import kone_peru, kone_siirto, kone_ihan_kaikki_wt_siirrot
PELINAPPULAT = [["p","r","n","b","q","k"],
                ["P","R","N","B","Q","K"]]
TYHJA = "-"

def arvioi_tilanne(pelitilanne, edellinen_siirto=(None,None,None,None), siirrot=None, shakit=None, peli_id="-----"):
    """Heuristinen funktio arvioimaan pelitilannetta, funktio on kevyt ja palauttaa siis vain tämän hetkisen pelitilanteen arvion,
    eli ei osaa mm. ennustaa shakkia. Funktio on hetkellä myös aika yksinkertainen, se ottaa huomioon vain materiaalin,
    mahdollisten siirtojen ja huonossa asemassa olevien sotilaiden määrät sekä shakki tilanteen.

    Args:
        pelitilanne list: lista pelilaudan riveistä
        edellinen_siirto (tuple, optional): viimeisin suoritettu siirto, en passantin laskentaan. Defaults to (None,None,None,None).
        siirrot (list, optional): [list: valkoisen siirrot, list: mustan siirrot]. Defaults to None.
        shakit (list, optional): [bool: onko valkoinen shakissa, bool: onko musta shakissa]. Defaults to None.
        peli_id (str, optional): pelikohtainen id tornituksen laskentaan. Defaults to "------".

    Returns:
        int: arvio pelitilanteesta, positiivinen jos valkoinen voittaa ja negatiivinen jos musta. centipawneissa eli sadasosa sotilaanarvosta.
    """
    materiaalipaino = 1
    sotilaspaino = 0.5
    siirtoja_paino = 5
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
    if not siirrot or not shakit:
        siirrot_v, siirrot_b, shakit_v, shakit_b, peli_id = kone_ihan_kaikki_wt_siirrot(pelitilanne, edellinen_siirto, peli_id)
    else:
        siirrot_v = siirrot[0]
        siirrot_b = siirrot[1]
        shakit_v = shakit[0]
        shakit_b = shakit[1]
    for x in range(8):
        for y in range(8):
            if pelitilanne[y][x] == TYHJA:
                continue
            if pelitilanne[y][x] == PELINAPPULAT[0][0]:
                materiaali += 100
                doubled_v.add(x)
                if not ((x > 0 and pelitilanne[y+1][x-1] == PELINAPPULAT[0][0]) or (x < 7 and pelitilanne[y+1][x+1] == PELINAPPULAT[0][0])):
                    isolated_v += 10
                if y < 7 and pelitilanne[y+1][x] != TYHJA:
                    blocked_v += 20
                advancing_v += 10*(6-y)-abs(10*x-35)
            elif pelitilanne[y][x] == PELINAPPULAT[1][0]:
                materiaali -= 100
                doubled_b.add(x)
                if not ((x > 0 and pelitilanne[y-1][x-1] == PELINAPPULAT[1][0]) or (x < 7 and pelitilanne[y-1][x+1] == PELINAPPULAT[1][0])):
                    isolated_b += 10
                if y > 0 and pelitilanne[y-1][x] != TYHJA:
                    blocked_b += 20
                advancing_b += 10*(y-1)-abs(10*x-35)
            elif pelitilanne[y][x] == PELINAPPULAT[0][3]:
                materiaali += 300
            elif pelitilanne[y][x] == PELINAPPULAT[1][3]:
                materiaali -= 300
            elif pelitilanne[y][x] == PELINAPPULAT[0][2]:
                materiaali += 300
            elif pelitilanne[y][x] == PELINAPPULAT[1][2]:
                materiaali -= 300
            elif pelitilanne[y][x] == PELINAPPULAT[0][1]:
                materiaali += 500
            elif pelitilanne[y][x] == PELINAPPULAT[1][1]:
                materiaali -= 500
            elif pelitilanne[y][x] == PELINAPPULAT[0][4]:
                materiaali += 900
            elif pelitilanne[y][x] == PELINAPPULAT[1][4]:
                materiaali -= 900
            elif pelitilanne[y][x] == PELINAPPULAT[0][5]:
                materiaali += 50000
                if shakit_v:
                    kuninkaan_uhka_v += 100
            elif pelitilanne[y][x] == PELINAPPULAT[1][5]:
                materiaali -= 50000
                if shakit_b:
                    kuninkaan_uhka_b += 100
    arvio = materiaali*materiaalipaino
    arvio -= (len(doubled_b)*100-len(doubled_v)*100+isolated_v-isolated_b+blocked_v-blocked_b+advancing_v-advancing_b)*sotilaspaino
    arvio += (len(siirrot_v)-len(siirrot_b))*siirtoja_paino
    arvio += (kuninkaan_uhka_b-kuninkaan_uhka_v)*kuninkaan_uhka_paino
    return arvio

def tekoalya(pelitilanne, syvyys, alpha, beta, vuoro, edellinen_siirto, siirto_taulu, vanha_id, edelliset_shakit = [False, False]):
    """Rekursiivinen funktio laskemaan paras siirto kun tekoälyn siirrolla tilanteen arvo maksimoidaan ja pelaajan vuorolla minimoidaan
    (shakkibotin suhteen). laskee mahdollisten siirtojen arvot joka askeleella, jolloin todennäköisesti karsitaan enemmän siirtoja.

    Args:
        pelitilanne list: pelilaudan esitelmä
        syvyys int: kuinka monta siirtoa eteenpäin lasketaan, kannattaa olla 4 tai suurempi
        alpha int: alpha karsintaan, ikään kuin siirron arvon yläraja.
        beta int: beta karsintaan, ikään kuin siirron arvon alaraja
        vuoro int: 0 jos valkoisen vuoro, 1 muuten
        edellinen_siirto tuple: viimeisin suoritettu siirto, hyödyllinen en passantin laskemiseen
        siirto_taulu dict: taulu johon talletetaan kaikki arvioidut tilanteet, hyödyllinen iteratiivisen syvenemisen kanssa 
        vanha_id str: peli_id ennen funktion kutsua.
        edelliset_shakit (list, optional): tieto oliko viime kutsulla shakkeja, auttaa katkaisemaan turhaa laskentaa. Defaults to [False, False].

    Returns:
        tuple: (int: siirron arvo, str: varsinainen botin laskema paras siirto)
    """
    if syvyys == 0 or -25000 > edellinen_siirto[0] or edellinen_siirto[0] > 25000:
        return edellinen_siirto
    siirrot = kone_ihan_kaikki_wt_siirrot(pelitilanne, edellinen_siirto[1], vanha_id)
    if siirrot[3] and edelliset_shakit[1]:
        return -50000, edellinen_siirto[1]
    if siirrot[2] and edelliset_shakit[0]:
        return 50000, edellinen_siirto[1]
    #pelitilanne kohtainen uniikki merkkijono
    uusi_id = update_fen(pelitilanne, vuoro, siirrot[4])
    paras = (0,"")
    if uusi_id in siirto_taulu:
        paras = siirto_taulu[uusi_id]
    #
    arviot = []
    for siirto in siirrot[vuoro]:
        #Jätetään paras siirto pois jotta ei arvioida kahdesti
        if siirto == paras[1]:
            pass
            #
        else:
            if syvyys > 1:
                nappula, temp_id = kone_siirto(pelitilanne, siirto, vuoro, uusi_id)
                arviot.append((
                    arvioi_tilanne(pelitilanne, siirto, [siirrot[0], siirrot[1]], [siirrot[2], siirrot[3]], temp_id)*(-1),
                    siirto
                    ))
                kone_peru(pelitilanne, siirto, nappula, vuoro)
            else:
                nappula, temp_id = kone_siirto(pelitilanne, siirto, vuoro, uusi_id)
                arviot.append((arvioi_tilanne(pelitilanne, siirto, [], [], temp_id)*(-1), siirto))
                kone_peru(pelitilanne, siirto, nappula, vuoro)
    if vuoro == 1:
        arviot.sort()
        arvo = (-500000,"")
        #Siirretään paras siirto ensimmäiseksi jos löytyi
        if paras[1] != "":
            arviot.append(paras)
        #
        for i in range(len(arviot)):
            siirto = arviot[-i]
            nappula, temp_id = kone_siirto(pelitilanne, siirto[1], vuoro, uusi_id)
            temp = tekoalya(pelitilanne, syvyys-1, alpha, beta, 0, (siirto[0], siirto[1]), siirto_taulu, temp_id, [siirrot[2], siirrot[3]])
            kone_peru(pelitilanne, siirto[1], nappula, vuoro)
            if temp[0] > arvo[0]:
                arvo = (temp[0], siirto[1])
            alpha = max(arvo[0], alpha)
            if arvo[0] >= beta:
                break
        #Tallennetaan arvo tauluun
        siirto_taulu[uusi_id] = arvo
        #
        return arvo
    else:
        arviot.sort(reverse=True)
        arvo = (500000, "")
        if paras[1] != "":
            arviot.append(paras)
        for i in range(len(arviot)):
            siirto = arviot[-i]
            nappula, temp_id = kone_siirto(pelitilanne, siirto[1], vuoro, uusi_id)
            temp = tekoalya(pelitilanne, syvyys-1, alpha, beta, 1, (siirto[0], siirto[1]), siirto_taulu, temp_id, [siirrot[2], siirrot[3]])
            kone_peru(pelitilanne, siirto[1], nappula, vuoro)
            if temp[0] < arvo[0]:
                arvo = (temp[0], siirto[1])
            beta = max(arvo[0], beta)
            if arvo[0] <= alpha:
                break
        siirto_taulu[uusi_id] = arvo
        return arvo

def tekoalyb(pelitilanne, syvyys, alpha, beta, vuoro, edellinen_siirto, siirto_taulu, vanha_id, edelliset_shakit=[False, False]):
    """Sama kuin tekoalya mutta pelaa valkoisilla napeilla, eli palauttaa siihen nähden vastustajan siirtoja ja käänteisen siirron arvon.
    """
    if syvyys == 0 or -25000 > edellinen_siirto[0] or edellinen_siirto[0] > 25000:
        return edellinen_siirto
    siirrot = kone_ihan_kaikki_wt_siirrot(pelitilanne, edellinen_siirto[1], vanha_id)
    if siirrot[3] and edelliset_shakit[1]:
        return 50000, edellinen_siirto[1]
    if siirrot[2] and edelliset_shakit[0]:
        return -50000, edellinen_siirto[1]
    arviot = []
    uusi_id = update_fen(pelitilanne, vuoro, siirrot[4])
    paras = (0,"")
    if uusi_id in siirto_taulu:
        paras = siirto_taulu[uusi_id]
    for siirto in siirrot[vuoro]:
        if siirto == paras[1]:
            pass
        else:
            if syvyys > 1:
                nappula, temp_id = kone_siirto(pelitilanne, siirto, vuoro, uusi_id)
                arviot.append((arvioi_tilanne(pelitilanne, siirto, [siirrot[0], siirrot[1]], [siirrot[2], siirrot[3]], temp_id), siirto))
                kone_peru(pelitilanne, siirto, nappula, vuoro)
            else:
                nappula, temp_id = kone_siirto(pelitilanne, siirto, vuoro, uusi_id)
                arviot.append((arvioi_tilanne(pelitilanne, siirto, [], [], temp_id), siirto))
                kone_peru(pelitilanne, siirto, nappula, vuoro)
    if vuoro == 0:
        arviot.sort()
        arvo = (-500000,"")
        if paras[1] != "":
            arviot.append(paras)
        for i in range(len(arviot)):
            siirto = arviot[-i]
            nappula, temp_id = kone_siirto(pelitilanne, siirto[1], vuoro, uusi_id)
            temp = tekoalyb(pelitilanne, syvyys-1, alpha, beta, 1, (siirto[0], siirto[1]), siirto_taulu, temp_id, [siirrot[2], siirrot[3]])
            kone_peru(pelitilanne, siirto[1], nappula, vuoro)
            if temp[0] > arvo[0]:
                arvo = (temp[0], siirto[1])
            alpha = max(arvo[0], alpha)
            if arvo[0] >= beta:
                break
        siirto_taulu[uusi_id] = arvo
        return arvo
    else:
        arviot.sort(reverse=True)
        arvo = (500000, "")
        if paras[1] != "":
            arviot.append(paras)
        for i in range(len(arviot)):
            siirto = arviot[-i]
            nappula, temp_id = kone_siirto(pelitilanne, siirto[1], vuoro, uusi_id)
            temp = tekoalyb(pelitilanne, syvyys-1, alpha, beta, 0, (siirto[0], siirto[1]), siirto_taulu, temp_id, [siirrot[2], siirrot[3]])
            kone_peru(pelitilanne, siirto[1], nappula, vuoro)
            if temp[0] < arvo[0]:
                arvo = (temp[0], siirto[1])
            beta = max(arvo[0], beta)
            if arvo[0] <= alpha:
                break
        siirto_taulu[uusi_id] = arvo
        return arvo

def update_fen(pelitilanne, vuoro, peli_id):
    """Funktio päivittämään peli_id. Nimen mukaan inspiraatiota saatu FEN jonoista, mutta yksinkertaistetumpi versio. 
    Funktio päivittää vain pelilaudasta vastaavan osan, kone_siirto ja kone_ihan_kaikki_wt_siirrot hoitaa lopun.

    Args:
        pelitilanne list: lista listoista joissa pelimerkit
        vuoro int: 0 jos valkoisen vuoro, 1 muuten
        peli_id str: pelikohtainen id jota päivitetään.

    Returns:
        str: päivitetty peli_id
    """
    #koska tarvitaan vain siirtojen kannalta uniikki merkkijono niin voidaan yksinkertaistaa
    merkkijono = ""
    tyhjia = 0
    for y in range(8):
        for x in range(8):
            if pelitilanne[y][x] == TYHJA:
                tyhjia += 1
            else:
                if tyhjia > 0:
                    merkkijono += str(tyhjia)
                    tyhjia = 0
                merkkijono += pelitilanne[y][x]
    merkkijono += str(vuoro)
    return merkkijono + peli_id[-6:]
