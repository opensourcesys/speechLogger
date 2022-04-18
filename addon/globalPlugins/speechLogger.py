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

addonHandler.initTranslation()

@unique
class Origin(Enum):
	LOCAL = auto()
	REMOTE = auto()

#: Module level variable to track whether we should be logging, starts False
capturing = False

# We need to wrap speech.speech.speak() in order to capture speech from it.
speech.speech.speechLogger_old_speak = speech.speech.speak
@wraps(speech.speech.speak)
def new_speak(  # noqa: C901
		sequence: SpeechSequence,
		symbolLevel: Optional[int] = None,
		priority: Spri = Spri.NORMAL
):
	captureSpeech(sequence, Origin.LOCAL)
	return speech.speech.speechLogger_old_speak(sequence, symbolLevel, priority)

def captureSpeech(sequence: SpeechSequence, origin: Origin):
	if not capturing:
		return
	file = None
	if origin == Origin.LOCAL and LOCAL_LOG is not None:
		file = LOCAL_LOG
	if origin == Origin.REMOTE and REMOTE_LOG is not None:
		file = REMOTE_LOG
	if file is not None:
		logToFile(sequence, file)

def logToFile(sequence: SpeechSequence, file: str):
	with open(file, "ab") as f:
		f.write("\n".join(
			speech for speech in sequence if isinstance(speech, str)
		) + "\n")

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super().__init__()
		# Wrap speech.speech.speak, so we can get its output first
		speech.speech.speak = new_speak
		# We can't handle getting our callback into NVDA Remote during __init__,
		# because remoteClient doesn't show up in globalPlugins yet. We will do it in the script instead.
		#: Holds an initially empty reference to NVDA Remote
		self.remotePlugin = None
			
	def captureRemoteSpeech(self, *args, **kwargs):
		"""Register this as a callback to the NVDA Remote add-on's speech system, to obtain what it speaks."""
		if 'sequence' in kwargs:
			captureSpeech(kwargs.get('sequence'), Origin.REMOTE)
		return

	@script(
		category="Tools",
		description=_("Toggles logging of local and remote speech")
	)
	def script_speechLogToggle(self, gesture):
		"""Toggles whether we are actively logging, and sets up the remote portion if necessary."""
		if capturing:  # Stop
			capturing = False
			# Translators: message to tell the user that we are no longer logging.
			ui.message(_("Stopped logging speech."))
		else:  ## Start
			# Setup the initial message fragment
			if LOCAL_LOG is not NONE:
				# Translators: a message fragment telling the user that logging of local speech has begun, will be added to.
				message = _("Started logging local ")
			else:
				# Translators: a message fragment telling users that logging has started.
				message = _("Started logging ")
			# If this is the first time we're trying to start capturing,
			# we need to initialize the NVDA Remote portion of our log.
			if self.remotePlugin is None and self._obtainRemote():
				# We didn't have Remote before, but we do have it now. Configure the callback.
				self._setupRemoteCallback()
			# Add to the user message
			if self.remotePlugin is not None:
				# Translators: the word "and", a conjunction in case both kinds of speech are being logged.
				message += _("and ") if LOCAL_LOG is not None else ""
				# Translators: the word "remote", indicating remote speech.
				message += _("remote ")
			# Handles the case where no logging is ultimately possible.
			if LOCAL_LOG is None and (REMOTE_LOG is None or self.remotePlugin is None):
				# Translators: message to user when no log files configured, but user attempted logging
				ui.message(_("Can't start logging; no logs configured!"))
				capturing = False
			else:  # At least one log was configured above
				capturing = True
				# Translators: finish the message to the user.
				message += _("speech logging.")
				ui.message(message)

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

	def _setupRemoteCallback(self) -> None:
		# If we have a reference to the Remote plugin, register a handler for its speech:
		if self.remotePlugin is not None:
			remotePlugin.master_session.transport.callback_manager.register_callback('msg_speak', self.captureRemoteSpeech)

