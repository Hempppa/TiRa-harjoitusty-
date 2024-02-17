### Mitä olen tehnyt
En mitään varsin näyttävää. Pari pientä bugia korjasin ja tein yksikkötestejä lisää sekä korjasin vähän pylintillä koodin laatua

### Miten ohjelma on edistynyt
Jos bugeja ei laasketa niin varsinaisen ohjelman toimivuuden kannalta en ole tehnyt mitää uutta. Viime viikolla unohdin pushata muutokset gitiin joka vähän harmittaa sillä ensimmäisen vertaisarvioijan työ oli vähän turha, sillä suurin osa huomioista oli viikko4 versiossa jo korjattu.

### Mitä opin
Kuinka helposti huolimattomuus virheitä koodiin ilmestyy. Yksi bugi joka ilmeni oli että kuningas ei voinut liikkua suoraan ylöspäin jos se oli 2. rivillä, sillä siirtoja tarkistaessa ehdon x > 0 sijaan oli x > 1.

### Epäselvyyksiä/vaikeuksia
Onko laskentasyvyydelle neljä siirtoa hyvä tavoite? Kaksi siirtoa per pelaaja kuulostaa aika vähäiseltä, mutta viiden siirron laskemisessa menee 30s ja kuutta siirtoa en jaksanut edes odottaa laskentaa loppuun. Jos haluaisin suurentaa laskentasyvyyttä niin pitäisi varmaan jotenkin tehostaa mahdollisten siirtojen selvittämistä, sillä pelitilanteen arviointi ja minimaxi ovat varmaan niin tehokkaita kuin voin niistä saada.

### Mitö aion tehdä
En kerennyt tilannearvio funktioon koskemaan tällä viikolla. Testejä jäi myös pari toteuttamatta jotka haluisin sovellukseen. Harkitsen myös sovelluksen pilkkomista moneen eri tiedostoon, pääasiassa käyttöliittymä (alku(), yksinpeli(), kaksinpeli()), pelilogiikka(tee_siirto(), perusiirto(), kaikki_siirrot(), matti()) ja tekoäly(a,b,aa ja ba versiot). Sen jälkeen varmaan jos lisään jotain niin se on vain huvin vuoksi, esim. pelikentän koon muuttamisen mahdollisuus, pelinappien lisääminen/poistaminen alkutilanteesta, jokin aito käyttöliittymä, yms.
