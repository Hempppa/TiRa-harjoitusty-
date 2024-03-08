# Ohjelman rakenne
Koko ohjelma koostuu kolmesta tiedostosta, käyttöliitymä, pelilogiikka ja tekoäly:
## Käyttöliittymä
Käyttöliittymässä on funktiot alku(), yksinpeli(), kaksinpeli(), botti_v_botti() ja tulosta_peli().

- **alku()** on funktio valitsemaan pelimuotojen (yksinpeli, kaksinpeli, botti_v_botti) välillä eikä tee mitään mielenkiintoista
- **tulosta_peli()** On pelilaudan ja muiden pelin tilanteeseen liittyvien tietojen tulostamiseen käytettävä funktio eikä myöskään hirveän kiinnostava
- **kaksinpeli()** Funktio jolla kaksi pelaajaa voi pelata toisiaan vastaan. Kaikki pelimuoto funktiot käyttävät tulosta peli funktiota ja kutsuvat pelilogiikka funktioita itse pelin toimintojen toteuttamiseen. Näistä matti() palauttaa pelin tilanteen (onko matti, onko tasapeli, kaikki lailliset siirrot ja päivittää peli_id:hen mahdollisen ohestalyönti ruudun) ja kone_siirto() vastaa siirtojen tekemisestä pelikentälle. Pääasiassa vain hyvä integraatio testaamiseen ilman tekoälyä
- **yksinpeli()** Funktio joka vastaa sovelluksen päätarkoituksesta, eli tekoälyä vastaan pelaamisesta. Toimii siis samalla tavalla kuin kaksinpeli, mutta yksi pelaajista on tekoälyä, tätä varten on joko tekoalya mustilla pelaamaan tai tekoalyb valkoisilla pelaamaan. Molemmat palauttavat niiden mielestä parhaimman funktion, mutta eri puolille. Tekoälyjä käyttäessä käyttöliittymä myös iteroi niitä, eli lisää laskenta syvyyttä pikkuhiljaa ja antaa seuraavalle iteraatiolle edellisten täyttämää taulukkoa pelitilanteiden arvoista. 
- **botti_v_botti()** Nimensä mukaan molempien siirroista vastaa botti, eli käytössä on sekä tekoalya että tekoalyb.

Käyttöliittymän tarkoitus siis on, niin kuin pitäisikin, vain kommunikoida muiden funktioiden ja ohjelman käyttäjän välillä.

## Pelilogiikka
Pelilogiikassa on funktiot kone_siirto(), kone_peru(), onko_shakki(), matti(), kone_ihan_kaikki_wt_siirrot()

- **kone_siirto()** tekee sille annetun siirron määrämät muutokset sille annetulle kentälle. Samalla myös palauttaa päivitetyn version annetusta peli_id:stä, eli poistaa edellisen ohestalyönti ruudun ja poistaa tornitusmahdollisuudet vastaavasti jos kuningasta tai torneja siirretään.
- **kone_peru()** tarkoituksena peruuttaa kone_siirron tekemät muutoksen. Annetun siirron mukaan muutetaan annettua pelilautaa, funktiolla annetaan myös syöty ruutu jotta syödyt nappulat saadaan palautettua. Ei kuitenkaan päivitä peli_id:tä eli muiden pitää säilyttää vanha sillä peli_id muutoksia ei voi perua.
- **onko_shakki()** palauttaa vain True tai False arvon riippuen onko shakki annetulle pelaajalle. Annetaan myös peli_id ja edellinen siirto jotta kaikki siirrot saadaan laskettua oikein. Hakee kaikki vastustajan siirrot ja katsoo osuuko yksikään kuninkaan kohdalle.
- **matti()** hyödyntäen onko_shakki ja kone_ihan_kaikki_wt_siirrot laskee siirrot jotka veisivät annetun pelaajan pois shakista. Palauttaa totuus arvot että onko tällaisia siirtoja ja onko pelaaja edes shakissa, palauttaa myös nämä siirrot jos niitä on ja kone_ihan_kaikki_wt_siirrot päivittämän peli_id:n. 
- **kone_ihan_kaikki_wt_siirrot()** laskee kaikki mahdolliset siirrot pelitilanteessa ja samalla pitää kirjaa shakeista, sekä päivittää ohestalyönti ruudun peli_id:hen edellisen siirron mukaan. Syötteenä on vain pelilauta, edellinen siirto josta lasketaan ohestalyönti ja peli_id minkä pohjalta tarkistetaan tornitus. Palauttaa lasketut siirrot ja shakit kummallekin puolelle sekä päivitetyn peli_id:n.

