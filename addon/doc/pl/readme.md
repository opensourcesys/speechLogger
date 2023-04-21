# Speech Logger #

* Autor: Luke Davis, z wkładem Jamesa Scholesa
* Pobierz [wersja stabilna][1]
* Zgodność z NVDA: 2019.3.1 i nowsze

Dodatek NVDA do logowania mowy do pliku lub plików.  Może rejestrować mowę
wygenerowaną na komputerze lokalnym w pliku tekstowym.  Może również
rejestrować mowę ze zdalnego komputera odebraną za pośrednictwem dodatku
[NVDA Remote](https://nvdaremote.com/) do tego samego lub innego pliku.

### Ustawienia

Aby skonfigurować ten dodatek, otwórz menu NVDA, przejdź do Preferencje,
następnie Ustawienia, a następnie Rejestrator mowy (NVDA + N, P, S, a
następnie naciskaj S, aż tam dotrzesz, na domyślnej klawiaturze angielskiej
w USA).

Uwaga: dodatek można skonfigurować tylko w profilu normalnej konfiguracji
NVDA. Dodatek nie obsługuje profilu. Jeśli możesz wymyślić jakiś przypadek
użycia, który wymaga, aby działał inaczej w różnych profilach, skontaktuj
się z autorem lub zgłoś problem na [repozytorium GitHub]
(https://github.com/opensourcesys/speechLogger/issues/).

Dostępne są następujące ustawienia:

* Katalog dziennika. Możesz wprowadzić lub wyszukać żądany katalog docelowy,
  który musi już istnieć. Zmienne systemowe, takie jak %temp%, %userprofile%
  itp., Mogą być używane w tym polu.
* Nazwa pliku dziennika lokalnego. Utworzony plik zostanie umieszczony w
  powyższym katalogu. Będzie to zawierać mowę rejestrowaną, gdy włączony
  jest tryb dziennika lokalnego. Może to być to samo, co zdalny plik
  dziennika. Pozostaw puste, aby całkowicie wyłączyć ten rodzaj
  rejestrowania.
* Nazwa pliku dziennika zdalnego. Utworzony plik zostanie umieszczony w
  powyższym katalogu. Będzie to zawierać mowę rejestrowaną, gdy włączony
  jest tryb dziennika zdalnego. Może być taki sam jak lokalny plik
  dziennika. Pozostaw puste, aby całkowicie wyłączyć ten rodzaj
  rejestrowania.
* Separator. To pole kombi umożliwia wybranie jednego z dostępnych
  separatorów wypowiedzi. Więcej informacji można znaleźć poniżej.
* Separator niestandardowy. To pole umożliwia wprowadzenie niestandardowego
  separatora wypowiedzi (patrz poniżej), który jest używany, jeśli w polu
  kombi wybrano opcję "niestandardowy".

#### Separator wypowiedzi

Kiedy NVDA mówi coś takiego jak "kosz 1 z 55" podczas czytania pulpitu, jest
to uważane za dwie oddzielne wypowiedzi. Pierwszy z nich to nazwa elementu
("'Kosz'", w tym przykładzie), a drugi to informacja o położeniu obiektu
("'1 z 55'", w tym przykładzie).

W zależności od tego, co czytasz i jak skonfigurowałeś NVDA, może istnieć
kilka oddzielnych wypowiedzi, które zdarzają się podczas jednej sekwencji
mowy.

W normalnym dzienniku NVDA na poziomie debugowania każda pojedyncza
wypowiedź jest oddzielona dwiema spacjami, jak napisano w powyższym
przykładzie.

Speech Logger pozwala oddzielić wypowiedzi w taki sam sposób, jak NVDA (z
dwiema spacjami) lub przez jedną z kilku rozsądnych alternatyw (nowa linia,
przecinek i spacja, dwa podkreślenia) lub przez niestandardową sekwencję
własnego pomysłu.

Jeśli, na przykład, chcesz, aby separator wypowiedzi składał się z dwóch
znaków dolara ($$), ustaw pole kombi na "niestandardowe" i wpisz "$$" (bez
cudzysłowów) w polu separatora niestandardowego. Jeśli chcesz, aby była to
karta, możesz wpisać "\t".

### Uruchamianie i zatrzymywanie rejestrowania

Ten dodatek ma domyślnie ustawione dwa gesty. Możesz je zmienić w kategorii
Narzędzia gestów wejściowych NVDA.

Poszukaj "Przełącza rejestrowanie mowy lokalnej" i "Przełącza rejestrowanie
mowy zdalnej".

* NVDA+Alt+L: uruchamianie/zatrzymywanie rejestrowania mowy lokalnej.
* NVDA+Shift+Alt+L: rejestrowanie mowy zdalnej uruchamiania/zatrzymywania.

### Uwaga dotycząca zdalnego rejestrowania mowy

Ten dodatek jest przeznaczony do pracy z dodatkiem NVDA Remote do
rejestrowania mowy zdalnej.

Ważne jest, aby wiedzieć, że nie jest możliwe rozpoczęcie rejestrowania
sesji zdalnych, dopóki nie rozpoczniesz ich.  Nie ma sposobu, aby na
przykład rozpocząć rejestrowanie i poczekać w trybie gotowości, aż
rozpocznie się sesja zdalna, i rozpocząć rejestrowanie w tym czasie.

Jednak po rozpoczęciu rejestrowanie będzie kontynuowane w sesjach zdalnych.

### Opinie i prośby o funkcje

Jeśli chcesz zasugerować funkcję lub zgłosić błąd, skontaktuj się z nami
przez e-mail lub zgłoś
[problem](https://github.com/opensourcesys/speechLogger/issues/).

Jak zawsze, doceniam to, że moje dodatki są przydatne i do czego ludzie ich
używają.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=speechLogger
