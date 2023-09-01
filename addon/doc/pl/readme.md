# Speech Logger #

* Autor: Luke Davis, z wkładem Jamesa Scholesa
* Pobierz [wersja stabilna][1]
* Zgodność z NVDA: 2019.3.1 i nowsze

An [NVDA](https://nvaccess.org/) add-on to log speech to a file or files.
It can log speech generated on the local machine into a text file.  It can
also log speech from a remote machine received through the [NVDA
Remote](https://nvdaremote.com/) add-on, either to the same or a different
file.

### Ustawienia

To configure this add-on, open the NVDA menu, go to Preferences, then
Settings, then Speech Logger (NVDA+N, P, S, then press S until you get
there, on a default U.S. English keyboard).  There is also an unassigned
gesture in the Input Gestures "Configuration" category, which you can assign
and use to quickly open the add-on's settings directly.  Note: the add-on
can only be configured while in the Normal Configuration profile of NVDA.
The add-on is not profile-aware.  If you can think of some use case that
requires it to operate differently in different profiles, please contact the
author or file an issue on the [GitHub repo][2].

### Dostępne są następujące ustawienia:

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
* Timestamp mode. This combobox allows you to choose between no timestamps,
  and a timestamp at the start and end of each log session.
* Log speech during say-all (read to end) mode. This add-on logs speech
  generated when you press NVDA+DownArrow (NVDA+a in laptop layout). If you
  would rather not have that kind of narrative long reading logged, un-check
  this box.
* Begin logging at startup. You can set this option to "Always", if you want
  speech to be logged automatically when NVDA starts. This only applies to
  local speech, and the default is "never".

#### Separator wypowiedzi

When NVDA speaks something such as "`recycle bin 1 of 55`" while it's
reading your desktop, this is considered two separate utterances.  The first
one is the item name ("`Recycle bin`", in this example), and the second is
the object position information ("`1 of 55`", in this example).

W zależności od tego, co czytasz i jak skonfigurowałeś NVDA, może istnieć
kilka oddzielnych wypowiedzi, które zdarzają się podczas jednej sekwencji
mowy.

W normalnym dzienniku NVDA na poziomie debugowania każda pojedyncza
wypowiedź jest oddzielona dwiema spacjami, jak napisano w powyższym
przykładzie.

Speech Logger allows you to separate utterances in the same way NVDA does
(with two spaces), or by one of a few reasonable alternatives (a newline, a
comma and a space, a tab, two underscores), or by a custom sequence of your
own devising.

If, for example, you wanted your utterance separator to be two dollar signs
(`$$`), you would set the combobox to "custom", and enter "`$$`" (without
the quotes), in the custom separator field.  If you wanted it to be a
newline followed by a tab, you could enter "`\n\t`".

### Uruchamianie i zatrzymywanie rejestrowania

This add-on has two gestures set by default.  You can change them in the
NVDA Input Gestures Tools category.  Look for "Toggles logging of local
speech" and "Toggles logging of remote speech".

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

If you would like to suggest a feature or report a bug, please reach out by
email, or file an [issue][2].

Jak zawsze, doceniam to, że moje dodatki są przydatne i do czego ludzie ich
używają.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=speechLogger

[2]: https://github.com/opensourcesys/speechLogger/issues/new
