# NVDA Speech Logger add-on, V23.0
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

"""An NVDA add-on which logs, in real time, spoken output to a file or files.
This can include any output generated using the NVDA remote add-on.
Lightly based on suggestions sent to the nvda-addons@groups.io mailing list by James Scholes (https://nvda-addons.groups.io/g/nvda-addons/message/18552).

This add-on must be configured before use. Configure it in NVDA Preferences -> Settings -> Speech Logger.

You can change the logging toggle gestures for this add-on, under the NVDA Input Gestures Tools category.
Look for "Toggles logging of local speech" and "Toggles logging of remote speech".

The log files are opened and closed for each speech utterance, because the original mandate for this add-on
was to have real-time saving of output.
Be warned that means lots of disk activity.
"""

import os
from functools import wraps
from enum import Enum, unique, auto
from typing import Optional, Dict

import addonHandler
import globalPluginHandler
import globalPlugins
import globalVars
import ui
import gui
import config
import speech
from speech.types import SpeechSequence
from speech.priorities import Spri
from gui.message import messageBox
from scriptHandler import script
from logHandler import log
from globalCommands import SCRCAT_TOOLS

from .configUI import SpeechLoggerSettings, getConf
from .immutableKeyObj import ImmutableKeyObj

addonHandler.initTranslation()
	

