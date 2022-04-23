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
