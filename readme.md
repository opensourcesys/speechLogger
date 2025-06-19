### NVDA Speech Logger add-on

* Author: Luke Davis, with contributions by James Scholes
* Download [stable version][1]
* NVDA compatibility: 2019.3.1 and later

An [NVDA][3] add-on to log speech to a file or files.
It can log speech generated on the local machine into a text file.
It can also log speech from a remote machine received through the [NVDA Remote][5] add-on, either to the same or a different file.

**Note**: This feature is untested with NVDA's built in remote function, as of June, 2025.

### Configuration

To configure this add-on, open the NVDA menu, go to Preferences, then Settings, then Speech Logger (NVDA+N, P, S, then press S until you get there, on a default U.S. English keyboard).
There is also an unassigned gesture in the Input Gestures "Configuration" category, which you can assign and use to quickly open the add-on's settings directly.
Note: the add-on can only be configured while in the Normal Configuration profile of NVDA.
The add-on is not profile-aware.
If you can think of some use case that requires it to operate differently in different profiles, please contact the author or file an issue on the [GitHub repo][2].

### The following settings are available:

* The log directory. You can enter or browse for your desired destination directory, which must already exist. System variables such as %temp%, %userprofile%, etc., can be used in this field.
* Local log filename. The created file will be placed in the above directory. This will contain speech logged while the local log mode is engaged. This can be the same as the remote log file. Leave blank to disable this kind of logging completely.
* Remote log filename. The created file will be placed in the above directory. This will contain speech logged while the remote log mode is engaged. It can be the same as the local log file. Leave blank to disable this kind of logging completely.
* Separator. This combobox lets you choose one of the available utterance separators. See below for more information.
* Custom separator. This field lets you enter a custom utterance separator (see below), which is used if "custom" is chosen in the combobox.
* Timestamp mode. This combobox allows you to choose between no timestamps, and a timestamp at the start and end of each log session.
* Log speech during say-all (read to end) mode. This add-on logs speech generated when you press NVDA+DownArrow (NVDA+a in laptop layout). If you would rather not have that kind of narrative (potentially long) reading logged, un-check this box.
* Begin logging at startup. You can set this option to "Always", if you want speech to be logged automatically when NVDA starts. This only applies to local speech, and the default is "never".

#### Utterance separator

When NVDA speaks something such as "`recycle bin  1 of 55`" while it's reading your desktop, this is considered two separate utterances.
The first one is the item name ("`Recycle bin`", in this example), and the second is the object position information ("`1 of 55`", in this example).

Depending on what you are reading, and how you have NVDA configured, there can be several separate utterances that happen during a single speech sequence.

In the normal NVDA log at debug level, each individual utterance is separated with two spaces, as it is written in the example above.

Speech Logger allows you to separate utterances in the same way NVDA does (with two spaces), or by one of a few reasonable alternatives (a newline, a comma and a space, a tab, two underscores), or by a custom sequence of your own devising.

If, for example, you wanted your utterance separator to be two dollar signs (`$$`), you would set the combobox to "custom", and enter "`$$`" (without the quotes), in the custom separator field.
If you wanted it to be a newline followed by a tab, you could enter "`\n\t`".

### Controls:

This add-on has two keyboard shortcuts set by default, and one that is unassigned.

The default gestures, which you can change in the NVDA Input Gestures "`Speech Logger`" category, are:
* NVDA+Alt+L: start/stop logging of local speech.
* NVDA+Shift+Alt+L: start/stop logging of remote speech.
These are listed as "Toggles logging of local speech" and "Toggles logging of remote speech", respectively.

Additionally, it has one unassigned gesture for opening its configuration panel, which you may assign from the `Speech Logger` category in NVDA's Input Gestures.

### A note on remote speech logging

This add-on is intended to work with the NVDA Remote add-on, for logging of remote speech.

It is important to know, that it is not possible to start logging for remote sessions until you actually start one.
There is no way to, for example, start logging, and have it wait, on stand-by, until a remote session starts, and begin logging at that time.

However, once started, logging will continue across remote sessions.

### Feedback and feature requests

If you would like to suggest a feature or report a bug, please reach out by email, or file an [issue][2].

If you find this add-on useful, it would really help if you could [leave a review][4].

As always, I appreciate hearing that my add-ons are helpful, and finding out what people are using them for.

[1]: https://www.nvaccess.org/addonStore/legacy?file=speechLogger
[2]: https://github.com/opensourcesys/speechLogger/issues/new
[3]: https://nvaccess.org/
[4]: https://github.com/nvaccess/addon-datastore/discussions/2636
[5]: https://nvdaremote.com/
