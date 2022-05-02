# NVDA Speech Logger add-on: configuration and GUI module
#
#    Copyright (C) 2022 Luke Davis <XLTechie@newanswertech.com>, James Scholes
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by    the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import wx

import addonHandler
import config
import ui
import globalVars
import gui
from gui.settingsDialogs import PANEL_DESCRIPTION_WIDTH
from logHandler import log

addonHandler.initTranslation()

#: speechLogger Add-on config database
config.conf.spec["speechLogger"] = {
	"folder": "string(default='')",
	"local": "string(default='NVDA-speech.log')",
	"remote": "string(default='NVDA-speech-remote.log')",
	"rotate": "boolean(default=False)",
	"separator": "string(default='2spc')",
	"customSeparator": "string(default='')"
}

def getConf(item: str):
	"""Accessor to return NVDA config items in a safe way.
	Because of the profiles avoidance hack used here (borrowed from Update Channel Selector add-on),
	it is possible for accesses of the config dictionary to fail, when the add-on is first installed,
	or has yet to be configured. This method protects each access attempt, by providing an alternate
	mechanism for returning the config item, that makes certain to get the version
	initialized by config.conf.spec.
	"""
	try:  # First, try to get the Normal Configuration version from profile zero
		return config.conf.profiles[0]['speechLogger'][item]
	except KeyError:  # Second, try to get it from the main config
		try:
			return config.conf['speechLogger'][item]
		except KeyError:  # Something strange is happening, maybe a coding error
			raise

def setConf(key: str, value):
	"""Complement of getConf. Sets NVDA config items in a safe way.
	Because of the profiles avoidance hack used here (borrowed from Update Channel Selector add-on),
	it is possible for setting elements of the config dictionary to fail, when the add-on is first installed,
	or has yet to be configured. This method protects each set attempt, by providing an alternate
	mechanism for addressing the config item, that makes certain to use the version Configobj recognizes.
	Returns value on success, like a normal assignment would.
	"""
	try:  # First, try to set the Normal Configuration version in profile zero
		config.conf.profiles[0]['speechLogger'][key] = value
	except KeyError:  # Second, try to set it using the main config
		try:
			config.conf['speechLogger'][key] = value
		except KeyError:  # Something strange is happening, maybe a coding error
			raise
	return value


class SpeechLoggerSettings(gui.settingsDialogs.SettingsPanel):
	"""NVDA configuration panel based configurator  for speechLogger."""

	#: Class variable to track whether the configuration has been changed in the panel, thus causing the
	#: add-on to refresh its idea of the configuration.
	hasConfigChanges = True
	# Translators: This is the label for the Speech Logger settings category in NVDA Settings dialog.
	title = _("Speech Logger")
	# Translators: the introductory text for the settings dialog
	panelDescription = _(
		"Choose the log directory and filenames for the speech logs. "
		"System variables such as %temp% are permitted.\n"
		"You can also alter the string used to separate multiple"
		" utterances from the same speech sequence."
	)

