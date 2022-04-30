### NVDA Speech Logger add-on

This file and add-on are works in progress.

### Configuration

To configure this add-on, open the NVDA menu, go to Preferences, then Settings, then Speech Logger (NVDA+N, P, S, S, S, on a default U.S. English keyboard).

The following settings are available:
* The log directory. You can enter or browse for your desired destination directory, which must already exist. System variables such as %temp%, %userprofile%, etc., can be used in this field.
* Local log filename. The created file will be placed in the above directory. This will contain speech logged while the local log mode is engaged.
* Remote log filename. The created file will be placed in the above directory. This will contain speech logged while the remote log mode is engaged.
* Separator. This combobox lets you choose one of the available utterance separators. See below for more information.
* Custom separator. This field lets you enter a custom utterance separator (see below), which is used if "custom" is chosen in the combobox.

#### Utterance separator

When NVDA speaks something such as "`recycle bin  1 of 55`" while it's reading your desktop, this is considered two separate utterances. The first one is the item name ("`Recycle bin`", in this example), and the second is the object position information ("`1 of 55`", in this example).

Depending on what you are reading, and how you have NVDA configured, there can be several separate utterances that happen during a single speech sequence.

In the normal NVDA log at debug level, each individual utterance is separated with two spaces, as it is written in the example above.

Speech Logger allows you to separate utterances in the same way NVDA does (with two spaces), or by one of a few reasonable alternatives (a newline, a comma and a space, two underscores), or by a custom sequence of your own devising.

If, for example, you wanted your utterance separator to be two dollar signs (`$$`), you would set the combobox to "custom", and enter "`$$`" (without the quotes), in the custom separator field.

### Starting and stopping logging

This add-on has no gestures set by default.
You have to define your own toggle gestures, under the NVDA Input Gestures Tools category.
Look for "Toggles logging of local speech" and "Toggles logging of remote speech".

### A note on remote speech logging

This add-on is intended to work with the NVDA Remote add-on, for logging of remote speech.

It is important to know, that it is not possible to start logging for remote sessions until you actually start one.
There is no way too, for example, start logging, and have it wait, on stand-by, until a remote session starts, and begin logging at that time.

However it currently appears from limited testing, that once started, logging will continue across remote sessions.
