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
	with open(file, "a+", encoding="utf-8") as f:
		f.write("\n".join(
			toSpeak for toSpeak in sequence if isinstance(toSpeak, str)
		) + "\n")

def deblog(message: str):
	"""Crude debug log appender. Disable by uncommenting the return statement."""
	#return  # Don't log anything; production code should use this.
	file = os.path.abspath(os.path.expandvars(r"%temp%\lukeslog.txt"))
	with open(file, "a+", encoding="utf-8") as f:
		f.write(message + "\n")


class ImmutableKeyObj:
	"""Helper type which you initialize with kwargs that become its members, after which no new members can be added.
	Think of it as an implementation of __slots__, that works at the instance level.
	"""
	def __setattr__(self, key, val):
		"""If object already has key as a member, its value is set to val. Otherwise KeyError is raised."""
		if not hasattr(self, key):
			raise KeyError(f'Can not set: {self} has no member "{key}".')
		else:
			object.__setattr__(self, key, val)

	def __init__(self, *args, **kwargs):
		"""Sets its kwargs with their values as the instance members, and gently prevents other members.
		Example:
		options = ImmutableKeyObj(recursive=True, backupExt=".bac")
		options.recursive  ## True
		options.backupExt = ".bk"  # Success
		options.file = "testing.txt"  # Fail, KeyError is raised
		"""
		self.__dict__ = {k: v for k, v in kwargs.items()}

	def __repr__(self):
		"""Returns the members of the instance as a formatted string."""
		itemSep = ", "  # A comma and a space between items
		kvSep = ": "  # A colon and a space between each key and value
		return itemSep.join(kvSep.join((k, str(v))) for (k, v) in self.__dict__.items())


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		global LOCAL_LOG, REMOTE_LOG
		super().__init__()
		deblog("Initializing.")
		# Runtime vars and their sane defaults:
		# Because our runtime flags and variables are many and confusing,
		# We try to prevent some errors by using Immutable Key Objects to hold them.
		self.flags = ImmutableKeyObj(
			# Do we intend to log local speech?
			logLocal=False,
			# Tracks whether we are actively logging local speech
			localActive=False,
			# Do we intend to log remote speech?
			logRemote=False,
			# Tracks whether we are actively logging remote speech
			remoteActive=False
		)
		self.files = ImmutableKeyObj(local=LOCAL_LOG, remote=REMOTE_LOG)
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
			#deblog("In wrapped speak.")
			self.captureSpeech(sequence, Origin.LOCAL)
			return old_speak(sequence, symbolLevel, priority)
		speech.speech.speak = new_speak

	def fileSetup(self):
		"""Makes sure the paths exist, and the files can be written."""
		deblog("In fileSetup.")
		# If either filename is set to None, it means the user doesn't want logging for that type
		if self.files.local is None:
			self.flags.logLocal = False
		else:
			self.flags.logLocal = True
			# Regularize filename
			self.files.local = os.path.abspath(os.path.expandvars(self.files.local))
			# Test open
			try:
				with open(self.files.local, "a+", encoding="utf-8") as f:
					pass
			except Exception as e:
				log.error(f"Couldn't open local log file {self.files.local} for appending. {e}")
				self.files.local = None
				self.flags.logLocal = False
		if self.files.remote is None:
			self.flags.logRemote = False
		else:
			self.flags.logRemote = True
			# Regularize filename
			self.files.remote = os.path.abspath(os.path.expandvars(self.files.remote))
			# Test open
			try:
				with open(self.files.remote, "a+", encoding="utf-8") as test:
					pass
			except Exception as e:
				log.error(f"Couldn't open remote log file {self.files.remote} for appending. {e}")
				self.files.remote = None
				self.flags.logRemote = False
		deblog(f"fileSetup: {self.flags}\n{self.files}")

	def captureSpeech(self, sequence: SpeechSequence, origin: Origin):
		"""Receives incoming local or remote speech, and if we are capturing that kind, sends it to the appropriate file."""
		file = None
		if origin == Origin.LOCAL and self.flags.localActive:
			file = self.files.local
		elif origin == Origin.REMOTE and self.flags.remoteActive:
			file = self.files.remote
		if file is not None:
			logToFile(sequence, file)
		#deblog(f"In captureSpeech. Type is: {origin}, and file is: {file},\nFlags: {self.flags}.")

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
		except AttributeError:  # NVDA Remote is not running
			deblog("_obtainRemote: couldn't find it, returning False.")
			return False

	def _setupRemoteCallback(self) -> bool:
		"""Adds our callback to NVDA Remote, if possible."""
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
		deblog(f"In local toggle script. Capture was {self.flags.localActive}.")
		if self.flags.localActive:  # Currently logging, stop
			deblog("Local toggle script: stopping.")
			self.flags.localActive = False
			# Translators: message to tell the user that we are no longer logging.
			ui.message(_("Stopped logging local speech."))
		else:  # Currently not logging, start
			deblog(f"Local toggle script: starting, Flags: {self.flags}.")
			# Must check whether we can or should log
			if self.flags.logLocal:
				self.flags.localActive = True
				# Translators: a message to tell the user that we are now logging.
				ui.message(_("Started logging local speech."))
			else:
				deblog(f"Local toggle script: failed to start, Flags: {self.flags}.")
				# Translators: a message to tell the user that we can't start this kind of logging
				ui.message(_("Unable to log local speech. Check NVDA log for more information."))

	@script(
		category="Tools",
		# Translators: the description of an item in the input gestures tools category
		description=_("Toggles logging of remote speech")
	)
	def script_toggleRemoteSpeechLogging(self, gesture):
		"""Toggles whether we are actively logging remote speech."""
		deblog(f"In remote toggle script. Flags: {self.flags}.")
		if self.flags.remoteActive:  # We were logging, stop
			self.flags.remoteActive = False
			# Translators: message to tell the user that we are no longer logging.
			ui.message(_("Stopped logging remote speech."))
		else:  # We weren't logging, start
			deblog(f"Remote toggle script: starting, flags: {self.flags}.")
			# Must check whether we can or should log
			if self.flags.logRemote:
				# If this is the first time we're trying to start capturing,
				# we need to initialize our NVDA Remote interface.
				deblog("Remote toggle script: attempting to start, checking for remote.")
				if self._obtainRemote():
					# We have obtained (or already had) a reference to NVDA Remote. Configure the callback.
					deblog("Remote toggle script: setting up the callback.")
					if self._setupRemoteCallback():
						self.flags.remoteActive = True
						deblog("Remote toggle script: success.")
						# Translators: a message to tell the user that we are now logging.
						ui.message(_("Started logging remote speech."))
					else:
						deblog("Remote toggle script:  failed to register the callback.")
						# Translators: a message to tell the user that we failed to start remote logging.
						ui.message(_("Could not log speech from the remote session. Maybe you need to connect?"))
				else:  # self._obtainRemote() returned False
					deblog("Remote toggle script: _obtainRemote() failed.")
					# Translators: a message telling the user that the Remote add-on is unavailable.
					ui.message(_("Failed! Could not find the NVDA Remote add-on."))
			else:
				deblog(f"Remote toggle script: can't do that kind of logging. Flags: {self.flags}\nFiles: {self.files}.")
				# Translators: a message to tell the user that we can't start this kind of logging
				ui.message(_("Unable to log local speech. Check NVDA log for more information."))
