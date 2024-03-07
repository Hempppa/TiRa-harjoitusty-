# pylint: skip-file
import sys
import os
import unittest
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from pelilogiikka import kone_siirto, matti
from tekoaly import tekoalya, tekoalyb, arvioi_tilanne, pelitilanne_to_simplified_FEN 

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
        while True:
            alku_aika = time.time()
            siirto = tekoalya(Pelilauta, syvyys, -5000000, 5000000, 1, (0, ""), siirto_taulu)
            loppu_aika = time.time()
            if loppu_aika-alku_aika > 2:
                break
            syvyys += 1
        tilanne = matti(Pelilauta, 1)
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
        while True:
            alku_aika = time.time()
            siirto = tekoalya(Pelilauta, syvyys, -5000000, 5000000, 0, (0, ""), siirto_taulu)
            loppu_aika = time.time()
            if loppu_aika-alku_aika > 2:
                break
            syvyys += 1
        tilanne = matti(Pelilauta, 0)
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