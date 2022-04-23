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

However it currently appears from limited testing, that once started, logging will continue across remote sessions.

As of 22.0.10, speech is now broken up by the same two spaces which NVDA uses in its own log. That is, when a speech sequence contains multiple spoken chunks, they will be separated by two spaces instead of the newline that was previously used.

This text separator is configurable in the Configuration section of the add-on.

### Known bugs

As of 22.0.10:
* There was a periodic clash between Speech Logger and Speech History while this add-on was in development. I am unsure if it has been resolved by the latest version; interoperability with Speech History was not my immediate goal for this alpha series. Disable one of them if anything strange happens, such as NVDA log errors involving speech.speech.speak, or Speech History, or strange event failures.
