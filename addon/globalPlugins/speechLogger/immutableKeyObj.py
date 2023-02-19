# immutableKeyObj, V1.0
#
#    Copyright (C) 2022-2023 Luke Davis <XLTechie@newanswertech.com>
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by    the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from typing import Any

class ImmutableKeyObj:
	"""Helper type which you initialize with kwargs that become its members, after which no new members can be added.
	Think of it as an implementation of __slots__, that works at the instance level.
	"""

	def __setattr__(self, key: str, val: Any) -> None:
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

	def __repr__(self) -> str:
		"""Returns the members of the instance as a formatted string."""
		itemSep = ", "  # A comma and a space between items
		kvSep = ": "  # A colon and a space between each key and value
		return itemSep.join(kvSep.join((k, str(v))) for (k, v) in self.__dict__.items())
