### NVDA dodatak Zapisnik govora

* Autor: Luke Davis, uz doprinos Jamesa Scholesa
* Preuzmite [stabilnu verziju][1]
* NVDA kompatibilnost: 2019.3.1 i kasnije

[NVDA](https://nvaccess.org/) dodatak za zapisivanje govora u datoteku ili datoteke.
Može zapisati govor generiran na računalu u tekstualnu datoteku.
Također može zapisati govor s udaljenog računala primljen preko [NVDA Remote](https://nvdaremote.com/) dodatka, bilo u istu ili drugu datoteku.

### Konfiguracija

Za konfiguraciju ovog dodatka, otvorite NVDA izbornik, idite na Postavke, zatim Postavke, zatim Zapisnik govora (NVDA+N, P, P, zatim pritisnite Z dok ne dođete tamo, na zadanoj tipkovnici za hrvatski).

Napomena: dodatak se može konfigurirati samo dok je u profilu NVDA standardne konfiguracije.
Dodatak nije svjestan profila.
Ako se možete sjetiti nekog slučaja upotrebe koji zahtijeva različito funkcioniranje u različitim profilima, obratite se autoru ili prijavite problem na [GitHub repozitoriju][2].

### Dostupne su sljedeće postavke:

* Direktorij dnevnika. Možete unijeti ili pretraživati ​​željeni odredišni direktorij, koji već mora postojati. Varijable sustava kao što su %temp%, %userprofile%, itd., mogu se koristiti u ovom polju.
* Naziv datoteke dnevnika govora. Stvorena datoteka bit će smještena u gornji direktorij. Ovo će sadržavati govor koji se zapisuje dok je uključeno zapisivanje govora. To može biti isto što i datoteka udaljenog dnevnika. Ostavite prazno kako biste potpuno onemogućili ovu vrstu zapisivanja.
* Naziv datoteke dnevnika govora s udaljenog računala. Stvorena datoteka bit će smještena u gornji direktorij. Ovo će sadržavati zabilježeni govor dok je uključeno zapisivanje govora s udaljenog računala. Može biti ista kao lokalna datoteka dnevnika. Ostavite prazno kako biste potpuno onemogućili ovu vrstu zapisivanja.
* Razdjelnik. Ovaj odabirni okvir omogućuje vam odabir jednog od dostupnih razdjelnika izgovora. Više informacija potražite u nastavku.
* Prilagođeni razdjelnik. Ovo polje vam omogućuje da unesete prilagođeni razdjelnik izgovora (pogledajte dolje), koji se koristi ako je "Prilagođeno" odabrano u odabirnom okviru.
* Način vremenske oznake. Ovaj odabirni okvir omogućuje vam odabir između bez vremenskih oznaka i vremenske oznake na početku i kraju svake sesije dnevnika.
* Zapisuj govor u Izgovori sve (čita do kraja). Od verzije 23.2, ovaj dodatak zapisuje govor generiran kada pritisnete NVDA+Strelica dolje (NVDA+A u rasporedu prijenosnog računala). Ako radije ne biste da se ovo zapisuje, odznačite ovaj potvrdni okvir.

#### Razdjelnik izgovora

Kada NVDA izgovori nešto poput "Koš za smeće  1 od 55" dok čita vašu radnu površinu, to se smatra kao dva odvojena izgovora.
Prvi je naziv stavke ("Koš za smeće", u ovom primjeru), a drugi je informacija o položaju objekta ("1 od 55", u ovom primjeru).

Ovisno o tome što čitate i kako ste konfigurirali NVDA, može postojati nekoliko zasebnih izgovora koji će se dogoditi tijekom jedne govorne sekvence.

U standardnom NVDA dnevniku na razini otklanjanja pogrešaka, svaki pojedinačni izgovor odvojen je s dva razmaka, kao što je napisano u gornjem primjeru.

Zapisnik govora vam omogućuje da odvojite izgovore na isti način na koji to radi NVDA (s dva razmaka), ili pomoću jedne od nekoliko razumnih alternativa (novi red, zarez i razmak, tabulator, dvije podvlake), ili prilagođenim nizom.

Ako, na primjer, želite da vaš razdjelnik izgovora bude dva znaka dolara ($$), postavili biste kombinirani okvir na "Prilagođeno" i unijeli "$$" (bez navodnika) u polje za unos prilagođenog razdjelnika.
Ako želite da to bude novi redak nakon kojeg slijedi tabulator, možete unijeti "\n\t".

### Pokretanje i zaustavljanje zapisivanja

Ovaj dodatak ima dvije geste postavljene prema zadanim postavkama.
Možete ih promijeniti u kategoriji ulaznih gesti u NVDA alatima.
Potražite "Uključuje i isključuje zapisivanje govora" i "Uključuje i isključuje zapisivanje govora s udaljenog računala".
* NVDA+Alt+L: pokretanje/zaustavljanje zapisivanja govora.
* NVDA+Shift+Alt+L: pokretanje/zaustavljanje zapisivanja govora s udaljenog računala.

### Napomena o zapisivanju govora s udaljenog računala

Ovaj dodatak je namijenjen za rad s dodatkom Udaljena podrška, za zapisivanje govora s udaljenog računala.

Važno je znati da nije moguće pokrenuti zapisivanje govora udaljene sesije dok se stvarno ne spojite.
Ne postoji način da se, na primjer, započne zapisivanje, i čeka, u stanju pripravnosti, dok udaljena sesija ne započne, i počne zapisivati u tom trenutku.

Međutim, nakon pokretanja, zapisivanje će se nastaviti kroz udaljene sesije.

### Povratne informacije i zahtjevi za značajke

Ako želite predložiti značajku ili prijaviti grešku, javite se e-poštom ili pošaljite [problem][2].

Kao i uvijek, drago mi je čuti da su moji dodaci korisni i za što ih ljudi koriste.

[1]: https://www.nvaccess.org/addonStore/legacy?file=speechLogger
[2]: https://github.com/opensourcesys/speechLogger/issues/new
