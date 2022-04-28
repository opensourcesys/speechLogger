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
import gui
from gui.settingsDialogs import PANEL_DESCRIPTION_WIDTH
from logHandler import log

addonHandler.initTranslation()

#: speechLogger Add-on config database
config.conf.spec["speechLogger"] = {
	"local": "",
	"remote": ""
}

# Some past iteration of this was probably based on something by Joseph Lee.
class SpeechLoggerSettings(gui.settingsDialogs.SettingsPanel):
	"""NVDA configuration panel based configurator  for speechLogger."""

	# Translators: This is the label for the Speech Logger settings category in NVDA Settings dialog.
	title = _("Speech Logger")
	# Translators: the introductory text for the settings dialog
	panelDescription = _(
		"Choose the log directory and filenames for the speech logs. "
		"System variables such as %temp% are permitted.\n"
		"You may also choose whether the logs grow continuously, or are rotated (renamed with \"-old\" "
		"before the extension) when NVDA starts.\nFinally, you can alter the string used to separate multiple"
		" utterances from the same speech sequence."
	)

	def makeSettings(self, settingsSizer):
		"""Creates a settings panel."""
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

		# Translators: label of a text field to enter local speech log filename.
		localFNControl = fileGroupHelper.addLabeledControl(_("Local speech log filename: "), wx.TextCtrl)
		# Translators: label of a text field to enter remote speech log filename.
		remoteFNControl = fileGroupHelper.addLabeledControl(_("Remote speech log filename: "), wx.TextCtrl)

		# Translators: Text of a checkbox to specify whether logs are exchanged on NVDA start.
		rotateLogsText = _("&Rotate logs on NVDA startup")
		self.rotateLogsCB = helper.addItem(wx.CheckBox(self, label=rotateLogsText))
		self.rotateLogsCB.Value = False

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
		separatorOptions = (
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
		separatorDisplayChoices = [name for setting, name in separatorOptions]
		separatorChoiceControl = sepGroupHelper.addLabeledControl(
			separatorComboLabel, wx.Choice, choices=separatorDisplayChoices
		)
		separatorChoiceControl.SetSelection(0)
		"""for index, (setting, name) in enumerate(separatorOptions):
			if setting == config.conf["speechLogger"]["separatorChoice"]:
				separatorChoiceControl.SetSelection(index)
				break
		else:
			log.debugWarning("Could not set separator combobox to the config derived option.")"""

		customSeparatorControl = sepGroupHelper.addLabeledControl(
			# Translators: the label for a text field requesting an optional custom separator string
			_(r"Custom utterance separator (can use escapes like \t): "), wx.TextCtrl
		)

	def onSave(self):
		#config.conf["speechLogger"]["local"] = self.localCB.Value
		pass
