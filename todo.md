### Things to do:

#### Priority 1:

* Add tab as a pre-configured separator option. (2/20/2023)
* Write dates to the files when logging starts and stops. (2/20/2023)
* Stop creating files before they need to be written to the first time. (2/20/2023)

#### Priority 2:

* Replace the Any types in configUI.setConf, with more likely typings. (2/18/2023)
* Add a config validation function, to check on directory provided.
* Make rotation work.
* Disable the custom field, if custom isn't selected.

#### Priority 3:

* Use the extensionpoint post_configReset to re-apply configuration when reloads happen.
* Start logging in memory, and only dumping to disk every 30 seconds or such with a timing thread. (2/20/2023)
    + Will likely need to use extensionPoints to trigger writes on the timer.
    + Will definitely need to use extensionPoints to catch when NVDA is terminating, and write buffer.
    + Consider making write to disk interval configurable, for SSD users.
* Make sure it doesn't save to config profiles. [Done, but re-do!]
