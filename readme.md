### NVDA Speech Logger add-on

This file and add-on are works in progress.

### No UI

This add-on doesn't currently have a GUI to configure it.
It tries to have sane defaults, but you may want to change the configuration.

To do this, open the source file in %appdata%\nvda\addons\speechLogger\globalPlugins\speechLogger.py, and edit the "configuration" section according to your preferences.

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
(This is a forward-looking statement. You will currently get undefined behavior until you toggle off logging, after a remote session ends.)

### Known bugs

As of 22.0.9:
* Speech is broken up in the log files by newlines between each utterance of a sequence. That results in some blocks that are broken up where one might not expect. I can easily fix this, but haven't decided whether it is a desirable thing or not. Comments welcome.
* After starting remote logging, it can not be stopped while the session is still connected. It is untested what happens if one session is disconnected, logging is left running, and another session is started.
* There was a periodic clash between Speech Logger and Speech History while this add-on was in development. I am unsure if it has been resolved by the latest version; interoperability with Speech History was not my immediate goal for this alpha series. Disable one of them if anything strange happens, such as NVDA log errors involving speech.speech.speak, or Speech History, or strange event failures.
