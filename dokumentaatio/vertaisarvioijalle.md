
## Sovelluksen käyttäminen
Sovelluksen käyttämiseen ei tarvitse asentaa riippuvaisuuksia. Sovelluksella on hetkellä (ehkä myös pysyvästi) vain tekstikäyttöliittymä komentorivillä. Ainakin linuxissa (varmaan windowsilla on ainakin samankaltainen) sovelluksen saa käynnistettyä juurikansiosta komennolla:

	python3 app.py

Jonka jälkeen sovellus kysyy pelataanko yksin shakkibottia vastaan "1P" vai kaksinpeliä "2P" (lokaalisti eli samalla koneella vuorotellen vain). Shakkibotti ei ole hirveän hiottu ja laskentasyvyys on alkuun vain 3, eli botti ei ole varmaan hirveän hyvä. Jos kuitenkin huomaa, että botti ei voita selviä voittavia tilanteita tai häivää tarkoituksella niin kannattaa siitä sanoa. Laskentasyvyyttä voi koodissa ensimmäisillä riveillä muuttaa jos haluaa, mutta laskenta hidastuu eksponentiaalisesti, eli ei kannata yli 4.

Siirtoja syötetään muodossa alku x, alku y, loppu x, loppu y. Eli esim. siirto ruudulta e2 ruutuun e4 on "e2e4". Myöhemmin saattaa tulla erikoisempia siirtoja peliin mutta hetkellä mm. tornitus, ohestalyönti, sotilaan korotus eivät ole pelissä.

Pelistä voi aina poistua syöttämällä "quit".

## Testaaminen ja laaduntarkastus
Ei kannata tehdä, en ole kerennyt tehdä kuin pari yksikkötestiä tai korjata pylintin palautteella koodin laatua. Jos kuitenkin välttämättä haluaa testejä itse suorittaa niin pitää asentaa riippuvaisuuksia, käyttöohjeessa lisää.

