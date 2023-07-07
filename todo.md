### Things to do:

#### Priority 1:

* [ ] Functionalize file creation, and carry the filenames in the plugin independently from the raw names given in configuration. This will allow strftime and other variables in the filenames. (Listed: 5/12/2023)
* [X] Add tab as a pre-configured separator option. (listed: 2/20/2023, completed: 5/15/2023)
* [X] Write dates to the files when logging starts and stops. (Listed: 2/20/2023, completed: 5/3/2023)
* [ ] Stop creating files before they need to be written to the first time. (listed: 2/20/2023)
* [ ] Add the possibility of strftime variables in file and directory names, per issue #4 (listed: 4/26/2023)
* [ ] Add optional timestamping on every logged item. (Listed: 5/12/2023)

#### Priority 2:

* [ ] Replace the Any types in configUI.setConf, with more likely typings. (listed: 2/18/2023)
* [ ] Make rotation work.
* [X] Disable the custom field, if custom isn't selected. (Listed: ~5/15/2022, Completed: 7/7/2023)
* Make timestamps configurable (Listed: 5/12/2023)
    + [X] Initially, a combobox to turn on/off (on default) the start/end timestamps. Use an int in configObj. (Completed: 5/15/2023)
    + [ ] Later, a combobox to choose between None, when starting or stopping, and every logged item.

#### Priority 3:

* [ ] Use the extensionpoint post_configReset to re-apply configuration when reloads happen.
* [ ] Use the extension point to find out when NVDA has finished initializing, and register the remote callback then. (Listed: 5/15/2023)
* [ ] Start logging in memory, and only dumping to disk every 30 seconds or such with a timing thread. (listed: 2/20/2023)
    + Will likely need to use extensionPoints to trigger writes on the timer.
    + Can probably use GlobalPlugin.terminate() to write the buffer for the last time.
    + [ ] Consider making write to disk interval configurable, for SSD users.
* [ ] Make sure it doesn't save to config profiles. [Done, but re-do!]
