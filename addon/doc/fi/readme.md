# Puheen tallennin #

* Tekijä: Luke Davis yhteistyössä James Scholesin kanssa
* Lataa [vakaa versio][1]
* Yhteensopivuus: NVDA 2019.3.1 ja uudemmat

Tämä lisäosa tallentaa NVDA:n tuottaman puheen tiedostoon tai
tiedostoihin. Se voi tallentaa joko samaan tai eri tiedostoon paikallisella
koneella tai etäkoneessa tuotetun puheen, joka on vastaanotettu
[NVDA-etäkäyttö](https://nvdaremote.com/)-lisäosan kautta.

### Asetusten määrittäminen

Määritä tämän lisäosan asetukset avaamalla NVDA-valikko, menemällä
Asetukset-alivalikkoon, valitsemalla Asetukset ja sitten Puheen tallennin
(NVDA+N, A, A ja paina sitten P kunnes tulet tämän lisäosan kategorian
kohdalle).

Huom: Tämä lisäosa voidaan määrittää vain NVDA:n normaalissa
asetusprofiilissa. Lisäosa ei tue useita profiileita. Mikäli sinulla on
mielessäsi jokin käyttötapaus, joka edellyttää lisäosan toimimista eri
tavalla eri profiileissa, ota yhteyttä tekijään tai ilmoita ongelmasta
[GitHub-koodiarkistossa]
(https://github.com/opensourcesys/speechLogger/issues/).

Seuraavat asetukset ovat käytettävissä:

* Lokihakemisto. Voit kirjoittaa tai etsiä haluamasi olemassa olevan
  hakemiston. Ympäristömuuttujia, kuten %temp%, %userprofile% jne., voidaan
  käyttää tässä kentässä.
* Paikallisen puheen lokitiedosto. Luotu tiedosto sijoitetaan yllä
  määritettyyn hakemistoon. Tämä tiedosto sisältää puheen, joka on
  tallennettu paikallisen puheen tallennustilan ollessa käytössä. Tämä voi
  olla sama kuin etäpuheen lokitiedosto. Poista paikallisen puheen tallennus
  kokonaan käytöstä jättämällä tämä kenttä tyhjäksi.
* Etäpuheen lokitiedosto. Luotu tiedosto sijoitetaan yllä määritettyyn
  hakemistoon. Tämä tiedosto sisältää puheen, joka on tallennettu etäpuheen
  tallennustilan ollessa käytössä. Se voi olla sama kuin paikallisen puheen
  lokitiedosto. Poista etäpuheen tallennus kokonaan käytöstä jättämällä tämä
  kenttä tyhjäksi.
* Erotin. Tästä yhdistelmäruudusta voit valita jonkin käytettävissä olevista
  puhekatkelmien erottimista. Katso lisätietoja alta.
* Mukautettu erotin. Tähän kenttään voit kirjoittaa haluamasi puhekatkelmien
  erottimen (katso alta), jota käytetään, jos yhdistelmäruudussa on
  valittuna "Mukautettu".

#### Puhekatkelmien erotin

Kun NVDA puhuu työpöytääsi lukiessaan jotain, kuten "Roskakori 1/55", sitä
pidetään kahtena erillisenä puhekatkelmana. Ensimmäinen on objektin nimi
("Roskakori") ja toinen on objektin sijaintitiedot ("`1/55`").

Riippuen siitä, mitä luet ja miten NVDA on määritetty, yksittäisen
puhesekvenssin aikana voi olla useita erillisiä katkelmia.

Normaalin NVDA-lokin virheenkorjaustasolla jokainen yksittäinen katkelma
erotetaan kahdella välilyönnillä, kuten yllä olevassa esimerkissä on
kirjoitettu.

Puheen tallentimen avulla voit erottaa katkelmat samalla tavalla kuin NVDA
(kahdella välilyönnillä), jollakin muutamasta järkevästä vaihtoehdosta
(rivinvaihto, pilkku ja välilyönti, kaksi alaviivaa) tai itse
määrittämälläsi mukautetulla erottimella.

Jos esimerkiksi haluat katkelman erottimen olevan kaksi dollarimerkkiä
(`$$`), valitse yhdistelmäruudusta "Mukautettu" ja kirjoita mukautetun
erottimen kenttään "`$$`" (ilman lainausmerkkejä). Jos haluat erottimeksi
sarkainmerkin, kirjoita "`\t`".

### Tallennuksen aloittaminen ja lopettaminen

Tällä lisäosalla on kaksi oletusarvoisesti määritettyä näppäinkomentoa. Voit
muuttaa niitä NVDA:n Näppäinkomennot-valintaikkunan Työkalut-kategoriassa.

Etsi kohtia "Ottaa käyttöön tai poistaa käytöstä paikallisen puheen
tallennuksen" ja "Ottaa käyttöön tai poistaa käytöstä etäpuheen
tallennuksen".

* NVDA+Alt+L: aloita/lopeta paikallisen puheen tallennus.
* NVDA+Vaihto+Alt+L: aloita/lopeta etäpuheen tallennus.

### Huomautus etäpuheen tallennuksesta

Tämä lisäosa on tarkoitettu toimimaan NVDA-etäkäyttö-lisäosan kanssa
etäpuheen tallentamiseen.

Etäistuntojen tallentamista ei voi aloittaa ennen kuin aloitat sellaisen. Ei
ole mahdollista esimerkiksi aloittaa tallennusta ja odottaa valmiustilassa,
kunnes etäistunto alkaa, ja aloittaa tallennusta tuolloin.

Aloittamisen jälkeen tallennus kuitenkin jatkuu etäistuntojen välillä.

### Palaute ja ominaisuuspyynnöt

Jos haluat ehdottaa ominaisuutta tai ilmoittaa bugista, ota yhteyttä
sähköpostitse tai tee
[raportti](https://github.com/opensourcesys/speechLogger/issues/).

Kuten aina, arvostan kuullessani, että lisäosistani on hyötyä ja mihin niitä
käytetään.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=speechLogger