Pelilogiikka siis käytetään siirtojen ja shakkien sekä shakkimattien laskemiseen, sekä siirtojen tekemiseen ja perumiseen, eli kaiken mikä on pelin toiminnallisuuden kannalta tärkeätä.

## Tekoäly
Sisältää kaksi/kolme funktiota arvioi_tilanne(), tekoalya() ja tekoalyb()

- **arvioi_tilanne()** heuristinen funktio laskemaan pelitilanteen arvo. Funktio tarvitsee käyttöönsä joko ennalta lasketut siirrot ja shakit (tekoälyn nopeuttamiseen hyödyllistä) tai oikeat edellisen siirron ja peli_id:n jotta se voi laskea kaikki mahdolliset siirrot itse kone_ihan_kaikki_wt_siirrot() funktiolla. Palauttaa arvion lukuna joka on positiivinen jos valkoinen on voittamassa ja negatiivinen jos musta. Tärkeänä huomiona funktio siis laskee vain tämänhetkisen tilanteen eikä huomaa jos esim. seuraava siirto aiheuttaa shakin tai jonkin nappulan menetyksen, eli ei siinä mielessä miten kenttä voi kehittyä ole kovin tarkka arvio pelin tilanteesta.

### Tekoäly, varsinainen minimaxi ja muut optimisaatiot
Varsinainen minimax algoritmi on tekoalya ja tekoalyb funktioissa. 

Funktiolle annetaan nykyinen pelitilanne, syvyys eli kuinka monta siirtoa tulevaisuuteen lasketaan, alpha eli ikään kuin siirron arvon yläraja, beta eli ikään kuin siirron arvon alaraja, vuoro eli kumman puolen siirtoa seuraavaksi lasketaan, edellinen siirto joka sisältää sekä varsinaisen siirron että sen arvion, siirto_taulun eli jo laskettuissa pelitilanteissa paras siirto, peli_id tekoälyä kutsuessa ja edelliset shakit jotta matti tilanteessa laskenta saadaan katkaistua ennen siirtojen arviointia. Jokaisella siirrolla lasketaan kaikki mahdolliset seuraavat siirrot, lasketaan jokaisesta siirrosta johtuvasta pelitilanteesta arvio ja tarkistetaan onko paras siirto jo siirto taulussa. 

Järjestämällä siirrot saadaan todennäköisesti aikaan aikaisempi karsinta. Tälleen järjestäessä käytetään edellisen vuoron mahdollisia siirtoja (jotka on jo laskettu) nopeuttamaan prosessia, mutta syvyydellä 1 lasketaan uudestaan tarkata arviot jotta lopullinen arvio pohjautuu oikeisiin arvoihin. Siirtotaulussa on siis tulos siitä kun viimeksi funktio oli tässä pelitilanteessa, tätä käytetään iteroidessa hyödyksi sillä edellisen iteraation paras siirto on paras arvaus tämän iteraation parhaasta siirrosta ja arvioimalla paras siirto ensin saadaan mahdollisesti aikaan aikaisempi siirtojen karsinta. Karsinta tapahtuu siten, että maksivoivassa haarassa lopetetaan laskenta jos löytyy suurempi siirto kuin viereisestä sillä ylempi minimoiva haara valitsee sen, beta karsinta. Minimoivassa taas toisin päin, eli jos löytyy pienempi niin ylempi maksimoiva ei koskaan valitse tätä haaraa. Lopuksi palautettu siirto on siis ensimmäinen ketjussa joka johtaa optimaaliseen pelitilaneteeseen, jos molemmat pelaajat pelaavat parhaita siirtoja.
- **tekoalya()** Laskee siirrot mustilla nappuloilla eli palauttaa mustilla laillisen siirron
- **tekoalyb()** Laskee siirrot valkoisilla ja palauttaa vastaavan siirron

Tekoäly tiedosto siis sisältää funktiot jotka pelilogiikka funktioita hyödyntämällä saavat laskettua parhaan siirron. Tärkeänä huomiona siis että jos haluaa nämä ottaa johonkin muuhun käyttöön niin täytyy myös ottaa siirrot tekevän ja peruvan sekä siirrot laskevan funktion, tai tehdä omat. Periaatteessa kelpaa minimaxi funktiot muihinkin peleihin, jos muuttaa/vaihtaa noita muita funktioita, mutta heuristinen funktio ei, eli sen joutuu tekemään käytännössä kokonaan uudestaan.