@unique
class Origin(Enum):
	"""Enum to tell our methods where a speech sequence came from."""
	LOCAL = auto()
	REMOTE = auto()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super().__init__()
		# Runtime vars and their sane defaults:
		# Because our runtime flags and variables are many and confusing,
		# We try to prevent some errors by using Immutable Key Objects to hold them where posible.
		self.flags: ImmutableKeyObj = ImmutableKeyObj(
			# Do we intend to log local speech?
			logLocal=False,
			# Tracks whether we are actively logging local speech
			localActive=False,
			# Do we intend to log remote speech?
			logRemote=False,
			# Tracks whether we are actively logging remote speech
			remoteActive=False,
			# Has the NVDA Remote speech capturing callback been registered?
			callbackRegistered=False,
			# Should we rotate logs on startup?
			rotate=False
		)
		#: Filenames are obtained from NVDA configuration, and setup in applyUserConfig().
		self.files: ImmutableKeyObj = ImmutableKeyObj(local=None, remote=None)
		# We can't handle getting our callback into NVDA Remote during __init__,
		# because remoteClient doesn't show up in globalPlugins yet. We will do it in the script instead.
		#: Holds an initially empty reference to NVDA Remote
		self.remotePlugin: Optional[globalPlugins.remoteClient.GlobalPlugin] = None
		#: Holds a text string used to separate speech. Assignable through user config.
		self.utteranceSeparator: str = "  "
		# Establish the add-on's NVDA configuration panel and config options, unless in secure mode
		if not globalVars.appArgs.secure:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(SpeechLoggerSettings)
		# Read user config or defaults
		self.applyUserConfig()
		# If we are supposed to rotate logs, do that now.
		if self.flags.rotate:
			self.rotateLogs()
		# Wrap speech.speech.speak, so we can get its output first
		old_speak = speech.speech.speak
		@wraps(speech.speech.speak)
		def new_speak(  # noqa: C901
				sequence: SpeechSequence,
				symbolLevel: Optional[int] = None,
				priority: Spri = Spri.NORMAL
		):
			self.captureSpeech(sequence, Origin.LOCAL)
			return old_speak(sequence, symbolLevel, priority)
		speech.speech.speak = new_speak

	def terminate(self) -> None:
		super().terminate()
		# Remove the NVDA settings panel
		if not globalVars.appArgs.secure:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SpeechLoggerSettings)

	def applyUserConfigIfNeeded(self) -> None:
		"""If the user has changed any part of the configuration, reset our internals accordingly."""
		if SpeechLoggerSettings.hasConfigChanges:
			self.applyUserConfig()
			SpeechLoggerSettings.hasConfigChanges = False

	def applyUserConfig(self) -> None:
		"""Configures internal variables according to those set in NVDA config."""
		# Stage 1: directory
		# If the directory hasn't been set, we disable all speech logging.
		if getConf("folder") == "":
			log.info("No log directory set. Disabling.")
			self.flags.logLocal = False
			self.flags.logRemote = False
			return
		# We shouldn't be able to reach this point with a bad directory name, unless
		# the user has been hand-editing nvda.ini. However, since that's possible, we must check.
		logFileFolder = os.path.abspath(os.path.expandvars(getConf("folder")))
		if not os.path.exists(logFileFolder):
			# Notify the user
			log.error(f'The folder given for log files does not exist. Folder: ({getConf("folder")}).')
			# Disable all speech logging
			self.flags.logLocal = False
			self.flags.logRemote = False
			# Nothing else matters.
			return
		if not os.access(logFileFolder, os.W_OK | os.X_OK):
			# Notify the user
			log.error(f'The folder given for log files can not be written by this user. Folder: ({getConf("folder")}).')
			# Disable all speech logging
			self.flags.logLocal = False
			self.flags.logRemote = False
			# Nothing else matters.
			return
		# Stage 2: files
		# If either filename is empty, it means the user doesn't want logging for that type.
		if getConf("local") == "":
			self.flags.logLocal = False
			self.files.local = None
		else:
			self.flags.logLocal = True
			self.files.local = os.path.join(
				logFileFolder,
				os.path.basename(os.path.expandvars(getConf("local")))
			)
			# Test open. Code suspended--we test folder access above as of 23.1.
			"""
			try:
				open(self.files.local, "a+", encoding="utf-8").close()
			except Exception as e:
				log.error(f"Couldn't open local log file {self.files.local} for appending. {e}")
				self.files.local = None
				self.flags.logLocal = False
			"""
		if getConf("remote") == "":
			self.flags.logRemote = False
			self.files.remote = None
		else:
			self.flags.logRemote = True
			self.files.remote = os.path.join(
				logFileFolder,
				os.path.basename(os.path.expandvars(getConf("remote")))
			)
			# Test open. Code suspended--we test folder access above as of 23.1.
			"""
			try:
				open(self.files.remote, "a+", encoding="utf-8").close()
			except Exception as e:
				log.error(f"Couldn't open remote log file {self.files.remote} for appending. {e}")
				self.files.remote = None
				self.flags.logRemote = False
			"""
		# Stage 3: file rotation
		# This is handled by __init__() and rotateLogs(); we just update the flag.
		self.flags.rotate = getConf("rotate")
		# Stage 4: utterance separation
		# For this one we may need the configured custom separator. However, it seems that
		# some part of NVDA or Configobj, escapes escape chars such as \t. We must undo that.
		unescapedCustomSeparator: str = getConf("customSeparator").encode().decode("unicode_escape")
		separators: Dict[str, str] = {
			"2spc": "  ",
			"nl": "\n",
			"comma": ", ",
			"__": "__",
			"custom": unescapedCustomSeparator
		}
		# In case the user has gone munging the config file, we must catch key errors.
		try:
			self.utteranceSeparator: str = separators[getConf("separator")]
		except KeyError:
			log.error(
				f'Value "{getConf("separator")}", found in NVDA config, is '
				'not a known separator. Using default of two spaces.'
			)
			self.utteranceSeparator: str = separators["2spc"]  # Use default

	def captureSpeech(self, sequence: SpeechSequence, origin: Origin) -> None:
		"""Receives incoming local or remote speech, and if we are capturing that kind, sends it to the appropriate file."""
		self.applyUserConfigIfNeeded()
		file: Optional[str] = None
		if origin == Origin.LOCAL and self.flags.localActive:
			file = self.files.local
		elif origin == Origin.REMOTE and self.flags.remoteActive:
			file = self.files.remote
		if file is not None:
			try:
				self.logToFile(sequence, file)
			except IOError:  # Could not write to the file for some reason; already logged by logToFile
				self.emergencyStop(showMessage=True, origin=origin)

	def emergencyStop(self, *, origin: Origin, showMessage: bool = False) -> None:
		"""Stops capturing a particular type of speech because of an error.
		@param showMessage: If True, alerts the user with a dialog.
		@param origin: The type of speech to stop logging.
		"""
		if origin is Origin.LOCAL:
			# Translators: The word "local", as in "local speech".
			translatedType = _("local")
		else:
			# Translators: The word "remote", as in "remote speech".
			translatedType = _("remote")
		# Translators: A message shown to the user when speech logging stopped unexpectedly.
		msg = _(
			"Logging of {type} speech has stopped unexpectedly.\n"
			"This is usually because Speech Logger could not write to its output file.\n"
			"More information may be found in the NVDA log.\n"
			"No further attempts will be made to log {type} speech during this NVDA session."
		).format(type=translatedType)
		# First, stop logging
		if origin is Origin.LOCAL:
			self.flags.logLocal = False
		else:
			self.flags.logRemote = False
		log.info(f"Terminated {origin.name} speech logging because of error.")
		if message:
			messageBox(
				msg,
				# Translators: A title indicating an error with the Speech Logger add-on
				_("Speech Logger Error")
			)

	def _captureRemoteSpeech(self, *args, **kwargs) -> None:
		"""Register this as a callback to the NVDA Remote add-on's speech system, to obtain what it speaks."""
		if 'sequence' in kwargs:
			self.captureSpeech(kwargs.get('sequence'), Origin.REMOTE)

	def _obtainRemote(self) -> bool:
		"""Gets us a reference to the NVDA Remote add-on, if available.
		Returns True if we got (or had) one, False otherwise.
		"""
		# If we already have it, we don't need to get it
		if self.remotePlugin is not None:
			return True
		# Find out if NVDA Remote is running, and get a reference if so:
		try:
			for plugin in globalPluginHandler.runningPlugins:
				if isinstance(plugin, globalPlugins.remoteClient.GlobalPlugin):
					self.remotePlugin = plugin
					return True  # break
		except AttributeError:  # NVDA Remote is not running
			return False

	def _registerCallback(self) -> bool:
		"""Adds our callback to NVDA Remote, if possible."""
		# If we have a reference to the Remote plugin, register a handler for its speech:
		if self.remotePlugin is not None:
			# If we already registered a callback, we're done early.
			# FixMe: should deregister the callback on session shutdown.
			if self.flags.callbackRegistered:
					return True
			try:
				self.remotePlugin.master_session.transport.callback_manager.register_callback('msg_speak', self._captureRemoteSpeech)
				self.flags.callbackRegistered = True
				startedRemoteLogging = True
			except:  # Couldn't do, probably disconnected
				startedRemoteLogging = False
		else:
			startedRemoteLogging = False
		return startedRemoteLogging

	@script(
		category=SCRCAT_TOOLS,
		# Translators: the description of an item in the input gestures tools category
		description=_("Toggles logging of local speech"),
		gesture="kb:NVDA+Alt+L"
	)
	def script_toggleLocalSpeechLogging(self, gesture):
		"""Toggles whether we are actively logging local speech."""
		if self.flags.localActive:  # Currently logging, stop
			self.flags.localActive = False
			# Translators: message to tell the user that we are no longer logging.
			ui.message(_("Stopped logging local speech."))
		else:  # Currently not logging, start
			# Must check whether we can or should log
			if self.flags.logLocal:
				self.flags.localActive = True
				# Translators: a message to tell the user that we are now logging.
				ui.message(_("Started logging local speech."))
			else:
				# Translators: a message to tell the user that we can't start this kind of logging
				ui.message(_("Local speech logging has been disabled by an error or your NVDA configuration."))

	@script(
		category=SCRCAT_TOOLS,
		# Translators: the description of an item in the input gestures tools category
		description=_("Toggles logging of remote speech"),
		gesture="kb:NVDA+Shift+Alt+L"
	)
	def script_toggleRemoteSpeechLogging(self, gesture):
		"""Toggles whether we are actively logging remote speech."""
		if self.flags.remoteActive:  # We were logging, stop
			self.flags.remoteActive = False
			# Translators: message to tell the user that we are no longer logging.
			ui.message(_("Stopped logging remote speech."))
		else:  # We weren't logging, start
			# Must check whether we can or should log
			if self.flags.logRemote:
				# If this is the first time we're trying to start capturing,
				# we need to initialize our NVDA Remote interface.
				if self._obtainRemote():
					# We have obtained (or already had) a reference to NVDA Remote. Configure the callback.
					if self._registerCallback():
						self.flags.remoteActive = True
						# Translators: a message to tell the user that we are now logging.
						ui.message(_("Started logging remote speech."))
					else:
						# Translators: a message to tell the user that we can not start logging because remote may not be connected..
						ui.message(_("Could not log remote speech, probably not connected."))
				else:  # self._obtainRemote() returned False
					# Translators: a message telling the user that the Remote add-on is unavailable.
					ui.message(_("Failed! Could not find the NVDA Remote add-on."))
			else:
				# Translators: a message to tell the user that we can't start this kind of logging
				ui.message(_("Remote speech logging has been disabled by an error or your NVDA configuration."))

	def logToFile(self, sequence: SpeechSequence, file: str) -> None:
		"""Append text of the given speech sequence to the given file."""
		try:
			with open(file, "a+", encoding="utf-8") as f:
				f.write(self.utteranceSeparator.join(
					toSpeak for toSpeak in sequence if isinstance(toSpeak, str)
				) + "\n")
		except IOError:
			log.error(f'Could not write to file: "{file}".', exc_info=True)
			raise

	def rotateLogs(self) -> None:
		"""Not implemented."""
		# FixMe: coming in a future version
		pass
