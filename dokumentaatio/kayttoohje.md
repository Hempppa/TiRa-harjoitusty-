## Riippuvuuksien asentaminen
Hetkellä en ole vielä ottanut käyttöön poetryä tai vastaavaa. Virtuaaliympäristön voi alustaa ja riippuvuudet voi asentaa juurikansiossa seuraavilla komennoilla (ainakin linux järjestelmässä)

	python3 -m venv venv
	source venv/bin/activate
	pip install -r ./requirements

**Riippuvuuksia ei tarvitse sovelluksen käyttämiseen**, mutta pylintillä voi tarkistaa koodin laadun, pytestillä voi suorittaa testit (sitten kun niitä on), coveragella tarkistaa testikattavuuden, invoke antaa joskus myöhemmin tehdä helpommin suoritettavia "task"ejä mm. sovelluksen testaamiseen ja tosiaan poetryllä voi helpommin asentaa riippuvuudet sitten kun se on käytössä.

Hetkellä siis vain pylint on käytettävissä.

## Sovelluksen käyttäminen
Sovelluksella on hetkellä (ehkä myös pysyvästi) vain tekstikäyttöliittymä komentorivillä. Ainakin linuxissa (varmaan windowsilla on ainakin samankaltainen) sovelluksen saa käynnistettyä juurikansiosta komennolla:

	python3 app.py

Jonka jälkeen sovellus kysyy pelataanko yksin shakkibottia (jota en vielä ole ohjelmoinut peliin) vastaan "1P" vai kaksinpeliä "2P" (lokaalisti eli samalla koneella vuorotellen vain).

Siirtoja syötetään muodossa alku x, alku y, loppu x, loppu y. Eli esim. siirto ruudulta e2 ruutuun e4 on "e2e4". Myöhemmin saattaa tulla erikoisempia siirtoja peliin mutta hetkellä mm. tornitus, ohestalyönti, sotilaan korotus eivät ole pelissä.

Pelistä voi aina poistua syöttämällä "quit".

## Testaaminen ja laaduntarkastus
Hetkellä ohjelmassa ei ole testejä joten testikattavuus on 0%. Joskus tulevaisuudessa varmaan kirjoitan testit app_test.py tiedostoon, jolloin testauksen voi suorittaa komennolla (taas linux):

	pytest	.

Ja kattavuusraportin saa komennolla:

	coverage run -m pytest .

Koodin laatua voi tarkastella pylintillä komennolla:

	pylint app.py

En ole kirjoitushetkellä suorittanut kertaakaan, joten saa olettaa että koodi ei saa hyvää arvosanaa.


