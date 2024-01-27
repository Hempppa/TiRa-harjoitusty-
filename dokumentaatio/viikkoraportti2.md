### Mitä olen tehnyt
Itse shakkisovellus on nyt mielestäni valmis, bugeja saattaa kyllä vielä löytyä sillä testausta en kerennyt aloittaa. Koodin dokumentointi on mielestäni nyt ajan tasalla.

### Miten ohjelma on edistynyt
Vähän hitaasti, shakkisääntöjen implementointi oli yllättävän työlästä enkä kerennyt mm. yksikkötestausta suorittamaan ollenkaan.

### Mitä opin
On yllättävän työlästä päätellä mahdollisia siirtoja shakissa. Esim. kuningattarella käytännössä vissiin joutuu käymään jokaisella kahdeksalla akselilla yksi kerrallaan kaikki ruudut läpi kunnes tulee pelinappi tai laudan reuna vastaan.
Myöskin se, että peli päättyy jo shakki-mattiin ja itse kuninkaan vieminen on mahdotonta ovat aiheuttaneet paljon vaivaa.

### Epäselvyyksiä/vaikeuksia
Luin viime palautuksen ja jäin miettimään miten shakkinappuloiden sijointia kannattaisi parhaiten arvioida jos niitä kannattaa ollenkaan, sillä shakkibotti arvioi toivottavasti ainakin peliä niin kauas, että pystyy myöhemmin lähestyessä 
tilannetta arvioimaan pelinapin sijainnin arvoa sitten siitä johtuvista pelinappien viemisestä. En myöskään tiedä miten sijaintia lähteä arvioimaan, esim. tässä [wikipedia artikkelissa](https://en.wikipedia.org/wiki/Evaluation_function) 
on lisää tietoa, mutta tulee ainakin olemaan vaikeaa itse päätellä arvoja/painoja jotka oikeasti auttaisivat arvioinissa, sillä en ole kovin hyvä shakissa tai tiedä juuri mitään shakin pelaamisen teoriasta.

### Mitö aion tehdä
Seuraavalla viikolla ainakin aloitan shakkibotin, olisi hyvä saada pelitilanteen arviointi aikaan, niin ensi viikolla voi keskittyä minmimax alpha-beta karsinta algoritmiin. Hetkellä yksikkötestaus on vähän takasijalla, että saattaa mennä vielä viikko tai kaksi ennen kuin sitä aloittelen. Myöskin ainakin poetry olisi hyvä saada kuitenkin käyttöön ensi viikkoon mennessä, hetkellä en vain muista miten sitä käytettiin ja aika on vähissä.
