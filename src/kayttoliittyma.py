"""Nimensä mukaan käyttöliittymään liittyvä tavara eli pääasiassa tulostaa pelikentän, mutta vastaa myös vuoron vaihtamisesta.
Muuten kutsuu vain muita funktioita.
"""
import time
from tekoaly import tekoalya, tekoalyb, arvioi_tilanne, update_fen
from pelilogiikka import kone_siirto, matti
#ns config asetukset, tästä voi pääasiassa vain aloitusvuoron vaihtaa, uusien nappuloidne tai
#pelilaudan koon vaihtaminen tässä versiossa rikkoo pelin
PELILAUTA = [["R","N","B","Q","K","B","N","R"],
            ["P","P","P","P","P","P","P","P"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["p","p","p","p","p","p","p","p"],
            ["r","n","b","q","k","b","n","r"]]
KAANNOSTAULU = {"p":chr(9817), "r":chr(9814), "n":chr(9816), "b":chr(9815), "q":chr(9813), "k":chr(9812),
                "P":chr(9823), "R":chr(9820), "N":chr(9822), "B":chr(9821), "Q":chr(9819), "K":chr(9818)}
TYHJA = "-"
ALKUID = "RNBQKBNRPPPPPPPP32pppppppprnbqkbnr0KQkq--"
AIKARAJA = 5

def alku():
    """Funktion kutsuminen käynnistää sovelluksen. Funktio kutsuu vain peliin liittyvän funktion.
    """
    print("Pelistä voi poistua kirjoittamalla quit")
    print("Siirrot syötetään muodossa x1 y1 x2 y2 eli esim. 'd7d5'")
    print("Tornitusta varten syötä '00' jos kuninkaan puolelle ja '000' jos kuningattaren")
    print("Ohestalyönnin kohdalla tulee sotilaan liikkeen lisäksi laittaa 'en' eli esim. d4e3en")
    print("Korottamisen siirrolle lisää haluttu pelinappula perään, esim. 'd6d7Q' tai 'd1d0p'.")
    print("Korottamisessa käyettävät nappulat;")
    print(KAANNOSTAULU)
    print("Tämän taulun saa tulostettua milloin vain syöttämällä 'nappulat',")
    print("varsinaiset siirrot näkyvät pelin aikana vielä 'mahdolliset siirrot' taulussa")
    print()
    while True:
        valinta = input("Kaksinpeli (2p), tekoalya vastaan (1p) vai tekoalä vastaan tekoäly (0p): ")
        if valinta in ("quit", "q"):
            break
        if valinta in ("2p", "2P", "2"):
            if kaksinpeli() == "quit":
                break
        if valinta in ("1p", "1P", "1"):
            if yksinpeli() == "quit":
                break
        if valinta in ("0p", "0P", "0"):
            if botti_v_botti() == "quit":
                break

def yksinpeli():
    """Yksinpeli shakkibottia vastaan. Funktio vain kutsuu muita funktioita ja vaihtaa pelaajien vuoroja.

    Returns:
        string: palauttaa 'quit' jos se jossain kohtaa konsoliin vastataan
    """
    vuoro = 0
    pelitilanne = []
    valkoiset_syoty = []
    mustat_syoty = []
    peli_id = ALKUID[:]
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
    edellinen = (0, (None, None, None, None))
    ala_tulosta = False
    while True:

        peli_id = update_fen(pelitilanne, vuoro, peli_id)

        if not ala_tulosta:
            print()
            tulosta_peli(pelitilanne, valkoiset_syoty, mustat_syoty, pelaaja, peli_id, edellinen)
            print()

            print("Pelaajan", vuoro+1, "vuoro")
            tilanne = matti(pelitilanne, vuoro, edellinen, peli_id)
            peli_id = tilanne[3]
            if tilanne[0]:
                print()
                if tilanne[2]:
                    print("Tasapeli")
                elif vuoro == 0:
                    print("Tekoäly voitti!!!")
                else:
                    print("Pelaaja voitti!!!")
                print()
                return ""
            siedettavammat = []
            for siirto in tilanne[1]:
                if len(siirto) > 4:
                    siedettavammat.append(chr(siirto[0]+97) + str(siirto[1]+1) + chr(siirto[2]+97) + str(siirto[3]+1) + siirto[4])
                elif len(siirto) < 4:
                    if len(siirto) < 3:
                        siedettavammat.append("00")
                    else:
                        siedettavammat.append("000")
                else:
                    siedettavammat.append(chr(siirto[0]+97) + str(siirto[1]+1) + chr(siirto[2]+97) + str(siirto[3]+1))
            print("mahdolliset siirrot ", siedettavammat)
        ala_tulosta = False
        if vuoro == pelaaja:
            siirtop = input("Syötä siirto: ")
            if siirtop in ("quit", "q"):
                return "quit"
            if siirtop in ("nappulat", "Nappulat"):
                print()
                print("Nappulat korottaessa:", KAANNOSTAULU)
                print()
                ala_tulosta = True
            elif siirtop in siedettavammat:
                if len(siirtop) > 4:
                    koneistettu = (ord(siirtop[0])-97,int(siirtop[1])-1, ord(siirtop[2])-97, int(siirtop[3])-1, siirtop[4:])
                elif len(siirtop) < 4:
                    if len(siirtop) < 3:
                        koneistettu = (0,0)
                    else:
                        koneistettu = (0,0,0)
                else:
                    koneistettu = (ord(siirtop[0])-97,int(siirtop[1])-1, ord(siirtop[2])-97, int(siirtop[3])-1)
                pois, peli_id = kone_siirto(pelitilanne, koneistettu, vuoro, peli_id)
                edellinen = koneistettu[:]
                if vuoro == 1:
                    if pois != TYHJA:
                        valkoiset_syoty.append(pois)
                    vuoro = 0
                else:
                    if pois != TYHJA:
                        mustat_syoty.append(pois)
                    vuoro = 1
            else:
                print("Laiton siirto")
        else:
            print()
            print("miettii.....")
            #Ennen looppia määrätään ensimmäisen iteraation syvyys ja tyhjä siirtotaulu joka annetaan tekoaly funktioille
            ihan_alku = time.time()
            syvyys = 1
            siirto_taulu = {}
            print("Syvyys: ...")
            while True:
                print(syvyys, end=": ")
                alku_aika = time.time()
                if aly_vuoro == 1:
                    siirto = tekoalya(pelitilanne, syvyys, -5000000, 5000000, 1, edellinen, siirto_taulu, peli_id)
                else:
                    siirto = tekoalyb(pelitilanne, syvyys, -5000000, 5000000, 0, edellinen, siirto_taulu, peli_id)
                loppu_aika = time.time()
                #Jos aikaa iteraation laskemiseen kesti yli kokonaisluvun osoittama määrä sekunneissa niin looppi katkaistaan
                print(loppu_aika-alku_aika, "s")
                if syvyys > 4 and (loppu_aika-alku_aika > AIKARAJA or syvyys > 100):
                    break
                    #
                syvyys += 1
            ihan_loppu = time.time()
            #
            print("Valmis! siirto; ", siirto[0], siirto[1])
            print("Aikaa miettimiseen kului: ", ihan_loppu-ihan_alku, "s")
            print("Iteraatioita: ", syvyys)
            if siirto[1] in tilanne[1]:
                pois, peli_id = kone_siirto(pelitilanne, siirto[1], vuoro, peli_id)
                edellinen = siirto[1][:]
                if vuoro == 1:
                    if pois != TYHJA:
                        valkoiset_syoty.append(pois)
                    vuoro = 0
                else:
                    if pois != TYHJA:
                        mustat_syoty.append(pois)
                    vuoro = 1
            else:
                print("Tekoäly rikki!!! Sori, laita palautetta jossain jotenkin, mieluusti pelitilanteen kera")
                return "quit"

def kaksinpeli():
    """Pelimuoto missä kaksi pelaajaa pelaa toisiaan vastaan. Tämä funktio vain vaihtaa vuoroja ja kutsuu muita funktioita

    Returns:
        String: voi palauttaa vain 'quit' jolloin pelin suoritus pysähtyy. Jos mitään ei palauteta niin sovelluksen suoritus jatkuu
    """
    vuoro = 0
    pelitilanne = []
    valkoiset_syoty = []
    mustat_syoty = []
    peli_id = ALKUID[:]
    edellinen = (0, (None, None, None, None))
    ala_tulosta = False
    for rivi in PELILAUTA:
        pelitilanne.append(rivi[:])
    while True:

        peli_id = update_fen(pelitilanne, vuoro, peli_id)

        if not ala_tulosta:
            print()
            tulosta_peli(pelitilanne, valkoiset_syoty, mustat_syoty, vuoro, peli_id, edellinen)
            print()

            print("Pelaajan", vuoro+1, "vuoro")
            tilanne = matti(pelitilanne, vuoro, edellinen, peli_id)
            peli_id = tilanne[3]
            siedettavammat = []
            for siirto in tilanne[1]:
                if len(siirto) > 4:
                    siedettavammat.append(chr(siirto[0]+97) + str(siirto[1]+1) + chr(siirto[2]+97) + str(siirto[3]+1) + siirto[4])
                elif len(siirto) < 4:
                    if len(siirto) < 3:
                        siedettavammat.append("00")
                    else:
                        siedettavammat.append("000")
                else:
                    siedettavammat.append(chr(siirto[0]+97) + str(siirto[1]+1) + chr(siirto[2]+97) + str(siirto[3]+1))
            if tilanne[0]:
                print()
                if tilanne[2]:
                    print("Tasapeli")
                elif vuoro == 0:
                    print("Pelaaja 2 voitti!!!")
                else:
                    print("Pelaaja 1 voitti!!!")
                print()
                return ""
            print("mahdolliset siirrot ", siedettavammat)
        ala_tulosta = False
        siirto = input("Syötä siirto: ")
        if siirto in ("quit", "q"):
            return "quit"
        if siirto in ("nappulat","Nappulat"):
            ala_tulosta = True
            print()
            print("Nappulat korottaessa:", KAANNOSTAULU)
            print()
        elif siirto in siedettavammat:
            if len(siirto) > 4:
                koneistettu = (ord(siirto[0])-97,int(siirto[1])-1, ord(siirto[2])-97, int(siirto[3])-1, siirto[4:])
            elif len(siirto) < 4:
                if len(siirto) < 3:
                    koneistettu = (0,0)
                else:
                    koneistettu = (0,0,0)
            else:
                koneistettu = (ord(siirto[0])-97,int(siirto[1])-1, ord(siirto[2])-97, int(siirto[3])-1)
            pois, peli_id = kone_siirto(pelitilanne, koneistettu, vuoro, peli_id)
            edellinen = koneistettu[:]
            if vuoro == 1:
                if pois != TYHJA:
                    mustat_syoty.append(pois)
                vuoro = 0
            else:
                if pois != TYHJA:
                    valkoiset_syoty.append(pois)
                vuoro = 1
        else:
            print("Laiton siirto")

def botti_v_botti():
    """Pelimuoto missä tekoalya pelaa tekoalyb vastaan. Tekoälyt ovat taidoltaan yhtä taitavia, joten tekoäly pelaa vain itseään vastaan.

    Returns:
        str: quit jos sattuu jokin virhe, muuten palaudutaan vain kun peli loppuu
    """
    vuoro = 0
    pelitilanne = []
    valkoiset_syoty = []
    mustat_syoty = []
    peli_id = ALKUID[:]
    for rivi in PELILAUTA:
        pelitilanne.append(rivi[:])
    siirto = (0, "")
    edellinen = (0, (None, None, None, None))
    while True:

        peli_id = update_fen(pelitilanne, vuoro, peli_id)

        print()
        tulosta_peli(pelitilanne, valkoiset_syoty, mustat_syoty, 0, peli_id, edellinen)
        print()


        print("Pelaajan", vuoro+1, "vuoro")
        tilanne = matti(pelitilanne, vuoro, edellinen, peli_id)
        peli_id = tilanne[3]
        if tilanne[0]:
            print()
            if tilanne[2]:
                print("Tasapeli")
            elif vuoro == 0:
                print("Tekoäly voitti!!!")
            else:
                print("Pelaaja voitti!!!")
            print()
            return ""
        siedettavammat = []
        for siirto in tilanne[1]:
            if len(siirto) > 4:
                siedettavammat.append(chr(siirto[0]+97) + str(siirto[1]+1) + chr(siirto[2]+97) + str(siirto[3]+1) + siirto[4])
            elif len(siirto) < 4:
                if len(siirto) < 3:
                    siedettavammat.append("00")
                else:
                    siedettavammat.append("000")
            else:
                siedettavammat.append(chr(siirto[0]+97) + str(siirto[1]+1) + chr(siirto[2]+97) + str(siirto[3]+1))
        print("mahdolliset siirrot ", siedettavammat)
        if vuoro == 1:
            print()
            print("miettii.....")
            #Ennen looppia määrätään ensimmäisen iteraation syvyys ja tyhjä siirtotaulu joka annetaan tekoaly funktioille
            ihan_alku = time.time()
            syvyys = 1
            siirto_taulu = {}
            print("Syvyys: ...")
            while True:
                print(syvyys, end=": ")
                alku_aika = time.time()
                siirto = tekoalya(pelitilanne, syvyys, -5000000, 5000000, 1, edellinen, siirto_taulu, peli_id)
                loppu_aika = time.time()
                print(loppu_aika-alku_aika, "s")
                #Jos aikaa iteraation laskemiseen kesti yli kokonaisluvun osoittama määrä sekunneissa niin looppi katkaistaan
                if loppu_aika-alku_aika > AIKARAJA:
                    break
                    #
                syvyys += 1
            ihan_loppu = time.time()
            #
            print("Valmis! siirto; ", siirto[0], siirto[1])
            print("Aikaa miettimiseen kului: ", ihan_loppu-ihan_alku, "s")
            print("Iteraatioita: ", syvyys)
            if siirto[1] in tilanne[1]:
                pois, peli_id = kone_siirto(pelitilanne, siirto[1], vuoro, peli_id)
                edellinen = siirto[1][:]
                if vuoro == 1:
                    if pois != TYHJA:
                        valkoiset_syoty.append(pois)
                    vuoro = 0
                else:
                    if pois != TYHJA:
                        mustat_syoty.append(pois)
                    vuoro = 1
            else:
                print("Tekoäly rikki!!! Sori, laita palautetta jossain jotenkin, mieluusti pelitilanteen kera")
                return "quit"
        else:
            print()
            print("miettii.....")
            #Ennen looppia määrätään ensimmäisen iteraation syvyys ja tyhjä siirtotaulu joka annetaan tekoaly funktioille
            ihan_alku = time.time()
            syvyys = 1
            siirto_taulu = {}
            print("Syvyys: ...")
            while True:
                print(syvyys, end=": ")
                alku_aika = time.time()
                siirto = tekoalyb(pelitilanne, syvyys, -5000000, 5000000, 0, edellinen, siirto_taulu, peli_id)
                loppu_aika = time.time()
                #Jos aikaa iteraation laskemiseen kesti yli kokonaisluvun osoittama määrä sekunneissa niin looppi katkaistaan
                print(loppu_aika-alku_aika, "s")
                if loppu_aika-alku_aika > AIKARAJA or syvyys > 100:
                    break
                    #
                syvyys += 1
            ihan_loppu = time.time()
            #
            print("Valmis! siirto; ", siirto[0], siirto[1])
            print("Aikaa miettimiseen kului: ", ihan_loppu-ihan_alku, "s")
            print("Iteraatioita: ", syvyys)
            if siirto[1] in tilanne[1]:
                pois, peli_id = kone_siirto(pelitilanne, siirto[1], vuoro, peli_id)
                edellinen = siirto[1][:]
                if vuoro == 1:
                    if pois != TYHJA:
                        valkoiset_syoty.append(pois)
                    vuoro = 0
                else:
                    if pois != TYHJA:
                        mustat_syoty.append(pois)
                    vuoro = 1
            else:
                print("Tekoäly rikki!!! Sori, laita palautetta jossain jotenkin, mieluusti pelitilanteen kera")
                return "quit"

def tulosta_peli(pelitilanne, valkoiset_syoty, mustat_syoty, suunta, peli_id, edellinen):
    """Apufunktio pelikentän tulostamiseen

    Args:
        pelitilanne list: lista jossa kaikki pelilaudalla olevat merkit_
        valkoiset_syoty list: lista valkoisen menetetyistä napeista
        mustat_syoty list. lista mustan menetetyistä napeista
        suunta int: jos 1 niin pelikenttä käännetään ylösalaisin
        peli_id str: pelikohtainen id, tulostetaan pääasiassa huvin vuoksi
    """
    if suunta == 0:
        print("Pelin tunniste:", peli_id)
        print("  --------------------")
        for y in range(8):
            rivi = str(y+1) + " |"
            for x in range(8):
                if pelitilanne[y][x] == TYHJA:
                    if (x+y)%2 == 0:
                        rivi += " " + chr(9633)
                    else:
                        rivi += " " + chr(9639)
                else:
                    rivi +=  " " + KAANNOSTAULU[pelitilanne[y][x]]
            print(rivi + "  |")
        print("  --------------------")
        print("    a b c d e f g h")
        print()
        ms = ""
        for merkki in mustat_syoty:
            ms += KAANNOSTAULU[merkki] + " "
        vs = ""
        for merkki in valkoiset_syoty:
            vs += KAANNOSTAULU[merkki] + " "
        print(ms)
        print(vs)
    else:
        kaannetty = []
        for rivi in pelitilanne:
            temp = rivi[:]
            temp.reverse()
            kaannetty.append(temp)
        kaannetty.reverse()
        print("Pelin tunniste:", peli_id)
        print("  --------------------")
        for y in range(8):
            rivi = str(8-y) + " |"
            for x in range(8):
                if kaannetty[y][x] == TYHJA:
                    if (x+y)%2 == 0:
                        rivi += " " + chr(9633)
                    else:
                        rivi += " " + chr(9639)
                else:
                    rivi +=  " " + KAANNOSTAULU[kaannetty[y][x]]
            print(rivi + "  |")
        print("  --------------------")
        print("    h g f e d c b a")
        ms = ""
        for merkki in mustat_syoty:
            ms += KAANNOSTAULU[merkki] + " "
        vs = ""
        for merkki in valkoiset_syoty:
            vs += KAANNOSTAULU[merkki] + " "
        print(vs)
        print(ms)
    print()
    arvio = arvioi_tilanne(pelitilanne, edellinen, [], [], peli_id)
    print("Pelikenttä arvio: ", arvio, " (ns. centipawn)")
