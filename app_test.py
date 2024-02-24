# pylint: skip-file
import unittest
from app import tee_siirto, kone_siirto, kone_kaikki_siirrot, matti, onko_shakki, tekoalya, tekoalyb, arvioi_tilanne 

# Vain yksi yksinkertainen testi, periaatteessa vain testaamaan, että testaaminen onnistuu

class Test_tee_siirto(unittest.TestCase):
    # Testaa siis sekä tee_siirto että kone_siirto
    def setUp(self) -> None:
        self.Pelilauta = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                        [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                        ["-","-","-","-","-","-","-","-"],
                        ["-","-","-","-","-","-","-","-"],
                        ["-","-","-","-","-","-","-","-"],
                        ["-","-","-","-","-","-","-","-"],
                        [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
                        [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        self.pelinappulat = [[chr(9817),chr(9814),chr(9816),chr(9815),chr(9813),chr(9812)],[chr(9823),chr(9820),chr(9822),chr(9821),chr(9819),chr(9818)]]
    
    def test_tekee_siirron(self):
        temp = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                ["-","-","-","-","-","-","-","-"],
                ["-","-","-","-","-","-","-","-"],
                ["-","-","-",chr(9817),"-","-","-","-"],
                ["-","-","-","-","-","-","-","-"],
                [chr(9817),chr(9817),chr(9817),"-",chr(9817),chr(9817),chr(9817),chr(9817)],
                [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        tee_siirto(self.Pelilauta, "d7d5")
        self.assertEqual(self.Pelilauta, temp)

    def test_palauttaa_oikeat_nappulat(self):
        nappula1 = tee_siirto(self.Pelilauta, "d7d5")
        nappula2 = tee_siirto(self.Pelilauta, "d7d5")
        nappula3 = tee_siirto(self.Pelilauta, "e7g1")
        self.assertEqual(nappula1, "-")
        self.assertEqual(nappula2, chr(9817))
        self.assertEqual(nappula3, chr(9822))

    def test_kone_tekee_siirron(self):
        temp = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                ["-","-","-","-","-","-","-","-"],
                ["-","-","-","-","-","-","-","-"],
                ["-","-","-",chr(9817),"-","-","-","-"],
                ["-","-","-","-","-","-","-","-"],
                [chr(9817),chr(9817),chr(9817),"-",chr(9817),chr(9817),chr(9817),chr(9817)],
                [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        kone_siirto(self.Pelilauta, (3,6,3,4))
        self.assertEqual(self.Pelilauta, temp)

    def test_kone_palauttaa_oikeat_nappulat(self):
        nappula1 = kone_siirto(self.Pelilauta, (3,6,3,4))
        nappula2 = kone_siirto(self.Pelilauta, (3,6,3,4))
        nappula3 = kone_siirto(self.Pelilauta, (4,6,6,0))
        self.assertEqual(nappula1, "-")
        self.assertEqual(nappula2, chr(9817))
        self.assertEqual(nappula3, chr(9822))


class Test_onko_shakki(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_v_sotilas(self):
        Pelilauta = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9817),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),"-",chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        self.assertEqual(onko_shakki(Pelilauta, 1), True)
    
    def test_v_torni(self):
        Pelilauta = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),"-",chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-",chr(9814),"-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
                    ["-",chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        self.assertEqual(onko_shakki(Pelilauta, 1), True)
    
    def test_v_hevonen(self):
        Pelilauta = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-",chr(9816),"-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),"-",chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        self.assertEqual(onko_shakki(Pelilauta, 1), True)
    
    def test_v_lahetti(self):
        Pelilauta = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),"-",chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9815),"-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),"-",chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        self.assertEqual(onko_shakki(Pelilauta, 1), True)
    
    def test_v_kuningatar(self):
        Pelilauta1 = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),"-",chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9813),"-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),"-",chr(9812),chr(9815),chr(9816),chr(9814)]]
        Pelilauta2 = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),"-",chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-",chr(9813),"-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),"-",chr(9812),chr(9815),chr(9816),chr(9814)]]
        self.assertEqual(onko_shakki(Pelilauta1, 1), True)
        self.assertEqual(onko_shakki(Pelilauta2, 1), True)
    
    def test_v_kuningas(self):
        Pelilauta1 = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9812),chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),"-",chr(9815),chr(9816),chr(9814)]]
        Pelilauta2 = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9812),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),"-",chr(9815),chr(9816),chr(9814)]]
        
        self.assertEqual(onko_shakki(Pelilauta1, 1), True)
        self.assertEqual(onko_shakki(Pelilauta2, 1), True)
    
    def test_b_sotilas(self):
        Pelilauta = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),"-",chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9823),chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        self.assertEqual(onko_shakki(Pelilauta, 0), True)
    
    def test_b_torni(self):
        Pelilauta = [["-",chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-",chr(9820),"-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),"-",chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        self.assertEqual(onko_shakki(Pelilauta, 0), True)
    
    def test_b_hevonen(self):
        Pelilauta = [[chr(9820),"-",chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-",chr(9822),"-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        self.assertEqual(onko_shakki(Pelilauta, 0), True)
    
    def test_b_lahetti(self):
        Pelilauta = [[chr(9820),chr(9822),"-",chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9821),"-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),"-",chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        self.assertEqual(onko_shakki(Pelilauta, 0), True)
    
    def test_b_kuningatar(self):
        Pelilauta1 = [[chr(9820),chr(9822),chr(9821),"-",chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-",chr(9819),"-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),"-",chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        Pelilauta2 = [[chr(9820),chr(9822),chr(9821),"-",chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9819),"-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),"-",chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        self.assertEqual(onko_shakki(Pelilauta1, 0), True)
        self.assertEqual(onko_shakki(Pelilauta2, 0), True)
    
    def test_b_kuningas(self):
        Pelilauta1 = [[chr(9820),chr(9822),chr(9821),chr(9819),"-",chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),chr(9818),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        Pelilauta2 = [[chr(9820),chr(9822),chr(9821),chr(9819),"-",chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9818),chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        self.assertEqual(onko_shakki(Pelilauta1, 0), True)
        self.assertEqual(onko_shakki(Pelilauta2, 0), True)

class Test_matti(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_matti_testi_1(self):
        Pelilauta = [[chr(9820),chr(9822),chr(9821),"-",chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-",chr(9819)],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),"-","-",chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        self.assertEqual(matti(Pelilauta, 0)[0], True)
    
    def test_matti_testi_2(self):
        Pelilauta = [["-","-","-","-","-",chr(9818),"-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9820),"-","-","-","-","-","-","-"],
                    [chr(9819),"-","-","-",chr(9812),"-","-","-"]]
        self.assertEqual(matti(Pelilauta, 0)[0], True)
    
    def test_matti_testi_3(self):
        Pelilauta = [["-","-","-",chr(9819),chr(9818),chr(9821),"-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-",chr(9812),"-","-","-"],
                    ["-","-","-","-","-","-","-",chr(9813)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),"-","-",chr(9815),chr(9816),chr(9814)]]
        self.assertEqual(matti(Pelilauta, 1)[0], True)

    def test_rajoittaa_siirtoja_jos_shakki(self):
        Pelilauta = [["-",chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-",chr(9820),"-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),"-",chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),"-",chr(9816),chr(9814)]]
        loytyy = False
        tilanne = matti(Pelilauta,0)
        if tilanne[0]:
            for siirto in tilanne[1]:
                if siirto == (4,7,4,6) or siirto == (0,6,0,5):
                    loytyy = True
        self.assertEqual(loytyy, False)
    
    def test_rajoittaa_siirtoja_jos_olisi_shakki(self):
        Pelilauta = [["-",chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-",chr(9820),"-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),"-",chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),"-",chr(9816),chr(9814)]]
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
        Pelilauta = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        pitaisi_olla = [(0,6,0,5),(0,6,0,4),(1,6,1,5),(1,6,1,4),(2,6,2,5),(2,6,2,4),(3,6,3,5),(3,6,3,4),(4,6,4,5),(4,6,4,4),(5,6,5,5),(5,6,5,4),(6,6,6,5),(6,6,6,4),(7,6,7,5),(7,6,7,4),(1,7,0,5),(1,7,2,5),(6,7,5,5),(6,7,7,5)]
        mita_on = kone_kaikki_siirrot(Pelilauta,0)
        for siirto in pitaisi_olla:
            self.assertEqual(siirto in mita_on, True)
    
    def test_vaikeampi_tilanne(self):
        Pelilauta = [["-",chr(9818),"-","-","-","-","-","-"],
                     ["-","-",chr(9820),"-","-","-","-",chr(9823)],
                     ["-",chr(9823),chr(9821),"-","-","-","-","-"],
                     ["-","-","-","-",chr(9815),"-","-","-"],
                     ["-",chr(9822),"-",chr(9823),chr(9819),"-","-","-"],
                     [chr(9813),chr(9817),chr(9817),"-",chr(9821),"-","-","-"],
                     [chr(9817),"-",chr(9820),"-","-","-","-",chr(9817)],
                     ["-",chr(9812),"-",chr(9814),"-",chr(9814),"-","-"]]
        pitaisi_olla = [(1,0,0,0),(1,0,0,1),(1,0,1,1),(1,0,2,0),(2,1,2,0),(2,1,1,1),(2,1,0,1),(2,1,3,1),(2,1,4,1),(2,1,5,1),(2,1,6,1),(1,2,1,3),(2,2,3,3),(2,2,1,3),(2,2,0,4),(2,2,1,1),(2,2,0,0),(2,2,3,1),(2,2,4,0),(7,1,7,2),(7,1,7,3),(1,4,0,2),(1,4,3,5),(1,4,3,3),(1,4,0,6),(3,4,3,5),(3,4,2,5),(4,4,3,3),(4,4,5,4),(4,4,6,4),(4,4,7,4),(4,4,5,3),(4,4,6,2),(4,4,5,5),(4,4,6,6),(4,4,7,7),(4,4,3,5),(4,5,5,6),(4,5,6,7),(4,5,3,6),(4,5,2,7),(4,5,5,4),(4,5,6,3),(4,5,7,2),(2,6,1,6),(2,6,0,6),(2,6,2,5),(2,6,2,7),(2,6,3,6),(2,6,3,6),(2,6,4,6),(2,6,5,6),(2,6,6,6),(2,6,7,6)]
        mita_on = kone_kaikki_siirrot(Pelilauta, 1)
        for siirto in pitaisi_olla:
            self.assertTrue(siirto in mita_on)

class Test_tekoaly(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_a_palauttaa_jotain_alussa(self):
        Pelilauta = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        try:
            siirto = tekoalya(Pelilauta, 3, -50000, 50000, 1, (0,""))
        except:
            self.assertTrue(False)
            return
        tilanne = matti(Pelilauta, 1)
        self.assertTrue(siirto[1] in tilanne[1])
    
    def test_a_palauttaa_vaikeammassa_tilanteessa(self):
        Pelilauta = [["-",chr(9818),"-","-","-","-","-","-"],
                     ["-","-",chr(9820),"-","-","-","-",chr(9823)],
                     ["-",chr(9823),chr(9821),"-","-","-","-","-"],
                     ["-","-","-","-",chr(9815),"-","-","-"],
                     ["-","-","-",chr(9823),chr(9819),"-","-","-"],
                     [chr(9813),chr(9817),"-","-",chr(9821),"-","-","-"],
                     [chr(9817),"-",chr(9820),"-","-","-","-",chr(9817)],
                     ["-",chr(9812),"-",chr(9814),"-",chr(9814),"-","-"]]
        try:
            siirto = tekoalya(Pelilauta, 3, -50000, 50000, 1, (0,""))
        except:
            self.assertTrue(False)
            return
        tilanne = matti(Pelilauta, 1)
        self.assertTrue(siirto[1] in tilanne[1])
    
    def test_a_osaa_voittaa_kahden_siirron_päässä(self):
        Pelilauta = [["-","-","-","-",chr(9820),"-",chr(9818),"-"],
                     [chr(9823),"-","-","-","-",chr(9814),"-",chr(9823)],
                     ["-","-","-",chr(9815),"-","-",chr(9823),chr(9819)],
                     ["-","-","-",chr(9813),chr(9817),"-","-","-"],
                     ["-","-","-",chr(9821),"-","-","-","-"],
                     ["-","-","-","-","-","-",chr(9817),"-"],
                     [chr(9817),"-","-","-","-",chr(9814),"-","-"],
                     ["-","-",chr(9820),chr(9815),"-","-",chr(9812),"-"]]
        siirrot = [(2,7,3,7),(7,2,7,7)]
        vastasiirrot = [(6,7,6,6)]
        i = 0
        while i < len(siirrot):
            try:
                siirto = tekoalya(Pelilauta, 3, -50000, 50000, 1, (0,""))
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
    
    def test_bloittaa_palauttaa_jotain_alussa(self):
        Pelilauta = [[chr(9820),chr(9822),chr(9821),chr(9819),chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),chr(9814)]]
        try:
            siirto = tekoalyb(Pelilauta, 3, -50000, 50000, 0, (0,""))
        except:
            self.assertTrue(False)
            return
        tilanne = matti(Pelilauta, 0)
        self.assertTrue(siirto[1] in tilanne[1])
    
    def test_bloittaa_palauttaa_vaikeammassa_tilanteessa(self):
        Pelilauta = [["-",chr(9818),"-","-","-","-","-","-"],
                     ["-","-",chr(9820),"-","-","-","-",chr(9823)],
                     ["-",chr(9823),chr(9821),"-","-","-","-","-"],
                     ["-","-","-","-",chr(9815),"-","-","-"],
                     ["-","-","-",chr(9823),chr(9819),"-","-","-"],
                     [chr(9813),chr(9817),"-","-",chr(9821),"-","-","-"],
                     [chr(9817),"-",chr(9820),"-","-","-","-",chr(9817)],
                     ["-",chr(9812),"-",chr(9814),"-",chr(9814),"-","-"]]
        try:
            siirto = tekoalyb(Pelilauta, 3, -50000, 50000, 0, (0,""))
        except:
            self.assertTrue(False)
        tilanne = matti(Pelilauta, 0)
        self.assertTrue(siirto[1] in tilanne[1])
    
    def test_b_osaa_voittaa_kahden_siirron_päässä(self):
        Pelilauta = [["-",chr(9818),"-","-",chr(9821),chr(9814),"-","-"],
                     ["-","-",chr(9820),"-","-","-","-",chr(9823)],
                     ["-",chr(9823),"-","-","-","-","-","-"],
                     ["-","-","-","-",chr(9815),"-","-","-"],
                     ["-","-","-",chr(9823),chr(9819),"-","-","-"],
                     [chr(9813),chr(9817),"-","-",chr(9821),"-","-","-"],
                     [chr(9817),"-",chr(9820),"-","-","-","-",chr(9817)],
                     ["-",chr(9812),"-",chr(9814),"-","-","-","-"]]
        siirrot = [(5,0,4,0),(0,5,0,0)]
        vastasiirrot = [(1,0,1,1)]
        i = 0
        while i < len(siirrot):
            try:
                siirto = tekoalyb(Pelilauta, 3, -50000, 50000, 0, (0,""))
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

#Vähän turhat testit mutta näyttää hyvältä kattavuudessa
class Test_arvioi_tilanne(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_positiivinen(self):
        Pelilauta = [[chr(9820),chr(9822),chr(9821),"-",chr(9818),"-",chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),chr(9814),chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-",chr(9817),chr(9817),"-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),chr(9817),chr(9817),"-","-",chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),chr(9813),chr(9812),chr(9815),chr(9816),"-"]]
        self.assertEqual(arvioi_tilanne(Pelilauta)>0, True)

    def test_negatiivinen(self):
        Pelilauta = [[chr(9820),chr(9822),"-","-",chr(9818),chr(9821),chr(9822),chr(9820)],
                    [chr(9823),chr(9823),chr(9823),chr(9823),"-",chr(9823),chr(9823),chr(9823)],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9821),"-","-",chr(9819),chr(9823),"-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    [chr(9817),"-","-","-","-","-","-","-"],
                    [chr(9817),"-",chr(9817),"-",chr(9817),chr(9817),chr(9817),chr(9817)],
                    [chr(9814),chr(9816),chr(9815),"-",chr(9812),chr(9815),chr(9816),chr(9814)]]
        self.assertEqual(arvioi_tilanne(Pelilauta)<0, True)