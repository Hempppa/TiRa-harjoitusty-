## Riippuvuuksien asentaminen
Virtuaaliympäristön voi alustaa ja riippuvuudet voi asentaa juurikansiossa seuraavilla komennoilla (ainakin linux järjestelmässä)

	python3 -m venv venv
	source venv/bin/activate
	pip install -r ./requirements

**Riippuvuuksia ei tarvitse sovelluksen käyttämiseen**, mutta pylintillä voi tarkistaa koodin laadun, pytestillä voi suorittaa testit ja coveragella tarkistaa testikattavuuden.

## Sovelluksen käyttäminen
Sovelluksella on hetkellä (ehkä myös pysyvästi) vain tekstikäyttöliittymä komentorivillä. Ainakin linuxissa (varmaan windowsilla on ainakin samankaltainen) sovelluksen saa käynnistettyä juurikansiosta komennolla:

	python3 app.py

Jonka jälkeen sovellus kysyy pelataanko yksin shakkibottia vastaan "1P" vai kaksinpeliä "2P" (lokaalisti eli samalla koneella vuorotellen vain).

Siirtoja syötetään muodossa alku x, alku y, loppu x, loppu y. Eli esim. siirto ruudulta e2 ruutuun e4 on "e2e4". Ohestalyömisen (en passant) tapauksessa syötä sotilaan siirto ja "en" perään eli esim. d3e2en. Korottaessa sotilasta, joutuu siirron perään lisäämään nappula johon korotetaan. Mahdolliset napit ovat p=sotilas, r=torni, n=ratsu, b=lähetti, q=kuningatar. Nämä pitää syöttää isolla jos pelaa mustilla, eli S, R, N, B, Q. Tornitusta varten syötetään "00" jos kuninkaan puolelle ja "000" jos tornitetaan kuningattaren puolelle.

Pelistä voi aina poistua syöttämällä "quit".

## Testaaminen ja laaduntarkastus
Testit löytyvät app_test.py tiedostosta, testauksen voi suorittaa komennolla:

	pytest

Ja kattavuusraportin saa komennoilla:

	coverage run -m pytest
 	coverage html

Jolloin htmlcov/index.html löytyy tarkka jäsentely testikattavuudesta

Koodin laatua voi tarkastella pylintillä komennolla:

	pylint app.py

En ole kirjoitushetkellä suorittanut kertaakaan, joten saa olettaa että koodi ei saa hyvää arvosanaa.


