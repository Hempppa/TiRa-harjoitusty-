import unittest
from app import tee_siirto

# Vain yksi yksinkertainen testi, periaatteessa vain testaamaan, että testaaminen onnistuu

class Test_tee_siirto(unittest.TestCase):
    def setUp(self) -> None:
        self.Pelilauta = [["R","H","B","Q","K","B","H","R"],
                    ["P","P","P","P","P","P","P","P"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["p","p","p","p","p","p","p","p"],
                    ["r","h","b","q","k","b","h","r"]]
        pelinappulat = [["p","r","h","b","q","k"],["P","R","H","B","Q","K"]]
    

    def test_tekee_siirron(self):
        temp = [["R","H","B","Q","K","B","H","R"],
                ["P","P","P","P","P","P","P","P"],
                ["-","-","-","-","-","-","-","-"],
                ["-","-","-","-","-","-","-","-"],
                ["-","-","-","p","-","-","-","-"],
                ["-","-","-","-","-","-","-","-"],
                ["p","p","p","-","p","p","p","p"],
                ["r","h","b","q","k","b","h","r"]]
        tee_siirto(self.Pelilauta, "d7d5")
        self.assertEqual(self.Pelilauta, temp)

    def test_palauttaa_oikeat_nappulat(self):
        nappula1 = tee_siirto(self.Pelilauta, "d7d5")
        nappula2 = tee_siirto(self.Pelilauta, "d7d5")
        nappula3 = tee_siirto(self.Pelilauta, "e7g1")
        self.assertEqual(nappula1, "-")
        self.assertEqual(nappula2, "p")
        self.assertEqual(nappula3, "H")