import typing
from pathlib import Path

from .utils.ReprMixin import ReprMixin

URIsT = typing.Union[str, typing.Iterable[str]]


class DownloadTarget(ReprMixin):
	__slots__ = ("uris", "metalink", "fsPath")

	def __init__(self, uris: URIsT, fsPath: typing.Optional[Path] = None, metalink: typing.Optional[typing.Union[str, Path]] = None) -> None:
		self.uris = uris
		self.fsPath = fsPath
		self.metalink = metalink
