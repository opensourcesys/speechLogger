# Sprachausgaben-Protokollierung #

* Autor: Luke Davis, mit Unterstützung von James Scholes
* [Stabile Version herunterladen][1]
* NVDA-Kompatibilität: 2019.3.1 und neuer

Eine NVDA-Erweiterung zur Protokollierung des Sprachausgabenverlaufs in
einer oder mehreren Dateien. Es kann auf dem lokalen Computer den
Sprachausgabenverlauf in eine Textdatei protokollieren. Es kann auch den
Sprachausgabenverlauf von einem Remote-Computer protokollieren, die über die
Erweiterung [Fernzugriff](https://nvdaremote.com/) empfangen wurde, entweder
in dieselbe oder eine andere Datei gespeichert werden.

### Konfiguration

Um diese Erweiterung zu konfigurieren, öffnen Sie das NVDA-Menü, gehen Sie
in die Einstellungen, dort wählen Sie Sprachausgaben-Protokollierung aus
(NVDA+N, O, E, dann drücken Sie S, bis Sie dorthin kommen).

Hinweis: Die Erweiterung kann nur im Profil "Normale Konfiguration" von NVDA
konfiguriert werden. Das Add-on ist nicht profilabhängig. Wenn Ihnen ein
Anwendungsfall einfällt, bei dem es in verschiedenen Profilen anders
funktionieren muss, wenden Sie sich bitte an den Autor oder melden Sie einen
Fehler im
[GitHub-Repository](https://github.com/opensourcesys/speechLogger/issues/).

Die folgenden Einstellungen sind verfügbar:

* Das Verzeichnis für die Protokollierung. Sie können das gewünschte
  Zielverzeichnis, das bereits existieren muss, eingeben oder danach
  suchen. Systemvariablen wie %temp%, %userprofile%, etc. können in diesem
  Feld verwendet werden.
* Dateiname für das eigene Protokoll. Die erstellte Datei wird in dem oben
  genannten Verzeichnis abgelegt. Sie enthält den Sprachausgabenverlauf, der
  im Protokollmodus aufgezeichnet wird. Dies kann dieselbe wie die Datei für
  die Remote-Protokollierung sein. Lassen Sie das Feld leer, um diese Art
  der Protokollierung vollständig zu deaktivieren.
* Dateiname für das Remote-Protokoll. Die erstellte Datei wird in dem oben
  genannten Verzeichnis abgelegt. Sie enthält den Sprachausgabenverlauf, der
  protokolliert wird, während der Remote-Protokollierungsmodus aktiviert
  ist. Sie kann dieselbe wie die Datei für eigene Protokollierung
  sein. Lassen Sie das Feld leer, um diese Art der Protokollierung
  vollständig zu deaktivieren.
* Trennzeichen. In diesem Kombinationsfeld können Sie eines der verfügbaren
  Trennzeichen für die Äußerungen auswählen. Siehe unten für weitere
  Informationen.
* Benutzerdefiniertes Trennzeichen. In dieses Feld können Sie ein
  benutzerdefiniertes Trennzeichen für die Äußerungen eingeben (siehe
  unten), welches verwendet wird, wenn in dem Kombinationsfeld
  "Benutzerdefiniert" ausgewählt wurde.

#### Trennzeichen für die Äußerungen

Wenn NVDA beim Lesen Ihres Desktops etwas wie "Papierkorb 1 von 55" sagt,
wird dies als zwei separate Äußerungen betrachtet. Die erste ist der Name
des Objekts ("Papierkorb", in diesem Beispiel) und die zweite ist die
Information über die Position des Objekts ("1 von 55", in diesem Beispiel).

Je nachdem, was Sie lesen und wie Sie NVDA konfiguriert haben, können
während einer einzigen Sprachsequenz mehrere separate Äußerungen erfolgen.

Im normalen NVDA-Protokoll auf der Debug-Stufe wird jede einzelne Äußerung
durch zwei Leerzeichen getrennt, wie im obigen Beispiel dargestellt.

Mit der Sprachausgaben-Protokollierung können Sie Äußerungen auf die gleiche
Weise wie NVDA trennen (mit zwei Leerzeichen) oder durch eine von mehreren
Alternativen (ein Zeilenumbruch, ein Komma und ein Leerzeichen, zwei
Unterstriche) oder durch eine benutzerdefinierte Sequenz, die Sie sich
selbst ausdenken.

Wenn Sie z. B. zwei Dollarzeichen ($$) als Trennzeichen für die Äußerungen
von der Sprachausgabe verwenden möchten, stellen Sie das Kombinationsfeld
auf "Benutzerdefiniert" ein und geben "$$" (ohne Anführungszeichen) in das
Feld für das benutzerdefinierte Trennzeichen ein. Wenn es ein Tabulator sein
soll, können Sie "`\t`" eingeben.

### Protokollierung starten und beenden

In dieser Erweiterung sind standardmäßig zwei Tastenbefehle
voreingestellt. Sie können sie im NVDA-Menü unter "Werkzeuge" in der
entsprechenden Kategorie im Dialogfeld für die Tastenbefehle anpassen.

Suchen Sie nach "Schaltet die Protokollierung der eigenen Sprachausgabe um"
und "Schaltet die Protokollierung der Remote-Sprachausgabe um".

* NVDA+Alt+L: Startet/beendet die Aufzeichnung der eigenen Sprachausgabe.
* NVDA+Umschalt+Alt+L: Startet/stoppt die Aufzeichnung der
  Remote-Sprachausgabe.

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
Sie sich bitte per E-Mail an uns oder melden Sie ein
[issue](https://github.com/opensourcesys/speechLogger/issues/).

Wie immer freue ich mich, wenn ich höre, dass meine Erweiterungen nützlich
sind und wofür sie verwendet werden.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=speechLogger
