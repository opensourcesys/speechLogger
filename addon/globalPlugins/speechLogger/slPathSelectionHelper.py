import wx
from gui.dpiScalingHelper import scaleSize
from wx.lib.expando import ExpandoTextCtrl
from gui import guiHelper


class SLPathSelectionHelper(guiHelper.PathSelectionHelper):
	"""
	Abstracts away details for creating a path selection helper. The path selection helper is a textCtrl with a
	button in horizontal layout. The Button launches a directory explorer. To get the path selected by the user, use the
	`pathControl` property which exposes a wx.TextCtrl.
	"""

	def __init__(self, parent: wx.Dialog, buttonText: str, browseForDirectoryTitle: str) -> None:
		"""
		:param parent: An instance of the parent wx window. EG wx.Dialog
		:param buttonText: The text for the button to launch a directory dialog (wx.DirDialog). This is typically 'Browse'
		:param browseForDirectoryTitle: The text for the title of the directory dialog (wx.DirDialog)
		"""
		super().__init__(self)
		self._textCtrl = ExpandoTextCtrl(
			parent,
			size=(scaleSize(250), -1),
			style=wx.TE_READONLY,
		)
		self._browseButton = wx.Button(parent, label=buttonText)
		self._browseForDirectoryTitle = browseForDirectoryTitle
		self._browseButton.Bind(wx.EVT_BUTTON, self.onBrowseForDirectory)
		self._sizer = associateElements(self._textCtrl, self._browseButton)
