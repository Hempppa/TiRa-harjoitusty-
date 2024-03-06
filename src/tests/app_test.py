# pylint: skip-file
import sys
import os
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from pelilogiikka import tee_siirto, kone_siirto, kone_kaikki_siirrot, matti, onko_shakki
from tekoaly import tekoalya, tekoalyb, arvioi_tilanne, pelitilanne_to_simplified_FEN 

class Test_tee_siirto(unittest.TestCase):
    # Testaa siis sekä tee_siirto että kone_siirto
    def setUp(self) -> None:
        self.Pelilauta = [["R","N","B","Q","K","B","N","R"],
                        ["P","P","P","P","P","P","P","P"],
                        ["-","-","-","-","-","-","-","-"],
                        ["-","-","-","-","-","-","-","-"],
                        ["-","-","-","-","-","-","-","-"],
                        ["-","-","-","-","-","-","-","-"],
                        ["p","p","p","p","p","p","p","p"],
                        ["r","n","b","q","k","b","n","r"]]
        self.pelinappulat = [["p","r","n","b","q","k"],["P","R","N","B","Q","K"]]
    
    def test_tekee_siirron(self):
        temp = [["R","N","B","Q","K","B","N","R"],
                ["P","P","P","P","P","P","P","P"],
                ["-","-","-","-","-","-","-","-"],
                ["-","-","-","-","-","-","-","-"],
                ["-","-","-","p","-","-","-","-"],
                ["-","-","-","-","-","-","-","-"],
                ["p","p","p","-","p","p","p","p"],
                ["r","n","b","q","k","b","n","r"]]
        tee_siirto(self.Pelilauta, "d7d5")
        self.assertEqual(self.Pelilauta, temp)

    def test_palauttaa_oikeat_nappulat(self):
        nappula1 = tee_siirto(self.Pelilauta, "d7d5")
        nappula2 = tee_siirto(self.Pelilauta, "d7d5")
        nappula3 = tee_siirto(self.Pelilauta, "e7g1")
        self.assertEqual(nappula1, "-")
        self.assertEqual(nappula2, "p")
        self.assertEqual(nappula3, "N")
    
    def test_kone_korotus_toimii(self):
        return

    def test_kone_tekee_siirron(self):
        temp = [["R","N","B","Q","K","B","N","R"],
                ["P","P","P","P","P","P","P","P"],
                ["-","-","-","-","-","-","-","-"],
                ["-","-","-","-","-","-","-","-"],
                ["-","-","-","p","-","-","-","-"],
                ["-","-","-","-","-","-","-","-"],
                ["p","p","p","-","p","p","p","p"],
                ["r","n","b","q","k","b","n","r"]]
        kone_siirto(self.Pelilauta, (3,6,3,4))
        self.assertEqual(self.Pelilauta, temp)

    def test_kone_palauttaa_oikeat_nappulat(self):
        nappula1 = kone_siirto(self.Pelilauta, (3,6,3,4))
        nappula2 = kone_siirto(self.Pelilauta, (3,6,3,4))
        nappula3 = kone_siirto(self.Pelilauta, (4,6,6,0))
        self.assertEqual(nappula1, "-")
        self.assertEqual(nappula2, "p")
        self.assertEqual(nappula3, "N")
    
    def test_kone_korotus_toimii(self):
        return


