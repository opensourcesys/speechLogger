# Puhelokin tallennin #

* Tekijä: Luke Davis yhteistyössä James Scholesin kanssa
* Lataa [vakaa versio][1]
* Yhteensopivuus: NVDA 2019.3.1 ja uudemmat

Tämä lisäosa tallentaa NVDA:n paikallisessa koneessa tuottaman puheen
tekstitiedostoon tai -tiedostoihin. Se voi tallentaa myös joko samaan tai
eri tiedostoon etäkoneessa tuotetun puheen, joka on vastaanotettu
[NVDA-etäkäyttö](https://nvdaremote.com/)-lisäosan kautta.

### Asetusten määrittäminen

Määritä tämän lisäosan asetukset avaamalla NVDA-valikko, siirtymällä
Asetukset-alivalikkoon, valitsemalla Asetukset ja sitten Puhelokin tallennin
(NVDA+N, A, A ja paina sitten P niin monta kertaa, että olet kohdassa
Puhelokin tallennin. Näppäinkomennot-valintaikkunan "Asetukset"-kategoriassa
on myös määrittämätön näppäinkomento, jonka määritettyäsi voit käyttää sitä
lisäosan asetusten avaamiseen. Huom: Tämä lisäosa voidaan määrittää vain
NVDA:n normaalissa asetusprofiilissa. Lisäosa ei tue useita
profiileja. Mikäli sinulla on mielessäsi jokin käyttötapaus, joka edellyttää
lisäosan toimimista eri tavalla eri profiileissa, ota yhteyttä tekijään tai
ilmoita ongelmasta [GitHubin koodivarastossa][2].

### Seuraavat asetukset ovat käytettävissä:

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
* Aikaleimatila. Tästä yhdistelmäruudusta voit valita kahden vaihtoehdon
  väliltä, jotka ovat "Ei käytössä" ja "Kun lokin tallennus alkaa tai
  päättyy".
* Tallenna puhelokia jatkuvaa lukua käytettäessä. Tämä lisäosa tallentaa
  lokiin puhetta, joka tuotetaan painettaessa NVDA+Nuoli alas (kannettavien
  näppäinasettelussa NVDA+A). Jos et halua tallentaa kaikkea jatkuvan luvun
  aikana puhuttua tekstiä, poista tämän valintaruudun valinta.
* Aloita lokin tallennus käynnistettäessä. Määritä asetukseksi "Aina",
  mikäli haluat, että puhelokin tallennus alkaa NVDA:n käynnistyessä. Tämä
  koskee vain paikallisen järjestelmän puhetta, ja oletusasetuksena on "Ei
  koskaan".

#### Puhekatkelmien erotin

Kun NVDA puhuu työpöytääsi lukiessaan jotain, kuten "`Roskakori 1/55`", sitä
pidetään kahtena erillisenä puhekatkelmana. Ensimmäinen on objektin nimi
("`Roskakori`") ja toinen on objektin sijaintitiedot ("`1/55`").

Riippuen siitä, mitä luet ja miten NVDA on määritetty, yksittäisen
puhesekvenssin aikana voi olla useita erillisiä katkelmia.

Normaalin NVDA-lokin virheenkorjaustasolla jokainen yksittäinen katkelma
erotetaan kahdella välilyönnillä, kuten yllä olevassa esimerkissä on
kirjoitettu.

Puhelokin tallentimen avulla voit erottaa katkelmat samalla tavalla kuin
NVDA (kahdella välilyönnillä) tai jollakin muutamasta järkevästä
vaihtoehdosta (rivinvaihto, pilkku ja välilyönti, sarkain, kaksi alaviivaa)
tai itse määrittämälläsi mukautetulla erottimella.

Jos esimerkiksi haluat katkelman erottimen olevan kaksi dollarimerkkiä
(`$$`), valitse yhdistelmäruudusta "Mukautettu" ja kirjoita mukautetun
erottimen kenttään "`$$`" ilman lainausmerkkejä. Jos haluat erottimeksi
rivinvaihdon ja sarkainmerkin, kirjoita "`\n\t`".

### Lokin tallennuksen aloittaminen ja lopettaminen

Tälle lisäosalle on määritetty kaksi oletusarvoista näppäinkomentoa. Voit
muuttaa niitä NVDA:n Näppäinkomennot-valintaikkunan
Työkalut-kategoriassa. Etsi kohtia "Ottaa käyttöön paikallisen puheen lokin
tallennuksen tai poistaa sen käytöstä" ja "Ottaa käyttöön etäpuheen lokin
tallennuksen tai poistaa sen käytöstä".

* NVDA+Alt+L: aloita/lopeta paikallisen puheen lokin tallennus.
* NVDA+Vaihto+Alt+L: aloita/lopeta etäpuheen lokin tallennus.

### Huomautus etäpuheen lokin tallennuksesta

Tämä lisäosa on tarkoitettu toimimaan NVDA-etäkäyttö-lisäosan kanssa
etäpuheen lokin tallentamiseen.

Etäistunnon lokin tallennusta ei voi aloittaa ennen kuin istunnon yhteys on
muodostettu. Ei ole mahdollista esimerkiksi aloittaa lokin tallennusta ja
odottaa valmiustilassa, kunnes etäistunto alkaa, ja aloittaa lokin
tallennusta vasta sitten.

Aloittamisen jälkeen lokin tallennus kuitenkin jatkuu etäistuntojen välillä.

### Palaute ja ominaisuuspyynnöt

Jos haluat ehdottaa ominaisuutta tai ilmoittaa bugista, ota yhteyttä
sähköpostitse tai tee [ongelmaraportti][2].

Kuten aina, arvostan kuullessani, että lisäosistani on hyötyä ja mihin niitä
käytetään.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=speechLogger

[2]: https://github.com/opensourcesys/speechLogger/issues/new
