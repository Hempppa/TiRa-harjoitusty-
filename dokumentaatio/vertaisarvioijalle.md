
## Sovelluksen käyttäminen
Sovelluksen käyttämiseen ei tarvitse asentaa riippuvaisuuksia. Sovelluksella on hetkellä (ehkä myös pysyvästi) vain tekstikäyttöliittymä komentorivillä. Ainakin linuxissa (varmaan windowsilla on ainakin samankaltainen) sovelluksen saa käynnistettyä juurikansiosta komennolla:

	python3 app.py

Jonka jälkeen sovellus kysyy pelataanko yksin shakkibottia vastaan "1P" vai kaksinpeliä "2P" (lokaalisti eli samalla koneella vuorotellen vain). Jos shakkibottia vastaan pelatessa huomaa, että botti ei voita selviä voittavia tilanteita, rikkoo pelin sääntöjä tai häivää tarkoituksella niin kannattaa siitä sanoa. Laskentasyvyyttä voi koodissa ensimmäisillä riveillä muuttaa jos haluaa, mutta laskenta hidastuu eksponentiaalisesti, eli ei kannata laittaa yli 5.

Siirtoja syötetään muodossa alku x, alku y, loppu x, loppu y. Eli esim. siirto ruudulta e2 ruutuun e4 on "e2e4". Myöhemmin saattaa tulla erikoisempia siirtoja peliin mutta hetkellä mm. tornitus, ohestalyönti, sotilaan korotus eivät ole pelissä.

Pelistä voi aina poistua syöttämällä "quit".
