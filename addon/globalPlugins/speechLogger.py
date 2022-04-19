# Speech Logger with Remote Support, V22.0
#
#    Copyright (C) 2022 Luke Davis <XLTechie@newanswertech.com>
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by    the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""An NVDA add-on which logs, in real time, spoken output to a file.
This includes any output generated using the NVDA remote add-on.
Based on suggestions sent to the nvda-addons@groups.io mailing list by James Scholes (https://nvda-addons.groups.io/g/nvda-addons/message/18552).
This add-on has no UI, and must be configured by constants below.

You must define your own start-stop gesture for this add-on before using it. It can be found in the Tools category of Input Gestures.

Since the path(s) must be edited in the source, you have to reload plugins (NVDA+Ctrl+F3, or NVDA restart) in order to change them.

The log files are opened and closed for each speech utterance, because the original mandate for this add-on
was to have real-time saving of output.
That means lots of disk activity, and probably not wonderful performance unless writing to a RAMDisk or an SSD.

Note also that these files are never truncated, and must be managed manually or they will grow very large.
"""

# CONFIGURATION
#: Speech generated locally is output to this file.
#: Set to None to disable local speech logging.
LOCAL_LOG = r"%temp%\nvda-speech.log"
#: Speech collected from the NVDA Remote add-on is saved to this file.
#: If you use exactly the same path and name as LOCAL_LOG, then both kinds of speech are logged to the same file.
#: Set to None to disable remote speech logging.
REMOTE_LOG = r"%temp%\nvda-speech-remote.log"
# END OF CONFIGURATION

import os
from functools import wraps
from enum import Enum, unique, auto, IntEnum

import addonHandler
import globalPluginHandler
import speech
import globalPlugins
import ui
from speech.types import SpeechSequence, Optional
from speech.priorities import Spri
from scriptHandler import script
from logHandler import log

addonHandler.initTranslation()
	

@unique
class Origin(Enum):
	LOCAL = auto()
	REMOTE = auto()


def logToFile(sequence: SpeechSequence, file: str):
	with open(file, "ab") as f:
		f.write("\n".join(
			speech for speech in sequence if isinstance(speech, str)
		) + "\n")


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super().__init__()
		# Sane defaults for runtime variables
		#: Tracks whether we are logging local speech, starts False
		self.capturingLocal = False
		#: Tracks whether we are logging remote speech, starts False
		self.capturingRemote = False
		#: Do we intend to log local speech?
		self.doLogLocal = False
		#: Do we intend to log remote speech?
		self.doLogRemote = False
		# We can't handle getting our callback into NVDA Remote during __init__,
		# because remoteClient doesn't show up in globalPlugins yet. We will do it in the script instead.
		#: Holds an initially empty reference to NVDA Remote
		self.remotePlugin = None
		self.fileSetup()
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

	def fileSetup(self):
		"""Makes sure the paths exist, and the files can be written."""
		global LOCAL_LOG, REMOTE_LOG
		# If either filename is set to None, it means the user doesn't want logging for that type
		if LOCAL_LOG is None:
			self.doLogLocal = False
			self.localLogFile = None
		else:
			self.doLogLocal = True
			self.localLogFile = os.path.abspath(os.path.expandvars(LOCAL_LOG))
			# Test open
			try:
				with open(self.localLogFile, "ab+") as f:
					pass
			except Exception as e:
				log.warn(f"Couldn't open local log file {self.localLogFile} for appending. {e}")
				self.localLogFile = None
				self.doLogLocal = False
		if REMOTE_LOG is None:
			self.doLogRemote = False
			self.remoteLogFile = None
		else:
			self.doLogREMOTE = True
			self.remoteLogFile = os.path.abspath(os.path.expandvars(REMOTE_LOG))
			# Test open
			try:
				with open(self.remoteLogFile, "ab+") as test:
					pass
			except Exception as e:
				log.warn(f"Couldn't open remote log file {self.remoteLogFile} for appending. {e}")
				self.remoteLogFile = None
				self.doLogRemote = False

	def captureSpeech(self, sequence: SpeechSequence, origin: Origin):
		if not self.capturingLocal or self.capturingRemote:
			return
		file = None
		if origin == Origin.LOCAL and self.doLogLocal:
			file = self.localLogFile
		elif origin == Origin.REMOTE and self.doLogRemote:
			file = self.remoteLogFile
		if file is not None:
			logToFile(sequence, file)
			
	def _captureRemoteSpeech(self, *args, **kwargs):
		"""Register this as a callback to the NVDA Remote add-on's speech system, to obtain what it speaks."""
		if 'sequence' in kwargs:
			self.captureSpeech(kwargs.get('sequence'), Origin.REMOTE)
		return

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
		except TypeError:  # NVDA Remote is not running
			return False

	def _setupRemoteCallback(self) -> bool:
		# If we have a reference to the Remote plugin, register a handler for its speech:
		if self.remotePlugin is not None:
			try:
				self.remotePlugin.master_session.transport.callback_manager.register_callback('msg_speak', self._captureRemoteSpeech)
				startedRemoteLogging = True
			except:  # Couldn't do, probably disconnected
				startedRemoteLogging = False
		else:
			startedRemoteLogging = False
		return startedRemoteLogging

	@script(
		category="Tools",
		# Translators: the description of an item in the input gestures tools category
		description=_("Toggles logging of local speech")
	)
	def script_toggleLocalSpeechLogging(self, gesture):
		"""Toggles whether we are actively logging local speech."""
		if self.capturingLocal:  # Stop
			self.capturingLocal = False
			# Translators: message to tell the user that we are no longer logging.
			ui.message(_("Stopped logging local speech."))
		else:  ## Start
			# Must check whether we can or should log
			if self.doLogLocal:
				self.captureLocal = True
				# Translators: a message to tell the user that we are now logging.
				ui.message(_("Started logging local speech."))
			else:
				# Translators: a message to tell the user that we can't start this kind of logging
				ui.message(_("Unable to log local speech. Check NVDA log for more information."))

	@script(
		category="Tools",
		# Translators: the description of an item in the input gestures tools category
		description=_("Toggles logging of remote speech")
	)
	def script_toggleRemoteSpeechLogging(self, gesture):
		"""Toggles whether we are actively logging remote speech."""
		if self.capturingRemote:  # Stop
			self.capturingRemote = False
			# Translators: message to tell the user that we are no longer logging.
			ui.message(_("Stopped logging remote speech."))
		else:  ## Start
			# Must check whether we can or should log
			if self.doLogLocal:
				# If this is the first time we're trying to start capturing,
				# we need to initialize the NVDA Remote portion of our log.
				if self.remotePlugin is None and self._obtainRemote():
					# We didn't have Remote before, but we do have it now. Configure the callback.
					if self._setupRemoteCallback():
						self.captureRemote = True
						# Translators: a message to tell the user that we are now logging.
						ui.message(_("Started logging remote speech."))
					else:
						# Translators: a message to tell the user that we failed to start remote logging.
						ui.message(_("Could not log speech from the remote session, maybe you need to connect?"))
			else:
				# Translators: a message to tell the user that we can't start this kind of logging
				ui.message(_("Unable to log local speech. Check NVDA log for more information."))
