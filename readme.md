## NVDA Speech Logger add-on

This file and add-on are works in progress.

### No UI

This add-on doesn't currently have a GUI to configure it.
It tries to have sane defaults, but you may want to change the configuration.

To do this, open the source file in globalPlugins\speechLogger.py, and edit the "configuration" section according to your preferences.

### Default output files

By default, the output logs are stored as follows:

* Local speech is stored in `%temp%\nvda-speech.log`.
* Remote speech is stored in `%temp%\nvda-speech-remote.log`.

### Starting and stopping logging

This add-on has no gesture set by default.

It supports one: a gesture to toggle whether it is logging or not.
To set this, open NVDA's Input Gestures dialog (NVDA+N, P, N), and configure the shortcut key for "Toggles speech logging" under the Tools category.
