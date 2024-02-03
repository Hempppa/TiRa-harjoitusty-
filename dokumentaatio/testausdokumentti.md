## Miten testit on tehty
Hetkellä on vain kaksi yksikkötestiä 'teesiirto()' funktiolle  apptest.py tiedostossa. Tähän kuitenkin tulen ajallaan lisäämään kaikille sovelluksen funktioille omat yksikkötestit.
## Kattavuusraportti
Noin 6%, laitan kuvan kun on sellainen määrä testejä että kehtaa näyttää.
## Miten testit ja kattavuusraportin saa itse suoritettua
Testit löytyvät app_test.py tiedostosta, testauksen voi suorittaa komennolla:

	pytest

Ja kattavuusraportin saa komennoilla:

	coverage run -m pytest
 	coverage html

Jolloin htmlcov/index.html löytyy tarkka jäsentely testikattavuudesta
## Suorituskykytestit
Hetkellä ei ainakaan ole, voin tulevaisuudessa lisätä jos tarvitsee/on järkevää tehdä silleen. Periaatteessa voin testata hieman erilaisia algoritmeja eri laskentasyvyyksillä
