# Aufzeichnung des Sprachausgabenverlaufs #

### NVDA Speech Logger add-on

* Autoren: Luke Davis, mit Unterstützung von James Scholes
* [Stabile Version herunterladen][1]
* NVDA-Kompatibilität: 2019.3.1 und neuer

An [NVDA][3] add-on to log speech to a file or files.  It can log speech
generated on the local machine into a text file.  It can also log speech
from a remote machine received through the [NVDA Remote][5] add-on, either
to the same or a different file.

### Konfiguration

Um diese NVDA-Erweiterung zu konfigurieren, öffnen Sie das NVDA-Menü, gehen
Sie  dann zu Optionen, dann zu Einstellungen und wählen Sie die Kategorie
"SpeechLogger" aus.
Es gibt auch einen nicht zugewiesenen Tastenbefehl in der Kategorie
"Konfiguration", die Sie zuweisen und verwenden können, um die Einstellungen
der NVDA-Erweiterung direkt zu öffnen.
Hinweis: Die NVDA-Erweiterung kann nur im Profil "Normale Konfiguration" von
NVDA konfiguriert werden. Die NVDA-Erweiterung ist nicht
profilabhängig. Wenn Ihnen ein Anwendungsfall einfällt, bei dem es in
verschiedenen Profilen anders funktionieren muss, wenden Sie sich bitte an
den Autor oder melden Sie einen Fehler im Repository auf [GitHub][2].

### Die folgenden Einstellungen sind verfügbar:

* Das Verzeichnis für die Protokollierung. Sie können das gewünschte
  Zielverzeichnis, das bereits existieren muss, eingeben oder danach
  suchen. Systemvariablen wie %temp%, %userprofile%, etc. können in diesem
  Feld verwendet werden.
* Dateiname für das Protokoll auf Ihrem Computer. Die erstellte Datei wird
  in dem oben genannten Verzeichnis abgelegt. Sie enthält den
  Sprachausgabenverlauf, der im Protokollmodus aufgezeichnet wird. Dies kann
  dieselbe wie die Datei für die Remote-Protokollierung sein. Lassen Sie das
  Feld leer, um diese Art der Protokollierung vollständig zu deaktivieren.
* Dateiname für das Protokoll auf dem Remote-Computer. Die erstellte Datei
  wird in dem oben genannten Verzeichnis abgelegt. Sie enthält den
  Sprachausgabenverlauf, der protokolliert wird, während der
  Remote-Protokollierungsmodus aktiviert ist. Sie kann dieselbe wie die
  Datei für eigene Protokollierung sein. Lassen Sie das Feld leer, um diese
  Art der Protokollierung vollständig zu deaktivieren.
* Trennzeichen. In diesem Kombinationsfeld können Sie eines der verfügbaren
  Trennzeichen für die Äußerungen auswählen. Siehe unten für weitere
  Informationen.
* Benutzerdefiniertes Trennzeichen. In dieses Feld können Sie ein
  benutzerdefiniertes Trennzeichen für die Äußerungen eingeben (siehe
  unten), welches verwendet wird, wenn in dem Kombinationsfeld
  "Benutzerdefiniert" ausgewählt wurde.
* Zeitstempel-Modus. In diesem Kombinationsfeld können Sie wählen zwischen
  keinem Zeitstempel und einem Zeitstempel zu Beginn und am Ende jeder
  Protokollsitzung.
* Aufzeichnung der Sprachausgabe während Alles Vorlesen (liest bis zum
  Ende). Ab Version 2023.2 protokolliert diese NVDA-Erweiterung die
  Sprachausgabe, wenn Sie NVDA+Pfeiltaste nach unten im Desktop-Layout oder
  NVDA+A im Laptop-Layout drücken. Wenn Sie dies nicht wünschen,
  deaktivieren Sie ganz einfach dieses Kontrollkästchen.
