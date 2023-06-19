### 23.1.2

* Fixed the patching of NVDA's speech.speech.speak, as it gained a new parameter in PR nvaccess/nvda#13483.
    + This was causing many failures of navigation and other things, when used with NVDA alphas.
    + Closes #5.
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
