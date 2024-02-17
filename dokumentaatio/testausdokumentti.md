## Miten testit on tehty
Yksikkötestejä vain. Suurimmalle osalle funktioista, etenkin tärkeistä funktioista, on nyt edes pari testiä. Testejä suorittaessa näkyvä numero valehtelee siinä että se näyttää myös testit jotka aion toteuttaa, mutta ovat hetkellä vain return functioita. Erityisesti kuitenkin tekoälyjen testaaminen ei tule edes olemaan hirveän kattava, joitain testejä tulen lisäämään mutta tekoälyjä on vaikeaa testata sillä se tulostaa sen mielestä parhaan siirron ja shakissa ei aina ole sovitusti parasta siirtoa. 

Myöhemmin lisää tulevien testien tarkoitus on siis vain tarkistaa että shakkibotti osaa varmistaa varman voiton laskentasyvyydellään ja että se tulostaa laillisia siirtoja joka tilanteessa. Testaamatta jätän varmaan kokonaan 'käyttöliittymän' eli funktiot alku(), yksinpeli() ja kaksinpeli() jotka siis vain käyttäjän syötteen mukaan kutsuvat pelilogiikkaa ja tekoälyä toteuttavia funktioita, sekä tulostavat pelikentän. Nämä saatan joskus siirtää omaan tiedostoon, että testikattavuus olisi kuvaavampi.
## Kattavuusraportti
![Kattavuusraportti!](./Screenshot%20from%202024-02-17%2022-08-01.png)
Tämän voi siis alla olevilla komennoilla itse suorittaa ja avaamalla selaimella index.html tiedoston saa auki mm. rivittäin jäsennellyn näkymän testikattavuudesta
## Miten testit ja kattavuusraportin saa itse suoritettua
Testit löytyvät app_test.py tiedostosta, testauksen voi suorittaa komennolla:

	pytest

Ja kattavuusraportin saa komennoilla:

	coverage run -m pytest
 	coverage html

Jolloin htmlcov/index.html löytyy tarkka jäsentely testikattavuudesta
