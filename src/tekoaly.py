from pelilogiikka import kone_peru, kone_siirto, kone_ihan_kaikki_wt_siirrot
PELINAPPULAT = [["p","r","n","b","q","k"],
                ["P","R","N","B","Q","K"]]
TYHJA = "-"

def arvioi_tilanne(pelitilanne, siirrot=None, shakit=None, peliID="KQkq--"):
    """Heuristinen funktio arvioimaan pelitilannetta, funktio on kevyt ja palauttaa siis vain tämän hetkisen pelitilanteen arvion,
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
        siirrot_v, siirrot_b, shakit_v, shakit_b = kone_ihan_kaikki_wt_siirrot(pelitilanne, peliID)
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
                if not ((x > 0 and pelitilanne[y-1][x-1] == PELINAPPULAT[0][0]) or (x < 7 and pelitilanne[y-1][x+1] == PELINAPPULAT[0][0])):
                    isolated_v += 100
                if y < 7 and pelitilanne[y+1][x] != TYHJA:
                    blocked_v += 100
                advancing_v += 10*(6-y)-abs(10*x-35)
            elif pelitilanne[y][x] == PELINAPPULAT[1][0]:
                materiaali -= 100
                doubled_b.add(x)
                if not ((x > 0 and pelitilanne[y-1][x-1] == PELINAPPULAT[1][0]) or (x < 7 and pelitilanne[y-1][x+1] == PELINAPPULAT[1][0])):
                    isolated_b += 100
                if y > 0 and pelitilanne[y-1][x] != TYHJA:
                    blocked_b += 100
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

def tekoalya(pelitilanne, syvyys, alpha, beta, vuoro, edellinen_siirto, siirto_taulu, vanhaID):
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
    if syvyys == 0 or -25000 > edellinen_siirto[0] or edellinen_siirto[0] > 25000:
        return edellinen_siirto
    kaikki_siirrot = kone_ihan_kaikki_wt_siirrot(pelitilanne, vanhaID)
    #pelitilanne kohtainen uniikki merkkijono
    uusiID = update_FEN(pelitilanne, vuoro, vanhaID)
    paras = (0,"")
    if uusiID in siirto_taulu:
        paras = siirto_taulu[uusiID]
    #
    arviot = []
    for siirto in kaikki_siirrot[vuoro]:
        #Jätetään paras siirto pois jotta ei arvioida kahdesti
        if siirto == paras[1]:
            pass
            #
        else:
            if syvyys > 1:
                nappula, tempID = kone_siirto(pelitilanne, siirto, vuoro, uusiID)
                arviot.append((arvioi_tilanne(pelitilanne, [kaikki_siirrot[0], kaikki_siirrot[1]], [kaikki_siirrot[2], kaikki_siirrot[3]], tempID)*(-1), siirto))
                kone_peru(pelitilanne, siirto, nappula, vuoro)
            else:
                nappula, tempID = kone_siirto(pelitilanne, siirto, vuoro, uusiID)
                arviot.append((arvioi_tilanne(pelitilanne, [], [], tempID)*(-1), siirto))
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
            nappula, tempID = kone_siirto(pelitilanne, siirto[1], vuoro, uusiID)
            temp = tekoalya(pelitilanne, syvyys-1, alpha, beta, 0, (siirto[0], siirto[1]), siirto_taulu, tempID)
            kone_peru(pelitilanne, siirto[1], nappula, vuoro)
            if temp[0] > arvo[0]:
                arvo = (temp[0], siirto[1])
            alpha = max(arvo[0], alpha)
            if arvo[0] >= beta:
                break
        #Tallennetaan arvo tauluun
        siirto_taulu[uusiID] = arvo
        #
        return arvo
    else:
        arviot.sort(reverse=True)
        arvo = (500000, "")
        if paras[1] != "":
            arviot.append(paras)
        for i in range(len(arviot)):
            siirto = arviot[-i]
            nappula, tempID = kone_siirto(pelitilanne, siirto[1], vuoro, uusiID)
            temp = tekoalya(pelitilanne, syvyys-1, alpha, beta, 1, (siirto[0], siirto[1]), siirto_taulu, tempID)
            kone_peru(pelitilanne, siirto[1], nappula, vuoro)
            if temp[0] < arvo[0]:
                arvo = (temp[0], siirto[1])
            beta = max(arvo[0], beta)
            if arvo[0] <= alpha:
                break
        siirto_taulu[uusiID] = arvo
        return arvo

def tekoalyb(pelitilanne, syvyys, alpha, beta, vuoro, edellinen_siirto, siirto_taulu, vanhaID):
    """Sama kuin tekoalya mutta pelaa valkoisilla napeilla, varmaan lopullisessa versiossa yhdistän nämä.
    """
    if syvyys == 0 or -25000 > edellinen_siirto[0] or edellinen_siirto[0] > 25000:
        return edellinen_siirto
    kaikki_siirrot = kone_ihan_kaikki_wt_siirrot(pelitilanne, vanhaID)
    if vuoro == 0 and kaikki_siirrot[3]:
        return (50000, edellinen_siirto[1])
    elif kaikki_siirrot[2]:
        return (-50000, edellinen_siirto[1])
    arviot = []
    uusiID = update_FEN(pelitilanne, vuoro, vanhaID)
    paras = (0,"")
    if uusiID in siirto_taulu:
        paras = siirto_taulu[uusiID]
    for siirto in kaikki_siirrot[vuoro]:
        if siirto == paras[1]:
            pass
        else:
            if syvyys > 1:
                nappula, tempID = kone_siirto(pelitilanne, siirto, vuoro, uusiID)
                arviot.append((arvioi_tilanne(pelitilanne, [kaikki_siirrot[0], kaikki_siirrot[1]], [kaikki_siirrot[2], kaikki_siirrot[3]], tempID), siirto))
                kone_peru(pelitilanne, siirto, nappula, vuoro)
            else:
                nappula, tempID = kone_siirto(pelitilanne, siirto, vuoro, uusiID)
                arviot.append((arvioi_tilanne(pelitilanne, [], [], tempID), siirto))
                kone_peru(pelitilanne, siirto, nappula, vuoro)
    if vuoro == 0:
        arviot.sort()
        arvo = (-500000,"")
        if paras[1] != "":
            arviot.append(paras)
        for i in range(len(arviot)):
            siirto = arviot[-i]
            nappula, tempID = kone_siirto(pelitilanne, siirto[1], vuoro, uusiID)
            temp = tekoalyb(pelitilanne, syvyys-1, alpha, beta, 1, (siirto[0], siirto[1]), siirto_taulu, tempID)
            kone_peru(pelitilanne, siirto[1], nappula, vuoro)
            if temp[0] > arvo[0]:
                arvo = (temp[0], siirto[1])
            alpha = max(arvo[0], alpha)
            if arvo[0] >= beta:
                break
        siirto_taulu[uusiID] = arvo
        return arvo
    else:
        arviot.sort(reverse=True)
        arvo = (500000, "")
        if paras[1] != "":
            arviot.append(paras)
        for i in range(len(arviot)):
            siirto = arviot[-i]
            nappula, tempID = kone_siirto(pelitilanne, siirto[1], vuoro, uusiID)
            temp = tekoalyb(pelitilanne, syvyys-1, alpha, beta, 0, (siirto[0], siirto[1]), siirto_taulu, tempID)
            kone_peru(pelitilanne, siirto[1], nappula, vuoro)
            if temp[0] < arvo[0]:
                arvo = (temp[0], siirto[1])
            beta = max(arvo[0], beta)
            if arvo[0] <= alpha:
                break
        siirto_taulu[uusiID] = arvo
        return arvo

def update_FEN(pelitilanne, vuoro, peliID):
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
    return merkkijono + peliID[-6:]