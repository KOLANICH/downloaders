import typing
from abc import abstractmethod, ABC
from pathlib import Path
import sys

from .backends.aria2c import Aria2Downloader
from .DownloadTarget import DownloadTarget

defaultDownloader = Aria2Downloader()
