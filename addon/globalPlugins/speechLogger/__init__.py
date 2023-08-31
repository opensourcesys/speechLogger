# NVDA Speech Logger add-on, V23.3
#
#    Copyright (C) 2022-2023 Luke Davis <XLTechie@newanswertech.com>
# Initially based on code ideas suggested by James Scholes.
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
import wx
from time import strftime
from typing import Optional, Dict
from functools import wraps
from enum import Enum, unique, auto, IntEnum

import addonHandler
import globalPluginHandler
import globalPlugins
import globalVars
import ui
import gui
import config
import speech
from speech.speechWithoutPauses import SpeechWithoutPauses
from speech.types import SpeechSequence
from speech.priorities import Spri
from scriptHandler import script
from logHandler import log
from globalCommands import SCRCAT_TOOLS, SCRCAT_CONFIG
from core import postNvdaStartup

from .configUI import SpeechLoggerSettings, getConf
from .immutableKeyObj import ImmutableKeyObj
from . import extensionPoint

try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.error(
		"Attempted to initialize translations in an inappropriate context. May be running from scratchpad."
	)

@unique
class Origin(Enum):
	"""Enum to tell our methods where a speech sequence came from."""
	LOCAL = auto()
	REMOTE = auto()


def resolveOrMakeDirectory(dir: str) -> str:
	"""Resolves or makes the directory given, which may include Windows variable and time parameters.
	@param dir: The directory, maybe including Windows %v% & strftime %X variables, to (make and) return.
	@returns str: The fully qualified path.
	@raises osError: If the directory needed to be created but couldn't be, maybe because a file existed there.
	"""
	# First, we process the dir through expandvars, to explode any Windows variables.
	# Since expandvars leaves alone anything it doesn't understand, we can then
		# process through strftime, to handle the date/time replacements.
	# The opposite order will not work. Lastly, we make it an absolute path.
	expandedDir = os.path.abspath(strftime(os.path.expandvars(dir)))
	# We try to create the directory(ies), and silently fail if it already exists
	os.makedirs(expandedDir, exist_ok=True)
	return expandedDir


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
			# Have we already logged any local speech during this log session?
			startedLocalLog=False,
			# Do we intend to log remote speech?
			logRemote=False,
			# Tracks whether we are actively logging remote speech
			remoteActive=False,
			# Have we already logged any remote speech during this log session?
			startedRemoteLog=False,
			# Has the NVDA Remote speech capturing callback been registered?
			callbackRegistered=False,
			# Should we rotate logs on startup?
			rotate=False,
			# Should we log the timestamp when we start/stop a log session?
			startStopTimestamps=True,
			# Should we log during Say All/Read To End?
			logSayAll=True,
			# Should we start logging when launched?
			logAtStartup=False,
			# Becomes True if we were initially set to log at startup
			loggedAtStartup=False
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
		# Register to our private extensionPoint to notify our config reloads
		extensionPoint._configChanged.register(self.applyUserConfig)
		# Read user config the first time
		self.applyUserConfig(False)
		# If we are supposed to rotate logs, do that now.
		if self.flags.rotate:
			self.rotateLogs()
		# If we are supposed to start logging at NVDA startup, register a handler for that
		if self.flags.logAtStartup:
			postNvdaStartup.register(self.startLocalLog)
			self.flags.loggedAtStartup = True
		# Wrap speech.speech.speak, so we can get its output first
		self._speak_orig = speech.speech.speak
		@wraps(speech.speech.speak)
		def new_speak(  # noqa: C901
				sequence: SpeechSequence,
				symbolLevel: Optional[int] = None,
				priority: Spri = Spri.NORMAL,
				*args,
				**kwargs
		):
			self.captureSpeech(sequence, Origin.LOCAL)
			return self._speak_orig(sequence, symbolLevel, priority, *args, **kwargs)
		speech.speech.speak = new_speak
		# Wrap speech.SpeechWithoutPauses.speechWithoutPauses.speakWithoutPauses, so we can get its output first
		SpeechWithoutPauses._speakWithoutPauses_orig = SpeechWithoutPauses.speakWithoutPauses
		SpeechWithoutPauses._speechLogger_object = self
		SpeechWithoutPauses._speechLogger_origin = Origin.LOCAL
		@wraps(SpeechWithoutPauses.speakWithoutPauses)
		def speechLogger_speakWithoutPauses(  # noqa: C901
				self,
				sequence: Optional[SpeechSequence],
				detectBreaks: bool = True,
				*args,
				**kwargs
		):
			if (
				SpeechWithoutPauses._speechLogger_object.flags.logSayAll
				and sequence is not None
			):
				self._speechLogger_object.captureSpeech(sequence, self._speechLogger_origin)
			return self._speakWithoutPauses_orig(sequence, detectBreaks, *args, **kwargs)
		SpeechWithoutPauses.speakWithoutPauses = speechLogger_speakWithoutPauses

	def terminate(self) -> None:
		# Stop all logging that may be in progress
		self.stopRemoteLog()
		self.stopLocalLog()
		# Remove the NVDA settings panel
		if not globalVars.appArgs.secure:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SpeechLoggerSettings)
		# Unwrap/un-patch methods that we patched.
		# Note that this may screw with add-ons that patched them after we did.
		speech.speech.speak = self._speak_orig
		SpeechWithoutPauses.speakWithoutPauses = SpeechWithoutPauses._speakWithoutPauses_orig
		# Unregister extensionPoints
		if self.flags.loggedAtStartup:
			postNvdaStartup.unregister(self.startLocalLog)
		extensionPoint._configChanged.unregister(self.applyUserConfig)
		super().terminate()

	def startLocalLog(self, automatic: bool = True) -> bool:
		# If we are already logging, log a warning and return
		if self.flags.localActive:
			log.warning("Attempted to start logging speech when already logging speech!")
			return True
		# Must check whether we can or should log
		if self.flags.logLocal:
			self.flags.localActive = True  # Start logging with next utterance
			if automatic:
				log.info("Began logging local speech at NVDA startup.")
			else:
				log.info("User initiated logging of local speech.")
			return True
		else:
			return False

	def stopLocalLog(self) -> bool:
		if self.flags.localActive:  # Currently logging, stop
			# Write a message to the log stating that we are no longer logging
			self.logToFile(self.files.local, None, self.dynamicLogStoppedText)
			self.flags.localActive = False
			self.flags.startedLocalLog = False
			log.info("Stopped logging local speech.")
			return True
		else:
			return False

	def stopRemoteLog(self) -> bool:
		if self.flags.remoteActive:  # We were logging, stop
			# Write a message to the log stating that we have stopped logging
			self.logToFile(self.files.remote, None, self.dynamicLogStoppedText)
			self.flags.remoteActive = False
			self.flags.startedRemoteLog = False
			log.info("Stopped logging remote speech.")
			return True
		else:
			return False

	def applyUserConfig(self, triggeredByExtensionPoint: bool = True) -> None:
		"""Configures internal variables according to those set in NVDA config.

		@param triggeredByExtensionPoint: True (default) if triggered because of a config reload extensionPoint
		"""
		if triggeredByExtensionPoint:
			log.debug("Applying user configuration triggered by extensionPoint.")
		else:
			log.debug("Applying user configuration triggered by internal process.")
		# Stage 1: directory
		# If the directory hasn't been set, we disable all logging.
		if getConf("folder") == "":
			log.info("No log directory set. Disabling.")
			self.flags.logLocal = False
			self.flags.logRemote = False
			return
		# We shouldn't be able to reach this point with a bad directory name, unless
		# the user has been hand-editing nvda.ini. However, since that's possible, we must check.
		if not os.path.exists(os.path.abspath(os.path.expandvars(getConf("folder")))):
			# Notify the user
			log.error(f'The folder given for log files does not exist ({getConf("folder")}).')
			# Disable all logging
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
				os.path.abspath(os.path.expandvars(getConf("folder"))),
				os.path.basename(os.path.expandvars(getConf("local")))
			)
			# Test open
			try:
				open(self.files.local, "a+", encoding="utf-8").close()
			except Exception as e:
				log.error(f"Couldn't open local log file {self.files.local} for appending. {e}")
				self.files.local = None
				self.flags.logLocal = False
		if getConf("remote") == "":
			self.flags.logRemote = False
			self.files.remote = None
		else:
			self.flags.logRemote = True
			self.files.remote = os.path.join(
				os.path.abspath(os.path.expandvars(getConf("folder"))),
				os.path.basename(os.path.expandvars(getConf("remote")))
			)
			# Test open
			try:
				open(self.files.remote, "a+", encoding="utf-8").close()
			except Exception as e:
				log.error(f"Couldn't open remote log file {self.files.remote} for appending. {e}")
				self.files.remote = None
				self.flags.logRemote = False
		# Stage 3: file rotation
		# This is handled by __init__() and rotateLogs(); we just update the flag.
		self.flags.rotate = getConf("rotate")
		# Stage 4: misc/other settings
		# Timestamps can be off, on, or per-sequence.
		# In the config, tsMode will be 0 for off, higher for the other two options.
		self.flags.startStopTimestamps = True if getConf("tsMode") > 0 else False
		self.flags.logSayAll = bool(getConf("logSayAll"))
		# In the config, possible logAtStartup values are:
		# 0 for never, 1 for always, 2 for only if logging was on when shutdown (not yet implemented).
		self.flags.logAtStartup = True if getConf("logAtStartup") == 1 else False
		# Stage 5: utterance separation
		# For this one we may need the configured custom separator. However, it seems that
		# some part of NVDA or Configobj, escapes escape chars such as \t. We must undo that.
		unescapedCustomSeparator: str = getConf("customSeparator").encode().decode("unicode_escape")
		separators: Dict[str, str] = {
			"2spc": "  ",
			"nl": "\n",
			"tab": "\t",
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

	def _createDynamicLogStateText(self, started: bool = True) -> str:
		"""Returns translated text that can be inserted in the log, indicating that a log session started/ended.
		If the proper flag is set, it will include the date and time.
		Intended to be called from properties.
		@param started: If True, returns a "log started" style message. If False, a "log ended" style message.
		"""
		# Translators: Text inserted in the log indicating logging has started.
		startText: str = _("Log started")
		# Translators: Text inserted in the log indicating logging has ended.
		stopText: str = _("Log ended")
		# Translators: Series of punctuations that appear around unspoken log started/stopped messages.
		edgeTag: str = _("###")
		# Translators: This word appears between log stopped/started messages, and the date and time it happened.
		timestampSep: str = _("on")
		# Translators: A string that separates a date from a time. Should include space(s).
		dateTimeSep: str = _(" at ")
		date: str = strftime("%x")
		time: str = strftime("%X")
		if self.flags.startStopTimestamps:
			return edgeTag + (f" {startText}" if started else f" {stopText}") \
			+ f" {timestampSep} {date}{dateTimeSep}{time} " + (edgeTag if started else f"{edgeTag}\n")
		else:
			return edgeTag + (f" {startText} {edgeTag}" if started else f" {stopText} {edgeTag}\n")

	@property
	def dynamicLogStartedText(self) -> str:
		"""Returns translated text that can be inserted in the log indicating that a new log session has started.
		If the proper flag is set, it will include the date and time.
		"""
		return self._createDynamicLogStateText()

	@property
	def dynamicLogStoppedText(self) -> str:
		"""Returns translated text that can be inserted in the log indicating that the current log session has ended.
		If the proper flag is set, it will include the date and time.
		"""
		return self._createDynamicLogStateText(False)

	def captureSpeech(self, sequence: SpeechSequence, origin: Origin) -> None:
		"""Receives incoming local or remote speech, and if we are capturing that kind, sends it to the appropriate file."""
		file: Optional[str] = None
		initialText: Optional[str] = None
		if origin == Origin.LOCAL and self.flags.localActive:
			file = self.files.local
			if not self.flags.startedLocalLog:
				initialText = self.dynamicLogStartedText
				self.flags.startedLocalLog = True
		elif origin == Origin.REMOTE and self.flags.remoteActive:
			file = self.files.remote
			if not self.flags.startedRemoteLog:
				initialText = self.dynamicLogStartedText
				self.flags.startedRemoteLog = True
		if file is not None:
			self.logToFile(file, sequence, initialText)

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
		if self.stopLocalLog():  # Stop the local log; returns True if logging was stopped
			# Translators: message to tell the user that we are no longer logging.
			ui.message(_("Stopped logging local speech."))
		else:  # Currently not logging, start
			if self.startLocalLog(False):
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
		if self.stopRemoteLog():  # Stops remote logging if we were; returns True if stopped
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

	@script(
		# Translators: Input help mode message for open Speech Logger settings command.
		description=_("Opens the Speech Logger add-on's settings"),
		category=SCRCAT_CONFIG
	)
	@gui.blockAction.when(gui.blockAction.Context.MODAL_DIALOG_OPEN)
	def script_activateSpeechLoggerSettingsDialog(self, gesture):
		wx.CallAfter(
			# Maintain compatibility with pre-2023.2 versions of gui
			getattr(gui.mainFrame, "popupSettingsDialog" if hasattr(gui.mainFrame, "popupSettingsDialog") else "_popupSettingsDialog"),
			gui.settingsDialogs.NVDASettingsDialog,
			SpeechLoggerSettings
		)

	def logToFile(self, file: str, sequence: Optional[SpeechSequence], initialText: Optional[str]) -> None:
		"""Append text of the given speech sequence to the given file.
		If an initialText is given, it appears on its own line before the logged text.
		"""
		with open(file, "a+", encoding="utf-8") as f:
			if initialText is not None:
				f.write(f"{initialText}\n")
			if sequence is not None:
				f.write(self.utteranceSeparator.join(
					toSpeak for toSpeak in sequence if isinstance(toSpeak, str)
				) + "\n")

	def rotateLogs(self) -> None:
		"""Not implemented."""
		# FixMe: coming in a future version
		pass