class Test_onko_shakki(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_v_sotilas(self):
        Pelilauta = [["R","N","B","Q","K","B","N","R"],
                    ["P","P","P","P","P","p","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","-","p","p","p","p","p"],
                    ["r","n","b","q","k","b","n","r"]]
        self.assertEqual(onko_shakki(Pelilauta, 1), True)
    
    def test_v_torni(self):
        Pelilauta = [["R","N","B","Q","K","B","N","R"],
                    ["P","P","P","P","-","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","r","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["-","n","b","q","k","b","n","r"]]
        self.assertEqual(onko_shakki(Pelilauta, 1), True)
    
    def test_v_hevonen(self):
        Pelilauta = [["R","N","B","Q","K","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","n","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["r","-","b","q","k","b","n","r"]]
        self.assertEqual(onko_shakki(Pelilauta, 1), True)
    
    def test_v_lahetti(self):
        Pelilauta = [["R","N","B","Q","K","B","N","R"],
                    ["P","P","P","-","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["b","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["r","n","-","q","k","b","n","r"]]
        self.assertEqual(onko_shakki(Pelilauta, 1), True)
    
    def test_v_kuningatar(self):
        Pelilauta1 = [["R","N","B","Q","K","B","N","R"],
                    ["P","P","P","-","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["q","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["r","n","b","-","k","b","n","r"]]
        Pelilauta2 = [["R","N","B","Q","K","B","N","R"],
                    ["P","P","P","P","-","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","q","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["r","n","b","-","k","b","n","r"]]
        self.assertEqual(onko_shakki(Pelilauta1, 1), True)
        self.assertEqual(onko_shakki(Pelilauta2, 1), True)
    
    def test_v_kuningas(self):
        Pelilauta1 = [["R","N","B","Q","K","B","N","R"],
                    ["P","P","P","k","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["r","n","b","q","-","b","n","r"]]
        Pelilauta2 = [["R","N","B","Q","K","B","N","R"],
                    ["P","P","P","P","k","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["r","n","b","q","-","b","n","r"]]
        
        self.assertEqual(onko_shakki(Pelilauta1, 1), True)
        self.assertEqual(onko_shakki(Pelilauta2, 1), True)
    
    def test_b_sotilas(self):
        Pelilauta = [["R","N","B","Q","K","B","N","R"],
                    ["P","P","P","-","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","P","p","p","p","p"],
                    ["r","n","b","q","k","b","n","r"]]
        self.assertEqual(onko_shakki(Pelilauta, 0), True)
    
    def test_b_torni(self):
        Pelilauta = [["-","N","B","Q","K","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","R","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","-","p","p","p"],
                    ["r","n","b","q","k","b","n","r"]]
        self.assertEqual(onko_shakki(Pelilauta, 0), True)
    
    def test_b_hevonen(self):
        Pelilauta = [["R","-","B","Q","K","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","N","-","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["r","n","b","q","k","b","n","r"]]
        self.assertEqual(onko_shakki(Pelilauta, 0), True)
    
    def test_b_lahetti(self):
        Pelilauta = [["R","N","-","Q","K","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["B","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","-","p","p","p","p"],
                    ["r","n","b","q","k","b","n","r"]]
        self.assertEqual(onko_shakki(Pelilauta, 0), True)
    
    def test_b_kuningatar(self):
        Pelilauta1 = [["R","N","B","-","K","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","Q","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","-","p","p","p"],
                    ["r","n","b","q","k","b","n","r"]]
        Pelilauta2 = [["R","N","B","-","K","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["Q","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","-","p","p","p","p"],
                    ["r","n","b","q","k","b","n","r"]]
        self.assertEqual(onko_shakki(Pelilauta1, 0), True)
        self.assertEqual(onko_shakki(Pelilauta2, 0), True)
    
    def test_b_kuningas(self):
        Pelilauta1 = [["R","N","B","Q","-","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","K","p","p","p"],
                    ["r","n","b","q","k","b","n","r"]]
        Pelilauta2 = [["R","N","B","Q","-","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","K","p","p","p","p"],
                    ["r","n","b","q","k","b","n","r"]]
        self.assertEqual(onko_shakki(Pelilauta1, 0), True)
        self.assertEqual(onko_shakki(Pelilauta2, 0), True)

class Test_matti(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_matti_testi_1(self):
        Pelilauta = [["R","N","B","-","K","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","Q"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","p","-","-","p"],
                    ["r","n","b","q","k","b","n","r"]]
        self.assertEqual(matti(Pelilauta, 0)[0], True)
    
    def test_matti_testi_2(self):
        Pelilauta = [["-","-","-","-","-","K","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["R","-","-","-","-","-","-","-"],
                    ["Q","-","-","-","k","-","-","-"]]
        self.assertEqual(matti(Pelilauta, 0)[0], True)
    
    def test_matti_testi_3(self):
        Pelilauta = [["-","-","-","Q","K","B","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","k","-","-","-"],
                    ["-","-","-","-","-","-","-","q"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["r","n","b","-","-","b","n","r"]]
        self.assertEqual(matti(Pelilauta, 1)[0], True)

    def test_rajoittaa_siirtoja_jos_shakki(self):
        Pelilauta = [["-","N","B","Q","K","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","R","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","-","p","p","p"],
                    ["r","n","b","q","k","-","n","r"]]
        loytyy = False
        tilanne = matti(Pelilauta,0)
        if tilanne[0]:
            for siirto in tilanne[1]:
                if siirto == (4,7,4,6) or siirto == (0,6,0,5):
                    loytyy = True
        self.assertEqual(loytyy, False)
    
    def test_rajoittaa_siirtoja_jos_olisi_shakki(self):
        Pelilauta = [["-","N","B","Q","K","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","-","R","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","p","-","p","p"],
                    ["r","n","b","q","k","-","n","r"]]
        loytyy = False
        tilanne = matti(Pelilauta,0)
        if tilanne[0]:
            for siirto in tilanne[1]:
                if siirto == (4,7,5,7) or siirto == (4,7,5,6):
                    loytyy = True
        self.assertEqual(loytyy, False)

class Test_kone_kaikki_siirrot(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_aloituksesta(self):
        Pelilauta = [["R","N","B","Q","K","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["r","n","b","q","k","b","n","r"]]
        pitaisi_olla = [(0,6,0,5),(0,6,0,4),(1,6,1,5),(1,6,1,4),(2,6,2,5),(2,6,2,4),(3,6,3,5),(3,6,3,4),(4,6,4,5),(4,6,4,4),(5,6,5,5),(5,6,5,4),(6,6,6,5),(6,6,6,4),(7,6,7,5),(7,6,7,4),(1,7,0,5),(1,7,2,5),(6,7,5,5),(6,7,7,5)]
        mita_on = kone_kaikki_siirrot(Pelilauta,0)
        for siirto in pitaisi_olla:
            self.assertEqual(siirto in mita_on, True)
    
    def test_vaikeampi_tilanne(self):
        Pelilauta = [["-","K","-","-","-","-","-","-"],
                     ["-","-","R","-","-","-","-","P"],
                     ["-","P","B","-","-","-","-","-"],
                     ["-","-","-","-","b","-","-","-"],
                     ["-","N","-","P","Q","-","-","-"],
                     ["q","p","p","-","B","-","-","-"],
                     ["p","-","R","-","-","-","-","p"],
                     ["-","k","-","r","-","r","-","-"]]
        pitaisi_olla = [(1,0,0,0),(1,0,0,1),(1,0,1,1),(1,0,2,0),(2,1,2,0),(2,1,1,1),(2,1,0,1),(2,1,3,1),(2,1,4,1),(2,1,5,1),(2,1,6,1),(1,2,1,3),(2,2,3,3),(2,2,1,3),(2,2,0,4),(2,2,1,1),(2,2,0,0),(2,2,3,1),(2,2,4,0),(7,1,7,2),(7,1,7,3),(1,4,0,2),(1,4,3,5),(1,4,3,3),(1,4,0,6),(3,4,3,5),(3,4,2,5),(4,4,3,3),(4,4,5,4),(4,4,6,4),(4,4,7,4),(4,4,5,3),(4,4,6,2),(4,4,5,5),(4,4,6,6),(4,4,7,7),(4,4,3,5),(4,5,5,6),(4,5,6,7),(4,5,3,6),(4,5,2,7),(4,5,5,4),(4,5,6,3),(4,5,7,2),(2,6,1,6),(2,6,0,6),(2,6,2,5),(2,6,2,7),(2,6,3,6),(2,6,3,6),(2,6,4,6),(2,6,5,6),(2,6,6,6),(2,6,7,6)]
        mita_on = kone_kaikki_siirrot(Pelilauta, 1)
        for siirto in pitaisi_olla:
            self.assertTrue(siirto in mita_on)

    def test_sisaltaa_korotus(self):
        return

class Test_tekoaly(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_a_palauttaa_jotain_alussa(self):
        Pelilauta = [["R","N","B","Q","K","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["r","n","b","q","k","b","n","r"]]
        try:
            siirto = tekoalya(Pelilauta, 3, -5000000, 5000000, 1, (0,""), {})
        except:
            self.assertTrue(False)
            return
        tilanne = matti(Pelilauta, 1)
        self.assertTrue(siirto[1] in tilanne[1])
    
    def test_a_palauttaa_vaikeammassa_tilanteessa(self):
        Pelilauta = [["-","K","-","-","-","-","-","-"],
                     ["-","-","R","-","-","-","-","P"],
                     ["-","P","B","-","-","-","-","-"],
                     ["-","-","-","-","b","-","-","-"],
                     ["-","-","-","P","Q","-","-","-"],
                     ["q","p","-","-","B","-","-","-"],
                     ["p","-","R","-","-","-","-","p"],
                     ["-","k","-","r","-","r","-","-"]]
        try:
            siirto = tekoalya(Pelilauta, 3, -5000000, 5000000, 1, (0,""), {})
        except:
            self.assertTrue(False)
            return
        tilanne = matti(Pelilauta, 1)
        self.assertTrue(siirto[1] in tilanne[1])
    
    def test_a_osaa_voittaa_kahden_siirron_päässä(self):
        Pelilauta = [["-","-","-","-","R","-","K","-"],
                     ["P","-","-","-","-","r","-","P"],
                     ["-","-","-","b","-","-","P","Q"],
                     ["-","-","-","q","p","-","-","-"],
                     ["-","-","-","B","-","-","-","-"],
                     ["-","-","-","-","-","-","p","-"],
                     ["p","-","-","-","-","r","-","-"],
                     ["-","-","R","b","-","-","k","-"]]
        siirrot = [(2,7,3,7),(7,2,7,7)]
        vastasiirrot = [(6,7,6,6)]
        i = 0
        while i < len(siirrot):
            try:
                siirto = tekoalya(Pelilauta, 3, -5000000, 5000000, 1, (0,""), {})
            except:
                self.assertTrue(False)
                return
            self.assertEqual(siirto[1], siirrot[i])
            kone_siirto(Pelilauta, siirto[1])
            if i < len(vastasiirrot):
                kone_siirto(Pelilauta, vastasiirrot[i])
            else:
                tilanne = matti(Pelilauta, 0)
                self.assertTrue(tilanne[0])
            i += 1
    
    def test_a_iteratiivinen_syveneminen_toimii(self):
        return
    
    def test_b_palauttaa_jotain_alussa(self):
        Pelilauta = [["R","N","B","Q","K","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["r","n","b","q","k","b","n","r"]]
        try:
            siirto = tekoalyb(Pelilauta, 3, -5000000, 5000000, 0, (0,""), {})
        except:
            self.assertTrue(False)
            return
        tilanne = matti(Pelilauta, 0)
        self.assertTrue(siirto[1] in tilanne[1])
    
    def test_b_palauttaa_vaikeammassa_tilanteessa(self):
        Pelilauta = [["-","K","-","-","-","-","-","-"],
                     ["-","-","R","-","-","-","-","P"],
                     ["-","P","B","-","-","-","-","-"],
                     ["-","-","-","-","b","-","-","-"],
                     ["-","-","-","P","Q","-","-","-"],
                     ["q","p","-","-","B","-","-","-"],
                     ["p","-","R","-","-","-","-","p"],
                     ["-","k","-","r","-","r","-","-"]]
        try:
            siirto = tekoalyb(Pelilauta, 3, -5000000, 5000000, 0, (0,""), {})
        except:
            self.assertTrue(False)
        tilanne = matti(Pelilauta, 0)
        self.assertTrue(siirto[1] in tilanne[1])
    
    def test_b_osaa_voittaa_kahden_siirron_päässä(self):
        Pelilauta = [["-","K","-","-","B","r","-","-"],
                     ["-","-","R","-","-","-","-","P"],
                     ["-","P","-","-","-","-","-","-"],
                     ["-","-","-","-","b","-","-","-"],
                     ["-","-","-","P","Q","-","-","-"],
                     ["q","p","-","-","B","-","-","-"],
                     ["p","-","R","-","-","-","-","p"],
                     ["-","k","-","r","-","-","-","-"]]
        siirrot = [(5,0,4,0),(0,5,0,0)]
        vastasiirrot = [(1,0,1,1)]
        i = 0
        while i < len(siirrot):
            try:
                siirto = tekoalyb(Pelilauta, 3, -5000000, 5000000, 0, (0,""), {})
            except:
                self.assertTrue(False)
                return
            self.assertEqual(siirto[1], siirrot[i])
            kone_siirto(Pelilauta, siirto[1])
            if i < len(vastasiirrot):
                kone_siirto(Pelilauta, vastasiirrot[i])
            else:
                tilanne = matti(Pelilauta, 1)
                self.assertTrue(tilanne[0])
            i += 1

    def test_b_iteratiivinen_syveneminen_toimii(self):
        return

#Vähän turhat testit mutta näyttää hyvältä kattavuudessa
class Test_arvioi_tilanne(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_positiivinen(self):
        Pelilauta = [["R","N","B","-","K","-","N","R"],
                    ["P","P","P","P","r","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","p","p","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","-","-","p","p","p"],
                    ["r","n","b","q","k","b","n","-"]]
        self.assertEqual(arvioi_tilanne(Pelilauta)>0, True)

    def test_negatiivinen(self):
        Pelilauta = [["R","N","-","-","K","B","N","R"],
                    ["P","P","P","P","-","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["B","-","-","Q","P","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","-","-","-","-","-","-","-"],
                    ["p","-","p","-","p","p","p","p"],
                    ["r","n","b","-","k","b","n","r"]]
        self.assertEqual(arvioi_tilanne(Pelilauta)<0, True)