* Protokollierung beim Starten beginnen. Sie können diese Option auf "Immer"
  einstellen, wenn Sie möchten, dass die Sprachausgabe automatisch beim
  Start von NVDA protokolliert wird. Dies gilt nur lokal für die
  Sprachausgabe auf dem eigenen Computer, und die Standard-Einstellung ist
  "Niemals".

#### Trennzeichen für die Äußerungen

Wenn NVDA beim Vorlesen auf dem Desktop etwas wie "Papierkorb 1 von 55"
sagt, wird dies als zwei separate Äußerungen betrachtet.  Die erste ist der
Name des Objekts ("Papierkorb", in diesem Beispiel) und die zweite ist die
Information über die Objekt-Position ("1 von 55", in diesem Beispiel).

Je nachdem, was Sie lesen und wie Sie NVDA konfiguriert haben, können
während einer einzigen Sprachsequenz mehrere separate Äußerungen erfolgen.

Im normalen NVDA-Protokoll auf der Debug-Stufe wird jede einzelne Äußerung
durch zwei Leerzeichen getrennt, wie im obigen Beispiel dargestellt.

Mit den Aufzeichnungen des Sprachausgabenverlaufs können Äußerungen auf die
gleiche Weise wie NVDA getrennt werden (mit zwei Leerzeichen), oder durch
eine von mehreren sinnvollen Alternativen (ein Zeilenumbruch, ein Komma und
ein Leerzeichen, ein Tabulator, zwei Unterstriche), oder durch eine
benutzerdefinierte Trennzeichendequenz, die Sie sich selbst ausdenken.

Wenn Sie z. B. zwei Dollarzeichen ($$) als Trennzeichen verwenden möchten,
stellen Sie das Kombinationsfeld auf "benutzerdefiniert" und geben "$$"
(ohne Anführungszeichen) in das Feld für das benutzerdefinierte Trennzeichen
ein. Wenn einen Zeilenumbruch gefolgt von einem Tabulatorzeichen sein soll,
können Sie "\n\t" eingeben.

### Controls:

This add-on has two keyboard shortcuts set by default, and one that is
unassigned.

The default gestures, which you can change in the NVDA Input Gestures
"`Speech Logger`" category, are:

* NVDA+Alt+L: Startet/beendet die Aufzeichnung der eigenen Sprachausgabe.
* NVDA+Umschalt+Alt+L: Startet/stoppt die Aufzeichnung der
  Remote-Sprachausgabe.

These are listed as "Toggles logging of local speech" and "Toggles logging
of remote speech", respectively.

Additionally, it has one unassigned gesture for opening its configuration
panel, which you may assign from the `Speech Logger` category in NVDA's
Input Gestures.

### Ein Hinweis zur Aufzeichnung der Remote-Sprachausgabe

Diese Erweiterung ist für die Zusammenarbeit mit der Erweiterung für den
Fernzugriff zur Protokollierung der Remote-Sprachausgabe vorgesehen.

Es ist wichtig zu wissen, dass es nicht möglich ist, die Protokollierung für
Fernsitzungen zu starten, bevor Sie nicht tatsächlich eine Sitzung gestartet
haben.  Es gibt keine Möglichkeit, die Protokollierung zu starten und sie im
Standby-Modus warten zu lassen, bis eine Fernsitzung beginnt, und dann mit
der Protokollierung zu beginnen.

Einmal gestartet, wird die Protokollierung jedoch über alle Remote-Sitzungen
hinweg fortgesetzt.

### Feedback und Feature-Anfragen

Wenn Sie eine Funktion vorschlagen oder einen Fehler melden möchten, wenden
Sie sich bitte per E-Mail an uns oder melden Sie ein [Problem][2].

If you find this add-on useful, it would really help if you could [leave a
review][4].

As always, I appreciate hearing that my add-ons are helpful, and finding out
what people are using them for.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=speechLogger

[2]: https://github.com/opensourcesys/speechLogger/issues/new

[3]: https://nvaccess.org/

[4]: https://github.com/nvaccess/addon-datastore/discussions/2636

[5]: https://nvdaremote.com/