# Suspended description, awaiting the return of the rotation feature.
#	panelDescription = _(
#		"Choose the log directory and filenames for the speech logs. "
#		"System variables such as %temp% are permitted.\n"
#		"You may also choose whether the logs grow continuously, or are rotated (renamed with \"-old\" "
#		"before the extension) when NVDA starts.\nFinally, you can alter the string used to separate multiple"
#		" utterances from the same speech sequence."
#	)

	availableSeparators = (
		# Translators: a separator option in the separators combobox
		("2spc", _("Two spaces (NVDA log style)")),
		# Translators: a separator option in the separators combobox
		("nl", _("Newline")),
		# Translators: a separator option in the separators combobox
		("comma", _("A comma and space")),
		# Translators: a separator option in the separators combobox
		("__", _("Two underscores")),
		# Translators: a separator option in the separators combobox
		("custom", _("Custom"))
	)

	def makeSettings(self, settingsSizer):
		"""Creates a settings panel."""
		# Disable if in secure mode
		if globalVars.appArgs.secure:
			return

		helper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		introItem = helper.addItem(wx.StaticText(self, label=self.panelDescription))
		introItem.Wrap(self.scaleSize(PANEL_DESCRIPTION_WIDTH))

		# Grouping for path info
		groupSizer = wx.StaticBoxSizer(
			wx.VERTICAL, self,
			# Translators: label of the log files location grouping.
			label=_("Log &Directory: ")
		)
		fileGroupHelper = helper.addItem(gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer))
		fileGroupBox = groupSizer.GetStaticBox()

		# Translators: The label of a button to browse for a directory.
		browseText = _("Browse...")
		# Translators: The title of the dialog presented when browsing for the log directory.
		dirChooserTitle = _("Select log  directory")
		dirChooserHelper = gui.guiHelper.PathSelectionHelper(fileGroupBox, browseText, dirChooserTitle)
		directoryEntryControl = fileGroupHelper.addItem(dirChooserHelper)
		self.logDirectoryEdit = directoryEntryControl.pathControl
		self.logDirectoryEdit.SetValue(getConf("folder"))

		self.localFNControl = fileGroupHelper.addLabeledControl(
			# Translators: label of a text field to enter local speech log filename.
			_("Local speech log filename: "), wx.TextCtrl
		)
		self.localFNControl.SetValue(getConf("local"))
		self.remoteFNControl = fileGroupHelper.addLabeledControl(
			# Translators: label of a text field to enter remote speech log filename.
			_("Remote speech log filename: "), wx.TextCtrl
		)
		self.remoteFNControl.SetValue(getConf("remote"))

		# FixMe: log rotation is coming in the next version.
		# Translators: Text of a checkbox to specify whether logs are exchanged on NVDA start.
		#rotateLogsText = _("&Rotate logs on NVDA startup")
		#self.rotateLogsCB = helper.addItem(wx.CheckBox(self, label=rotateLogsText))
		#self.rotateLogsCB.SetValue(getConf("rotate"))

		# Grouping for separator options
		sepGroupSizer = wx.StaticBoxSizer(
			wx.VERTICAL, self,
			# Translators: label of the separator options grouping.
			label=_("&Separator Options")
		)
		sepGroupHelper = helper.addItem(gui.guiHelper.BoxSizerHelper(self, sizer=sepGroupSizer))
		sepGroupBox = sepGroupSizer.GetStaticBox()

		# Translators: this is the label for a combobox providing possible separator values
		separatorComboLabel = _("Utterance separator")
		separatorDisplayChoices = [name for setting, name in self.availableSeparators]
		self.separatorChoiceControl = sepGroupHelper.addLabeledControl(
			separatorComboLabel, wx.Choice, choices=separatorDisplayChoices
		)
		# Iterate the combobox choices, and pick the one listed in config
		for index, (setting, name) in enumerate(self.availableSeparators):
			if setting == getConf("separator"):
				self.separatorChoiceControl.SetSelection(index)
				break
		else:  # Unrecognized choice saved in configuration
			log.debugWarning(
				"Could not set separator combobox to the config derived option of"
				f' "{getConf("separator")}". Using default.'
			)
			self.separatorChoiceControl.SetSelection(0)  # Use default

		self.customSeparatorControl = sepGroupHelper.addLabeledControl(
			# Translators: the label for a text field requesting an optional custom separator string
			_(r"Custom utterance separator (can use escapes like \t): "), wx.TextCtrl
		)
		self.customSeparatorControl.SetValue(getConf("customSeparator"))

	def onSave(self):
		"""Save the settings to the Normal Configuration."""
		setConf("folder", self.logDirectoryEdit.Value)
		setConf("local", self.localFNControl.Value)
		setConf("remote", self.remoteFNControl.Value)
		# FixMe: log rotation is coming soon.
		#setConf("rotate", self.rotateLogsCB.Value)
		# Get the text of the selected separator
		sepText = self.availableSeparators[self.separatorChoiceControl.Selection][0]
		setConf("separator", sepText)
		setConf("customSeparator", self.customSeparatorControl.Value)
		# Lastly, restore the profile name, if it was munged by onPanelActivated().
		if self.changedProfileName:
			config.conf.profiles[-1].name = self.originalProfileName
			self.changedProfileName = False

	def postSave(self):
		"""After saving settings, set a flag to cause a config re-read by the add-on."""
		SpeechLoggerSettings.hasConfigChanges = True

	def onPanelActivated(self):
		"""When the panel activates, lie to it about what config we're using.
		This is necessary, because otherwise the panel's title may tell the user that
		a profile is being edited, when in fact we only edit the Normal Configuration.
		Improvement is needed in NVDA core to remove the necessity for hackishness such as this.
		"""
		# Basic concept developed by Jose-Manuel Delecado.
		if config.conf.profiles[-1].name is not None:
			self.originalProfileName = config.conf.profiles[-1].name
			config.conf.profiles[-1].name = None
			self.changedProfileName = True
		else:
			self.changedProfileName = False
		super().onPanelActivated()

	def onPanelDeactivated(self):
		"""Clean up any lies we might have told in onPanelActivated()."""
		# Basic concept developed by Jose-Manuel Delecado.
		if self.changedProfileName:
			config.conf.profiles[-1].name = self.originalProfileName
			self.changedProfileName = False
		super().onPanelDeactivated()

	def onDiscard(self):
		"""Restore the profile name if necessary (munged by onPanelActivated())."""
		# Basic concept developed by Jose-Manuel Delecado.
		if self.changedProfileName:
			config.conf.profiles[-1].name = self.originalProfileName
			self.changedProfileName = False
		super().onDiscard()
