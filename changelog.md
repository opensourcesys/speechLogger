### 24.2.0

* Use the pre_speech extensionPoint to obtain speech, instead of patching, if supported by NVDA. Still must patch for say-all.

### 24.1.0

* Move the input gestures from the "tools" category, to a language-specific category named for the add-on.
* Compatibility with NVDA 2024.1.
* Added a request for reviews to the readme.

### 23.3.01

* New feature: can be configured to automatically start logging at NVDA startup. (#9)
* Now stop all logging during add-on termination (fixes unreported bug with plugin reloads).

### 23..2.08

* Fixed the position of a checkbox in configuration display (contributed in #8 by @CyrilleB79).

### 23.2.05

* Internal: adapt to gui.MainFrame.popupSettingsDialog becoming part of the public API.

### 23.2.03

* Added an unassigned Input Gesture in the Configuration category, to open Speech Logger settings.
* Included a manual Croatian translation contributed by a user.

### 23.2.0

* Added the ability to log speech during say all (continuous reading/read to end). Closes #6.
    + Though enabled by default, this can be disabled by a checkbox in the add-on settings.
* Custom separator field is now disabled in settings, unless "custom" is chosen as separator type.
* Use an extensionPoint internally to handle config change notifications and reloads.

### 23.1.2

* Fixed the patching of NVDA's speech.speech.speak, as it gained a new parameter in PR nvaccess/nvda#13483.
    + This was causing many failures of navigation and other things, when used with NVDA alphas.
    + Closes #5.
    + The NVDA PR which caused this, was reverted in a later alpha; but nothing more needed to change on our end.
* More translation updates.

### 23.1.0

* Added tab as an optional utterance separator.
* A log-only message line is written to the file, whenever logging starts or stops.
    - The message states what has happened, and includes an optional timestamp.
* Updated the settings dialog description.
* Added an "Other options" grouping, and a Timestamp Mode combobox to the settings dialog.
    - Can choose either "off, no timestamps", or "When logging starts or stops", as the timestamp mode.
    - The default is to provide timestamps when logging starts and stops.
* Various under the hood changes, to make way for new features later, and improve code.
