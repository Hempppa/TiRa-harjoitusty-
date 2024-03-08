# pylint: skip-file
import sys
import os
import unittest
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from pelilogiikka import kone_siirto, matti
from tekoaly import tekoalya, tekoalyb, arvioi_tilanne, update_fen

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
        peliID = update_fen(Pelilauta, 1, "KQkq--")
        try:
            siirto = tekoalya(Pelilauta, 3, -5000000, 5000000, 1, (0,(None,None,None,None)), {}, peliID)
        except:
            self.assertTrue(False)
        tilanne = matti(Pelilauta, 1, (None,None,None,None), peliID)
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
        peliID = update_fen(Pelilauta, 1, "------")
        try:
            siirto = tekoalya(Pelilauta, 3, -5000000, 5000000, 1, (0,(None,None,None,None)), {}, peliID)
        except:
            self.assertTrue(False)
        tilanne = matti(Pelilauta, 1, (None,None,None,None), peliID)
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
        peliID = update_fen(Pelilauta, 1, "------")
        while i < len(siirrot):
            try:
                siirto = tekoalya(Pelilauta, 5, -5000000, 5000000, 1, (0,(None,None,None,None)), {}, peliID)
            except:
                self.assertTrue(False)
            self.assertTrue(siirto[0] > 25000)
            self.assertEqual(siirto[1], siirrot[i])
            p, peliID = kone_siirto(Pelilauta, siirto[1], 1, peliID)
            if i < len(vastasiirrot):
                p, peliID = kone_siirto(Pelilauta, vastasiirrot[i], 0, peliID)
            else:
                tilanne = matti(Pelilauta, 0, (None,None,None,None), peliID)
                self.assertTrue(tilanne[0])
            i += 1
    
    def test_a_iteratiivinen_syveneminen_toimii(self):
        Pelilauta = [["R","N","B","Q","K","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["r","n","b","q","k","b","n","r"]]
        syvyys = 1
        siirto_taulu = {}
        peliID = update_fen(Pelilauta, 1, "KQkq--")
        while True:
            alku_aika = time.time()
            siirto = tekoalya(Pelilauta, syvyys, -5000000, 5000000, 1, (0, (None,None,None,None)), siirto_taulu, peliID)
            loppu_aika = time.time()
            if loppu_aika-alku_aika > 2:
                break
            syvyys += 1
        tilanne = matti(Pelilauta, 1, (None,None,None,None), peliID)
        self.assertTrue(siirto[1] in tilanne[1])
        
    
    def test_b_palauttaa_jotain_alussa(self):
        Pelilauta = [["R","N","B","Q","K","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["r","n","b","q","k","b","n","r"]]
        peliID = update_fen(Pelilauta, 0, "KQkq--")
        try:
            siirto = tekoalyb(Pelilauta, 3, -5000000, 5000000, 0, (0,(None,None,None,None)), {}, peliID)
        except:
            self.assertTrue(False)
        tilanne = matti(Pelilauta, 0, (None,None,None,None), peliID)
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
        peliID = update_fen(Pelilauta, 0, "------")
        try:
            siirto = tekoalyb(Pelilauta, 4, -5000000, 5000000, 0, (0,(None,None,None,None)), {}, peliID)
        except:
            self.assertTrue(False)
        tilanne = matti(Pelilauta, 0,(None,None,None,None), peliID)
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
        peliID = update_fen(Pelilauta, 0, "------")
        while i < len(siirrot):
            try:
                siirto = tekoalyb(Pelilauta, 5, -5000000, 5000000, 0, (0,(None,None,None,None)), {}, peliID)
            except:
                self.assertTrue(False)
            self.assertTrue(siirto[0] > 25000)
            self.assertEqual(siirto[1], siirrot[i])
            p, peliID = kone_siirto(Pelilauta, siirto[1], 0, peliID)
            if i < len(vastasiirrot):
                p, peliID = kone_siirto(Pelilauta, vastasiirrot[i], 1, peliID)
            else:
                tilanne = matti(Pelilauta, 1, (None,None,None,None), peliID)
                self.assertTrue(tilanne[0])
            i += 1

    def test_b_iteratiivinen_syveneminen_toimii(self):
        Pelilauta = [["R","N","B","Q","K","B","N","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["r","n","b","q","k","b","n","r"]]
        syvyys = 1
        siirto_taulu = {}
        peliID = update_fen(Pelilauta, 0, "KQkq--")
        while True:
            alku_aika = time.time()
            siirto = tekoalya(Pelilauta, syvyys, -5000000, 5000000, 0, (0, (None,None,None,None)), siirto_taulu, peliID)
            loppu_aika = time.time()
            if loppu_aika-alku_aika > 2:
                break
            syvyys += 1
        tilanne = matti(Pelilauta, 0, (None,None,None,None), peliID)
        self.assertTrue(siirto[1] in tilanne[1])

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
        peliID = update_fen(Pelilauta, 1, "KQkq--")
        self.assertEqual(arvioi_tilanne(Pelilauta, (None,None,None,None), [], [], peliID)>0, True)

    def test_negatiivinen(self):
        Pelilauta = [["R","N","-","-","K","B","N","R"],
                    ["P","P","P","P","-","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["B","-","-","Q","P","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","-","-","-","-","-","-","-"],
                    ["p","-","p","-","p","p","p","p"],
                    ["r","n","b","-","k","b","n","r"]]
        peliID = update_fen(Pelilauta, 1, "KQkq--")
        self.assertEqual(arvioi_tilanne(Pelilauta, (None,None,None,None), [], [], peliID)<0, True)

class Test_update_fen(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_palauttaa_jarkevan_mittasen_eika_muuta_loppua(self):
        Pelilauta = [["-","K","-","-","-","-","-","-"],
                     ["-","-","R","-","-","-","-","P"],
                     ["-","P","B","-","-","-","-","-"],
                     ["-","-","-","-","b","-","-","-"],
                     ["-","-","-","P","Q","-","-","-"],
                     ["q","p","-","-","B","-","-","-"],
                     ["p","-","R","-","-","-","-","p"],
                     ["-","k","-","r","-","r","-","-"]]        
        peliID = "RNBQKBNRPPPPPPPP32pppppppprnbqkbnr0KQkq34"
        uusiID = update_fen(Pelilauta, 1, peliID)
        self.assertTrue(len(uusiID) == len("1K8R4P1PB9b6PQ3qp2B3p1R4p1k1r1r1KQkq34"))
        self.assertEqual(peliID[-6:], uusiID[-6:])
