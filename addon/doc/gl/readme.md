# Speech Logger #

* Autor: Luke Davis, con contribucións de James Scholes
* Descargar [versión estable][1]
* Compatibilidade con NVDA: 2019.3.1 e posteriores

An [NVDA](https://nvaccess.org/) add-on to log speech to a file or files.
It can log speech generated on the local machine into a text file.  It can
also log speech from a remote machine received through the [NVDA
Remote](https://nvdaremote.com/) add-on, either to the same or a different
file.

### Configuración

To configure this add-on, open the NVDA menu, go to Preferences, then
Settings, then Speech Logger (NVDA+N, P, S, then press S until you get
there, on a default U.S. English keyboard).  There is also an unassigned
gesture in the Input Gestures "Configuration" category, which you can assign
and use to quickly open the add-on's settings directly.  Note: the add-on
can only be configured while in the Normal Configuration profile of NVDA.
The add-on is not profile-aware.  If you can think of some use case that
requires it to operate differently in different profiles, please contact the
author or file an issue on the [GitHub repo][2].

### Están dispoñibles as seguintes opcións:

* O directorio de rexistro (log directory). Podes introducir ou explorar o
  teu directorio de destino desexado, que debe existir xa. Pódense utilizar
  neste campo variables do sistema como %temp%, %userprofile%, etc.
* Nome de arquivo do rexistro local (local log filename). O arquivo creado
  porase no directorio de arriba. Conterá a fala rexistrada mentres o modo
  de rexistro local estea activado. Pode ser o mesmo que o arquivo de
  rexistro remoto. déixao en blanco para desactivar este tipo de rexistro
  por completo.
* Nome de arquivo do rexistro remoto (remote log filename). O arquivo creado
  porase no directorio de arriba. Conterá a fala rexistrada mentres o modo
  de rexistro remoto estea activado. Pode ser o mesmo que o arquivo de
  rexistro local. déixao en blanco para desactivar este tipo de rexistro por
  completo.
* Separador (separator). Esta caixa combinada permíteche escoller un dos
  separadores de declaración dispoñibles. consulte a continuación para máis
  información.
* Separador persoalizado (custom separator). Este campo permíteche
  introducir un separador de declaración persoalizado (consulte a
  continuación), que se utiliza se "custom" (persoalizado) está seleccionado
  na caixa combinada.
* Timestamp mode. This combobox allows you to choose between no timestamps,
  and a timestamp at the start and end of each log session.
* Log speech during say-all (read to end) mode. This add-on logs speech
  generated when you press NVDA+DownArrow (NVDA+a in laptop layout). If you
  would rather not have that kind of narrative long reading logged, un-check
  this box.
* Begin logging at startup. You can set this option to "Always", if you want
  speech to be logged automatically when NVDA starts. This only applies to
  local speech, and the default is "never".

#### separador de declaración

When NVDA speaks something such as "`recycle bin 1 of 55`" while it's
reading your desktop, this is considered two separate utterances.  The first
one is the item name ("`Recycle bin`", in this example), and the second is
the object position information ("`1 of 55`", in this example).

En función do que esteas lendo, e de como teñas NVDA configurado, pode haber
varias declaracións separadas que se produzan durante unha soa secuencia de
fala.

No rexistro normal de NVDA en modo depuración, cada declaración individual
sepárase con dous espazos, como está escrito no exemplo de arriba.

Speech Logger allows you to separate utterances in the same way NVDA does
(with two spaces), or by one of a few reasonable alternatives (a newline, a
comma and a space, a tab, two underscores), or by a custom sequence of your
own devising.

If, for example, you wanted your utterance separator to be two dollar signs
(`$$`), you would set the combobox to "custom", and enter "`$$`" (without
the quotes), in the custom separator field.  If you wanted it to be a
newline followed by a tab, you could enter "`\n\t`".

### Iniciando e detendo o rexistro

This add-on has two gestures set by default.  You can change them in the
NVDA Input Gestures Tools category.  Look for "Toggles logging of local
speech" and "Toggles logging of remote speech".

* NVDA+Alt+L: iniciar/deter rexistro de fala local.
* NVDA+Shift+Alt+L: iniciar/deter rexistro de fala remota.

### Unha nota sobre o rexistro de fala remota

Este complemento está pensado para traballar co complemento NVDA Remote,
para o rexistro de fala remota.

É importante saber, que non é posible iniciar o rexistro de sesións remotas
ata que non empeces unha realmente.  Non hai forma de, por exemplo, iniciar
o rexistro, e facer que agarde, en segundo plano, a que comece unha sesión
remota, e que comece o rexistro nese momento.

Porén, unha vez empece unha, o rexistro continuará aínda que se cambie de
sesión.

### Comentarios e solicitudes de características

If you would like to suggest a feature or report a bug, please reach out by
email, or file an [issue][2].

Coma sempre, gústame escoitar que os meus complementos son útiles, e para
que os está a utilizar a xente.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=speechLogger

[2]: https://github.com/opensourcesys/speechLogger/issues/new
