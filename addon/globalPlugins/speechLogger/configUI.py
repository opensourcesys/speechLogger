# NVDA Speech Logger add-on: configuration and GUI module
#
#    Copyright (C) 2022-2023 Luke Davis <XLTechie@newanswertech.com>, James Scholes
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by    the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import wx
from typing import Any

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

def getConf(item: str) -> str:
	"""Accessor to return NVDA config items in a safe way."""
	return config.conf['speechLogger'][item]

def setConf(key: str, value: Any) -> Any:
	"""Complement of getConf. Sets NVDA config items in a safe way."""
	config.conf['speechLogger'][key] = value
	return value


class SpeechLoggerSettings(gui.settingsDialogs.SettingsPanel):
	"""NVDA configuration panel based configurator  for speechLogger."""

	#: Class variable to track whether the configuration has been changed in the panel, thus causing the
	#: add-on to refresh its idea of the configuration.
	hasConfigChanges: bool = True
	# Translators: This is the label for the Speech Logger settings category in NVDA Settings dialog.
	title: str = _("Speech Logger")
	# Translators: the primary introductory text for the settings dialog
	panelDescription_normalProfile: str = _(
		"Choose the log directory and filenames for the speech logs. "
		"System variables such as %temp% are permitted.\n"
		"You can also alter the string used to separate multiple"
		" utterances from the same speech sequence."
	)
	# Translators: the alternative introductory text for the settings dialog
	panelDescription_otherProfile: str = _(
		"The Speech Logger add-on can only be configured from the Normal Configuration profile.\n"
		"Please close this dialog, set your config profile to normal, and try again."
	)

# Suspended description, awaiting the return of the rotation feature.
#	panelDescription: str = _(
#		"Choose the log directory and filenames for the speech logs. "
#		"System variables such as %temp% are permitted.\n"
#		"You may also choose whether the logs grow continuously, or are rotated (renamed with \"-old\" "
#		"before the extension) when NVDA starts.\nFinally, you can alter the string used to separate multiple"
#		" utterances from the same speech sequence."
#	)

	availableSeparators: tuple = (
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

	def makeSettings(self, settingsSizer) -> None:
		"""Creates a settings panel.
		If an NVDA configuration profile other than "normal" is running, a panel with
		no options and a notification to the user is created.
		"""
		# Disable if in secure mode.
		# Can't use blockAction.when, because of compatibility with older versions.
		if globalVars.appArgs.secure:
			return

		if config.conf.profiles[-1].name is None and len(config.conf.profiles) == 1:
			SpeechLoggerSettings.panelDescription: str = self.panelDescription_normalProfile
		else:
			SpeechLoggerSettings.panelDescription: str = self.panelDescription_otherProfile

		helper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		introItem = helper.addItem(wx.StaticText(self, label=self.panelDescription))
		introItem.Wrap(self.scaleSize(PANEL_DESCRIPTION_WIDTH))

		if config.conf.profiles[-1].name is not None or len(config.conf.profiles) != 1:
			return

		# Grouping for path info
		groupSizer = wx.StaticBoxSizer(
			wx.VERTICAL, self,
			# Translators: label of the log files location grouping.
			label=_("Log &Directory: ")
		)
		fileGroupHelper = helper.addItem(gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer))
		fileGroupBox = groupSizer.GetStaticBox()

		# Translators: The label of a button to browse for a directory.
		browseText: str = _("Browse...")
		# Translators: The title of the dialog presented when browsing for the log directory.
		dirChooserTitle: str = _("Select log  directory")
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

		# FixMe: log rotation is coming in a future version.
		# Trans. Text of a checkbox to specify whether logs are exchanged on NVDA start.
		#rotateLogsText: str = _("&Rotate logs on NVDA startup")
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
		separatorComboLabel: str = _("Utterance separator")
		separatorDisplayChoices: list = [name for setting, name in self.availableSeparators]
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
		if config.conf.profiles[-1].name is None and len(config.conf.profiles) == 1:
			setConf("folder", self.logDirectoryEdit.Value)
			setConf("local", self.localFNControl.Value)
			setConf("remote", self.remoteFNControl.Value)
			# FixMe: log rotation is coming soon.
			#setConf("rotate", self.rotateLogsCB.Value)
			# Get the text of the selected separator
			sepText: str = self.availableSeparators[self.separatorChoiceControl.Selection][0]
			setConf("separator", sepText)
			setConf("customSeparator", self.customSeparatorControl.Value)

	def postSave(self):
		"""After saving settings, set a flag to cause a config re-read by the add-on."""
		if config.conf.profiles[-1].name is None and len(config.conf.profiles) == 1:
			SpeechLoggerSettings.hasConfigChanges = True
