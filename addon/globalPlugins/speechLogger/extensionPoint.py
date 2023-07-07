# NVDA Speech Logger add-on: extensionPoint module for config changes
#
#    Copyright (C) 2023 Luke Davis <XLTechie@newanswertech.com>
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by    the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import extensionPoints

"""Provide a private extensionPoint for Speech Logger to use for
signaling when its config has changed and needs to be reloaded.
"""

_configChanged = extensionPoints.Action()
