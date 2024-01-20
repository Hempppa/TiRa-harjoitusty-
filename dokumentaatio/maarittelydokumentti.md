## Määrittelydokumentti (tulee varmaan täydentymään projektin edetessä)
### Mitä ohjelmointi kieliä käytän
Vain pythonilla on koko ohjelmistotuotanto prosessi tuttu ja koska tavoitteena on saada toimiva ohjelma valmiiksi niin en usko että on aika opetella muita kieliä, joskus vuosia sitten kävin kuitenkin javascript perusteet kurssin, että ehkä hätätilanteessa voin arvioida. 

### Mitä algoritmeja ja tietorakenteita käytän ja miksi
Tavoitteena on siis saada aikaan yksinkertainen shakkibotti, eli Varmaan aiheiden valinnassa esitetty minimaxi alpha-beta karsinnalla pääasiassa. Tämä on hyvä algoritmi valitsemaan laskentasyvyyden rajoituksissa arvioiduista mahdollisista pelitilanteista "paras" siinä mielessä, että kumpikin pelaaja pelaa optimaalisesti. Pelitilanteet arvioin varmaan tämän [wikipedia sivun alaotsikon](https://en.wikipedia.org/wiki/Computer_chess#Leaf_evaluation) esittämällä vanhalla tavalla, lyhyesti jokaiselle pelinappulalle annetaan jokin oma arvo ja kuninkaalle erittäin korkea jolloin shakkimatti on arvokkain pelitilanne.

### Millä syötteillä ohjelma toimii
Annetaan vain pelilaudan nykyinen tilanne, eli jokaisen pelinappulan sijainti (todennäköisesti lista listoista joista jokainen vastaa yhtä laudan riviä. Tästä ohjelma palauttaa sitten tietenkin parhaimman mahdollisen siirron

### Tavoite aika- ja tilavaativuus
En ole ihan hirveästi perehtynyt algoritmiin tai alkanut ohjelmoimaan mitään, joten aikavaativuutta on vaikeaa arvioida. Alpha-beta karsinnan wikipedia sivulta luin ohimennen, että arviointijärjestyksestä riippuen teoreettisesti huonoin aikavaativuus on O(b^d) ja paras O(b^(d/2)), missä b on keskiverto mahdollisten siirtojen määrä kussakin pelitilanteessa ja d on laskentasyvyys siirtojen määränä (pelaajan ja botin). Oikea aikavaativuus on siis jossain tässä välissä ja monimutkaisempi sekä vaikutettavissa (esim. arvioimalla arvokkaimpien tai useiden pelattujen pelinappien liikkeitä ensin). 

Tilavaativuus kulkee varmaan aikavaatimuksen kanssa käsikädessä (arvioidut siirrot täytyy varmaan tallentaa) eikä varmaan ole merkittävän suuri missään tilanteessa. Myöskään ei varmaan ole hyödyllistä tallentaa edellisiä arviointeja sillä paras siirto saattaa muuttua, kun lasketaan kahden (edellinen botin ja sitä seuraava pelaajan) siirron verran pidemmälle. Edellinen parhaiden siirtojen ketju saattaa olla hyä arvioida silti ensin, mutta d siirron muistaminen ei ole vaativaa.

### Lähteet
Tällä hetkellä vain wikipedia sivut [alpha-beta karsinnasta](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) ja [shakin pelitilanteen arvioimisesta](https://en.wikipedia.org/wiki/Computer_chess#Leaf_evaluation) sekä kurssimateriaalit.

### Opinto-ohjelma ja projektin kieli
(TKT) tietojenkäsittelytieteen kanditaatti ja projekti on suomeksi
