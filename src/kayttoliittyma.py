import time
from tekoaly import tekoalya, tekoalyb, arvioi_tilanne
from pelilogiikka import tee_siirto, kone_siirto, matti
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

ALKUVUORO = 0 #kaksinpelissä kumpi puoli aloittaa
LASKENTA_SYVYYS = 5 #Kuinka kauas tekoäly laskee siirtoja, kannattaa varmaan pitää välillä 3 -- 5

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

def yksinpeli():
    """Yksinpeli shakkibottia vastaan. Funktio vain kutsuu muita ja tulostaa pelikentän yms.

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
            ihan_alku = time.time()
            syvyys = 2
            siirto_taulu = {}
            while True:
                alku_aika = time.time()
                if aly_vuoro == 1:
                    siirto = tekoalya(pelitilanne, syvyys, -500000, 500000, aly_vuoro, (0, ""), siirto_taulu)
                else:
                    siirto = tekoalyb(pelitilanne, syvyys, -500000, 500000, aly_vuoro, (0, ""), siirto_taulu)
                loppu_aika = time.time()
                if loppu_aika-alku_aika > 5:
                    break
                syvyys += 1
            ihan_loppu = time.time()
            print("Valmis! siirto; ", siirto[0], siirto[1])
            print("Aikaa miettimiseen kului: ", ihan_loppu-ihan_alku, "s")
            print("Iteraatioita: ", syvyys)
            if siirto[1] in tilanne[1]:
                kone_siirto(pelitilanne, siirto[1], aly_vuoro)
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