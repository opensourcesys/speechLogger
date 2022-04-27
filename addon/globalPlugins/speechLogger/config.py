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

	def makeSettings(self, settingsSizer):
		"""Creates a settings panel."""
		helper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		# Translators: the introductory text for the settings dialog
		introText = _(
			"Choose the log directory and filenames for the speech logs.\n"
			"System variables such as %temp% are permitted.\n"
			"Also choose whether the logs are rotated (renamed with \"old\" prepended)"
			" when NVDA is restarted."
		)
		helper.addItem(wx.StaticText(self, label=introText))
		groupSizer = wx.StaticBoxSizer(
			wx.VERTICAL, self,
			# Translators: label of the log files location grouping.
			label=_("Log Directory and &Files")
		)
		groupHelper = helper.addItem(gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer))
		groupBox = groupSizer.GetStaticBox()
		# Translators: The label of a button to browse for a directory.
		browseText = _("Browse...")
		# Translators: The title of the dialog presented when browsing for the log directory.
		dirChooserTitle = _("Select log  directory")
		dirChooserHelper = gui.guiHelper.PathSelectionHelper(groupBox, browseText, dirChooserTitle)
		directoryEntryControl = groupHelper.addItem(dirChooserHelper)
		self.logDirectoryEdit = directoryEntryControl.pathControl
		# Translators: Text of a checkbox to specify whether logs are exchanged on NVDA start.
		rotateLogsText = _("&Rotate logs on NVDA startup")
		self.rotateLogsCB = helper.addItem(wx.CheckBox(self, label=rotateLogsText))
		self.rotateLogsCB.Value = False

	def onSave(self):
		#config.conf["speechLogger"]["local"] = self.localCB.Value
		pass
