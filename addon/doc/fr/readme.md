# Speech Logger #

* Auteur : Luke Davis, avec des contributions de James Scholes
* Télécharger [version stable][1]
* Compatibilité NVDA : 2019.3.1 et ultérieure

Une extension [NVDA](https://nvaccess.org/) pour journaliser la parole dans
un fichier ou des fichiers. Il peut enregistrer la parole générée sur la
machine locale dans un fichier texte. Il peut également enregistrer la
parole reçue à partir d'une machine distante via l'extension [NVDA
Remote](https://nvdaremote.com/) dans le même fichier ou un fichier
différent.

### Configuration

Pour configurer cette extension, ouvrez le menu NVDA, accédez aux
Préférences, puis Paramètres, puis Speech Logger (NVDA+N, P, P, puis appuyez
sur S jusqu'à que vous êtes arrivé là, sur un clavier français par défaut).
Il existe également un geste non attribué dans la catégorie "Configuration"
du dialogue Gestes de commandes que vous pouvez affecter et utiliser pour
ouvrir rapidement le dialogue des paramètres de l'extension.  Remarque :
L'extension ne peut être configurée que dans le profil de configuration
normal de NVDA. L'extension n'est pas conscient du profil. Si vous pouvez
penser à un cas d'utilisation qui le nécessite de fonctionner différemment
dans différents profils, veuillez contacter l'auteur ou déposer une
incidence (issue) sur le [dépôt GitHub][2].

### Les paramètres suivants sont disponibles :

* Le répertoire de journal. Vous pouvez saisir ou parcourir le répertoire de
  destination souhaité, qui doit déjà exister. Les variables système telles
  que%temp%, %userprofile%, etc., peuvent être utilisées dans ce champ.
* Nom de fichier journal local. Le fichier créé sera placé dans le
  répertoire ci-dessus. Cela contiendra la parole enregistrée pendant que le
  mode de journal local est engagé. Cela peut être le même que le fichier
  journal distant. Laissez vide pour désactiver complètement ce type de
  journalisation.
* Nom de fichier de journal distant. Le fichier créé sera placé dans le
  répertoire ci-dessus. Cela contiendra la parole enregistrée pendant que le
  mode de journal distant est engagé. Cela peut être le même que le fichier
  journal local. Laissez vide pour désactiver complètement ce type de
  journalisation.
* Séparateur. Cette liste déroulante vous permet de choisir l'un des
  séparateurs de messages disponibles. Voir ci-dessous pour plus
  d'informations.
* Séparateur personnalisé. Ce champ vous permet de saisir un séparateur de
  message personnalisé (voir ci-dessous), qui est utilisé si "Personnalisé"
  est choisi dans la liste déroulante.
* Mode d'horodatage. Cette liste déroulante vous permet de choisir entre
  aucun horodatage et un horodatage au début et à la fin de chaque session
  de journalisation.
* Journalisation de la parole pendant le mode Dire tout (lire jusqu'à la
  fin). Cette extension journalise la parole  généré lorsque vous appuyez
  sur NVDA+Flèche bas (NVDA+A dans la disposition du clavier pour ordinateur
  portable). Si vous préférez ne pas avoir ce genre de longue lecture
  narrative journalisée, décocher cette case.
* Commencer la journalisation au démarrage. Vous pouvez définir cette option
  sur "Toujours", si vous voulez que la parole soit enregistrée
  automatiquement lorsque NVDA démarre. Cela ne s'applique qu'à la parole
  locale, et la valeur par défaut est "Jamais".

#### Séparateur de messages

Lorsque NVDA verbalise quelque chose tel que "`Recycler les ordures 1 sur
55`" pendant qu'il lit votre bureau, cela est considéré comme deux messages
séparés.  Le premier est le nom de l'élément ("`Recycler les ordures`", dans
cet exemple), et le second est l'information de la position de l'objet ("`1
sur 55`", dans cet exemple).

Selon ce que vous lisez et comment vous avez configuré NVDA, il peut y avoir
plusieurs messages séparés qui se produisent pendant une seule séquence de
la parole.

Dans le journal NVDA normal au niveau de débogage, chaque message individuel
est séparé avec deux espaces, car il est écrit dans l'exemple ci-dessus.

Speech Logger vous permet de séparer les messages de la même manière que
NVDA fait (avec deux espaces), ou par l'une des quelques alternatives
raisonnables (une nouvelle ligne, une virgule et un espace, une tabulation,
deux soulignements), ou par une séquence personnalisée de votre propre
conception.

Si, par exemple, vous vouliez que votre séparateur de message soit de deux
signes de dollar (`$$`), vous définissez dans la liste déroulante sur
"Personnalisé" et entrez  "`$$`" (sans les guillemets), dans le champ
séparateur personnalisé.  Si vous vouliez que ce soit une nouvelle ligne
suivie d'une tabulation, vous pouvez entrer "`\n\t`".

### Démarrage et arrêt de la journalisation

Cette extension a deux gestes définis par défaut. Vous pouvez les modifier
sous la catégorie Outils dans le dialogue Gestes de commandes de NVDA.
Chercher dans "Bascule de journalisation de la parole locale" et "Bascule de
journalisation de la parole distante".

* NVDA+Alt+L : démarre / arrête la journalisation de la parole locale.
* NVDA+Shift+Alt+L : démarre / arrête la journalisation de la parole
  distante.

### Une note sur la journalisation de la parole distante

Cette extension est destiné à fonctionner avec l'extension NVDA Remote, pour
la journalisation de la parole distante.

Il est important de savoir qu'il n'est pas possible de démarrer la connexion
pour les sessions distantes jusqu'à ce que vous en démarriez une. Il n'y a
aucun moyen, par exemple, de démarrer la journalisation et de l'attendre, en
attente, jusqu'à ce qu'une session distante démarre et commence à
enregistrer à ce moment-là.

Cependant, une fois démarrée, la journalisation se poursuivra à travers les
sessions distantes.

### Commentaires et demandes de fonctionnalités

Si vous souhaitez suggérer une fonctionnalité ou signaler un bogue, veuillez
contacter par courriel, ou déposer une [incidence (issue)][2].

Comme toujours, j'apprécie d'entendre que mes extensions sont utiles et pour
quoi les gens les utilisent.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=speechLogger

[2]: https://github.com/opensourcesys/speechLogger/issues/new
