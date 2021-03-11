import typing
from os import linesep
from pathlib import Path

import sh
from MempipedPath import MempipedPathRead

from fsutilz import relativePath

from ..DownloadTarget import DownloadTarget
from ..IDownloader import IDownloader


class Aria2Downloader(IDownloader):
	__slots__ = ("aria2c",)

	def __init__(self, aria2cPath: Path = "/usr/bin/aria2c", params: typing.Optional[dict] = None, fireJail=None):
		if params is None:
			params = {"continue": "true", "check-certificate": "true", "enable-mmap": "true", "optimize-concurrent-downloads": "true", "j": 16, "x": 16, "file-allocation": "falloc"}
		if fireJail is None:
			cmd = sh.Command(aria2cPath)  # no jail
		else:
			cmd = getattr(fireJail, aria2cPath)

		self.aria2c = cmd.bake(_fg=True, **params)

	def __call__(self, targets: typing.Iterable[DownloadTarget]) -> typing.Iterable[DownloadTarget]:
		if not targets:
			return
		args = []

		cwdP = Path(".").absolute()  # https://github.com/aria2/aria2/issues/1137

		needPassMetalink = False

		targets = sorted(targets, key=lambda t: not bool(t.metalink))
		needPassMetalink = bool(targets[0].metalink)

		if not needPassMetalink:
			for t in targets:
				uris = t.uris
				if not isinstance(uris, str):
					uris = "\t".join(uris)
				args += [uris, linesep]

				if t.fsPath:
					args += [" ", "out=", str(relativePath(t.fsPath, cwdP)), linesep]

			config = "".join(args)

			print(repr(config))

			with MempipedPathRead(config) as pipe:
				self.aria2c(**{"input-file": pipe})
		else:
			from ..Metalink import Metalink

			tIt = iter(targets)
			m = Metalink(next(tIt))

			for t in tIt:
				m += Metalink(t)

			with MempipedPathRead(str(m)) as pipe:
				self.aria2c(**{"metalink-file": pipe})


def download(downloadTargets: typing.Iterable[DownloadTarget]) -> typing.Iterable[DownloadTarget]:
	return Aria2Downloader()(downloadTargets)
