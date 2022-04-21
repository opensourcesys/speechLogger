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

"""An NVDA add-on which logs, in real time, spoken output to a file or files.
This includes any output generated using the NVDA remote add-on.
Lightly based on suggestions sent to the nvda-addons@groups.io mailing list by James Scholes (https://nvda-addons.groups.io/g/nvda-addons/message/18552).
This add-on has no UI, and must be configured by constants below.

You have to define your own toggle gestures for this add-on, under the NVDA Input Gestures Tools category.
Look for "Toggles logging of local speech" and "Toggles logging of remote speech".

Since the path(s) must be edited in the source, you have to reload plugins (NVDA+Ctrl+F3, or NVDA restart) in order to change them.
(N.B. reloading plugins doesn't work for this at the moment, reason unknown.)

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
import globalPlugins
import ui
import speech
from speech.types import SpeechSequence, Optional
from speech.priorities import Spri
from scriptHandler import script
from logHandler import log

addonHandler.initTranslation()
	

@unique
class Origin(Enum):
	"""Enum to tell our methods where a speech sequence came from."""
	LOCAL = auto()
	REMOTE = auto()


def logToFile(sequence: SpeechSequence, file: str):
	"""Helper function to append text of the given speech sequence to the given file."""
	deblog(f"In logToFile, logging to {file}")
	with open(file, "a+") as f:
		f.write("\n".join(
			speech for speech in sequence if isinstance(speech, str)
		) + "\n")

def deblog(message: str):
	"""Crude debug log appender. Disable by uncommenting the return statement."""
	#return  # Don't log anything; production code should use this.
	file = os.path.abspath(os.path.expandvars(r"%temp%\lukeslog.txt"))
	with open(file, "a+") as f:
		f.write(message + "\n")


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super().__init__()
		deblog("Initializing.")
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
			deblog("In wrapped speak.")
			self.captureSpeech(sequence, Origin.LOCAL)
			return old_speak(sequence, symbolLevel, priority)
		speech.speech.speak = new_speak

	def fileSetup(self):
		"""Makes sure the paths exist, and the files can be written."""
		deblog("In fileSetup.")
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
		deblog(f"fileSetup: doLogLocal: {self.doLogLocal}, doLogRemote: {self.doLogRemote},\nlocalLogFile: {self.localLogFile},\nremoteLogFile: {self.remoteLogFile}")

	def captureSpeech(self, sequence: SpeechSequence, origin: Origin):
		"""Receives incoming local or remote speech, and if we are capturing that kind, sends it to the appropriate file."""
		file = None
		if origin == Origin.LOCAL and self.capturingLocal:
			file = self.localLogFile
		elif origin == Origin.REMOTE and self.capturingRemote:
			file = self.remoteLogFile
		if file is not None:
			logToFile(sequence, file)
		deblog(f"In captureSpeech. Type is: {origin}, and file is: {file},\ncapturingLocal: {self.capturingLocal}, capturingRemote: {self.capturingRemote}.")

	def _captureRemoteSpeech(self, *args, **kwargs):
		"""Register this as a callback to the NVDA Remote add-on's speech system, to obtain what it speaks."""
		deblog("In _captureRemoteSpeech.")
		if 'sequence' in kwargs:
			self.captureSpeech(kwargs.get('sequence'), Origin.REMOTE)

	def _obtainRemote(self) -> bool:
		"""Gets us a reference to the NVDA Remote add-on, if available.
		Returns True if we got (or had) one, False otherwise.
		"""
		deblog("In _obtainRemote.")
		# If we already have it, we don't need to get it
		if self.remotePlugin is not None:
			deblog("_obtainRemote: already have it, returning true.")
			return True
		# Find out if NVDA Remote is running, and get a reference if so:
		try:
			for plugin in globalPluginHandler.runningPlugins:
				if isinstance(plugin, globalPlugins.remoteClient.GlobalPlugin):
					self.remotePlugin = plugin
					deblog("_obtainRemote: found it, returning True.")
					return True  # break
		except TypeError:  # NVDA Remote is not running
			deblog("_obtainRemote: couldn't find it, returning False.")
			return False

	def _setupRemoteCallback(self) -> bool:
		deblog("In _setupRemoteCallback.")
		# If we have a reference to the Remote plugin, register a handler for its speech:
		if self.remotePlugin is not None:
			deblog("_setupRemoteCallback: attempting to assign the callback.")
			try:
				self.remotePlugin.master_session.transport.callback_manager.register_callback('msg_speak', self._captureRemoteSpeech)
				startedRemoteLogging = True
				deblog("_setupRemoteCallback: success.")
			except:  # Couldn't do, probably disconnected
				startedRemoteLogging = False
				deblog("_setupRemoteCallback: failed.")
		else:
			startedRemoteLogging = False
			deblog("_setupRemoteCallback: didn't have a Remote plugin reference, couldn't try.")
		return startedRemoteLogging

	@script(
		category="Tools",
		# Translators: the description of an item in the input gestures tools category
		description=_("Toggles logging of local speech")
	)
	def script_toggleLocalSpeechLogging(self, gesture):
		"""Toggles whether we are actively logging local speech."""
		deblog(f"In local toggle script. CapturingLocal was {self.capturingLocal}.")
		if self.capturingLocal:  # Stop
			deblog("Local toggle script: stopping.")
			self.capturingLocal = False
			# Translators: message to tell the user that we are no longer logging.
			ui.message(_("Stopped logging local speech."))
		else:  ## Start
			deblog(f"Local toggle script: starting, DoLogLocal was {self.doLogLocal}, captureLocal was {self.captureLocal}.")
			# Must check whether we can or should log
			if self.doLogLocal:
				self.captureLocal = True
				# Translators: a message to tell the user that we are now logging.
				ui.message(_("Started logging local speech."))
			else:
				deblog(f"Local toggle script: failed to start, DoLogLocal was {self.doLogLocal}, captureLocal was {self.captureLocal}.")
				# Translators: a message to tell the user that we can't start this kind of logging
				ui.message(_("Unable to log local speech. Check NVDA log for more information."))

	@script(
		category="Tools",
		# Translators: the description of an item in the input gestures tools category
		description=_("Toggles logging of remote speech")
	)
	def script_toggleRemoteSpeechLogging(self, gesture):
		"""Toggles whether we are actively logging remote speech."""
		deblog(f"In remote toggle script. CapturingRemote was {self.capturingRemote}.")
		if self.capturingRemote:  # Stop
			self.capturingRemote = False
			# Translators: message to tell the user that we are no longer logging.
			ui.message(_("Stopped logging remote speech."))
		else:  ## Start
			deblog(f"Remote toggle script: starting, doLogRemote was {self.doLogRemote}, capturingRemote was {self.capturingRemote}.")
			# Must check whether we can or should log
			if self.doLogRemote:
				# If this is the first time we're trying to start capturing,
				# we need to initialize the NVDA Remote portion of our log.
				deblog("Remote toggle script: attempting to start, checking for remote.")
				if self.remotePlugin is None and self._obtainRemote():
					# We didn't have Remote before, but we do have it now. Configure the callback.
					deblog("Remote toggle script: setting up the callback.")
					if self._setupRemoteCallback():
						self.capturingRemote = True
						deblog("Remote toggle script: success.")
						# Translators: a message to tell the user that we are now logging.
						ui.message(_("Started logging remote speech."))
					else:
						deblog("Remote toggle script:  failed.")
						# Translators: a message to tell the user that we failed to start remote logging.
						ui.message(_("Could not log speech from the remote session, maybe you need to connect?"))
			else:
				deblog(f"Remote toggle script: can't do that kind of logging. CapturingRemote was {self.capturingRemote}, doLogRemote was {self.doLogRemote}.")
				# Translators: a message to tell the user that we can't start this kind of logging
				ui.message(_("Unable to log local speech. Check NVDA log for more information."))
