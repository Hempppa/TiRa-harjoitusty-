from pelilogiikka import kone_kaikki_siirrot, kone_peru, kone_siirto

def arvioi_tilanne(pelitilanne, siirrot=None, vuoro=0):
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
                materiaali += 50000
                for siirto in siirrot_b:
                    if siirto[2] == x and siirto[3] == y:
                        kuninkaan_uhka_v += 100
            elif pelitilanne[y][x] == chr(9818):
                materiaali -= 50000
                for siirto in siirrot_v:
                    if siirto[2] == x and siirto[3] == y:
                        kuninkaan_uhka_b += 100
    arvio = materiaali*materiaalipaino
    arvio -= (len(doubled_b)*100-len(doubled_v)*100+isolated_v-isolated_b+blocked_v-blocked_b+advancing_v-advancing_b)*sotilaspaino
    arvio += (len(siirrot_v)-len(siirrot_b))*siirtoja_paino
    arvio -= (kuninkaan_uhka_b-kuninkaan_uhka_v)*kuninkaan_uhka_paino
    return arvio

def tekoalya(pelitilanne, syvyys, alpha, beta, vuoro, edellinen_siirto, siirto_taulu):
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
    siirrot = kone_kaikki_siirrot(pelitilanne, vuoro)
    fenJono = pelitilanne_to_simplified_FEN(pelitilanne, vuoro)
    paras = (0,"")
    if fenJono in siirto_taulu:
        paras = siirto_taulu[fenJono]
    arviot = []
    for siirto in siirrot:
        if siirto == paras[1]:
            pass
        else:
            nappula = kone_siirto(pelitilanne, siirto, vuoro)
            arviot.append((arvioi_tilanne(pelitilanne, siirrot, vuoro)*(-1), siirto))
            kone_peru(pelitilanne, siirto, nappula, vuoro)
    if vuoro == 1:
        arviot.sort(reverse=True)
        arvo = (-500000,"")
        if paras[1] != "":
            arviot = [paras]+arviot
        for siirto in arviot:
            nappula = kone_siirto(pelitilanne, siirto[1], vuoro)
            temp = tekoalya(pelitilanne, syvyys-1, alpha, beta, 0, (siirto[0], siirto[1]), siirto_taulu)
            kone_peru(pelitilanne, siirto[1], nappula, vuoro)
            if temp[0] > arvo[0]:
                arvo = (temp[0], siirto[1])
            alpha = max(arvo[0], alpha)
            if arvo[0] >= beta:
                break
        siirto_taulu[fenJono] = arvo
        return arvo
    else:
        arviot.sort()
        arvo = (500000, "")
        if paras[1] != "":
            arviot = [paras]+arviot
        for siirto in arviot:
            nappula = kone_siirto(pelitilanne, siirto[1], vuoro)
            temp = tekoalya(pelitilanne, syvyys-1, alpha, beta, 1, (siirto[0], siirto[1]), siirto_taulu)
            if temp[0] < arvo[0]:
                arvo = (temp[0], siirto[1])
            kone_peru(pelitilanne, siirto[1], nappula, vuoro)
            beta = max(arvo[0], beta)
            if arvo[0] <= alpha:
                break
        siirto_taulu[fenJono] = arvo
        return arvo

def tekoalyb(pelitilanne, syvyys, alpha, beta, vuoro, edellinen_siirto, siirto_taulu):
    """Sama kuin tekoalya mutta pelaa valkoisilla napeilla, varmaan lopullisessa versiossa yhdistän nämä.
    """
    if syvyys == 0 or -25000 > edellinen_siirto[0] or edellinen_siirto[0] > 25000:
        return edellinen_siirto
    siirrot = kone_kaikki_siirrot(pelitilanne, vuoro)
    arviot = []
    fenJono = pelitilanne_to_simplified_FEN(pelitilanne, vuoro)
    paras = (0,"")
    if fenJono in siirto_taulu:
        paras = siirto_taulu[fenJono]
    for siirto in siirrot:
        if siirto == paras[1]:
            pass
        else:
            nappula = kone_siirto(pelitilanne, siirto, vuoro)
            arviot.append((arvioi_tilanne(pelitilanne, siirrot, vuoro), siirto))
            kone_peru(pelitilanne, siirto, nappula, vuoro)
    if vuoro == 0:
        arviot.sort(reverse=True)
        arvo = (-500000,"")
        if paras[1] != "":
            arviot = [paras]+arviot
        for siirto in arviot:
            nappula = kone_siirto(pelitilanne, siirto[1], vuoro)
            temp = tekoalyb(pelitilanne, syvyys-1, alpha, beta, 1, (siirto[0], siirto[1]), siirto_taulu)
            kone_peru(pelitilanne, siirto[1], nappula, vuoro)
            if temp[0] > arvo[0]:
                arvo = (temp[0], siirto[1])
            alpha = max(arvo[0], alpha)
            if arvo[0] >= beta:
                break
        siirto_taulu[fenJono] = arvo
        return arvo
    else:
        arviot.sort()
        arvo = (500000, "")
        if paras[1] != "":
            arviot = [paras]+arviot
        for siirto in arviot:
            nappula = kone_siirto(pelitilanne, siirto[1], vuoro)
            temp = tekoalyb(pelitilanne, syvyys-1, alpha, beta, 0, (siirto[0], siirto[1]), siirto_taulu)
            if temp[0] < arvo[0]:
                arvo = (temp[0], siirto[1])
            kone_peru(pelitilanne, siirto[1], nappula, vuoro)
            beta = max(arvo[0], beta)
            if arvo[0] <= alpha:
                break
        siirto_taulu[fenJono] = arvo
        return arvo
    
def pelitilanne_to_simplified_FEN(pelitilanne, vuoro):
    #koska tarvitaan vain siirtojen kannalta uniikki merkkijono niin voidaan yksinkertaistaa
    merkkijono = ""
    tyhjia = 0
    for x in range(8):
        for y in range(8):
            if pelitilanne[y][x] == "-":
                tyhjia += 1
            else:
                if tyhjia > 0:
                    merkkijono += str(tyhjia)
                merkkijono += pelitilanne[y][x]
    merkkijono += str(vuoro)
    return merkkijono
