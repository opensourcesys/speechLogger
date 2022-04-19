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

This add-on has no gestures set by default.
You have to define your own toggle gestures, under the NVDA Input Gestures Tools category.
Look for "Toggles logging of local speech" and "Toggles logging of remote speech".

### Notes

It is not possible to start logging for remote sessions, until you actually start one.
There is no way too, for example, start logging, and have it wait, on stand-by, until a remote session starts, and begin logging at that time.
The followup implication is also true: when the remote session ends, logging automatically stops.
(This is a forward-looking statement. You will currently get log errors or something until you toggle off logging, after a remote session ends.)
