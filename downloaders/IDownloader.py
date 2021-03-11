import typing
from abc import abstractmethod, ABC

from .DownloadTarget import DownloadTarget


class IDownloader(ABC):
	__slots__ = ()

	@abstractmethod
	def __call__(self, targets: typing.Iterable[DownloadTarget]) -> typing.Iterable[DownloadTarget]:
		raise NotImplementedError()
