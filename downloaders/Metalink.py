import bs4

from pahlib import Path

from .DownloadTarget import DownloadTarget


class Metalink:
	__slots__ = ("xml", "metalink")

	def initEmptyMetalink(self):
		self.xml = bs4.BeautifulSoup('<?xml version="1.0" encoding="utf-8"?>', "xml")
		self.metalink = bs4.Tag(name="metalink")
		self.metalink["xmlns"] = "urn:ietf:params:xml:ns:metalink"
		generator = bs4.Tag(name="generator")
		generator.append("downloaders python library")
		self.metalink.append("\n")
		self.metalink.append(generator)
		self.metalink.append("\n")
		self.xml.append(self.metalink)
		return self.xml

	def __init__(self, source: typing.Optional[typing.Union[str, Path, DownloadTarget]] = None) -> None:
		originalSource = source
		if originalSource is None:
			source = self.initEmptyMetalink()

		elif isinstance(originalSource, DownloadTarget):
			if originalSource.metalink:
				source = originalSource.metalink
			else:
				source = self.initEmptyMetalink()

		if isinstance(source, Path):
			source = originalSource.read_text()

		if isinstance(source, str):
			source = bs4.BeautifulSoup(source, "xml")

		if isinstance(source, bs4.BeautifulSoup):
			self.xml = source
			self.metalink = self.xml.select_one("metalink")

		if isinstance(originalSource, DownloadTarget):
			self.generateMetalinkFileNodeFromTarget(originalSource)

	def __iadd__(self, other):
		if isinstance(other, DownloadTarget):
			self.appendTarget(other)
		elif isinstance(other, self.__class__):
			self.appendFileNodesFromMetalink(other)
		else:
			raise NotImplementedError

		return self

	def appendTarget(self, target: DownloadTarget):
		if target.metalink:
			self.appendFileNodesFromMetalink(target.metalink)
		self.generateMetalinkFileNodeFromTarget(target)

	def appendFileNodesFromMetalink(self, metalink: "Metalink"):
		for f in next(metalink.xml.children).select("file"):
			self.metalink.append("\n")
			self.metalink.append(f)
			self.metalink.append("\n")

	def generateMetalinkFileNodeFromTarget(self, target):
		fileName = target.fsPath.name
		file = self.metalink.select_one("file", name=fileName)

		if file is None:
			file = bs4.Tag(name="file")
			file["name"] = target.fsPath.name
		self.metalink.append("\n")
		self.metalink.append(file)
		self.metalink.append("\n")

		for uri in target.uris:
			url = bs4.Tag(name="url")
			url.append(uri)
			file.append("\n")
			file.append(url)
		file.append("\n")
		return file

	def appendTargets(self, targets: typing.Iterable[DownloadTarget]):
		for target in targets:
			self.appendTarget(target)
		self.metalink.append("\n")

	def __str__(self):
		return str(self.xml)


def fixMetalink(meta4Text: str) -> "bs4.BeautifulSoup":
	"""This function is licensed under Unlicense license"""

	meta4XML = bs4.BeautifulSoup(meta4Text, "xml")
	fEl = meta4XML.select_one("file")
	urisEls = list(fEl.select("url"))
	for u in urisEls:
		u.string = fixHTTPS(u.string)
	if not fEl.select("metaurl[mediatype=torrent]"):
		t = bs4.Tag(name="metaurl")
		t.attrs["mediatype"] = "torrent"
		t.string = uris["torrent"]
		urisEls[0].insert_before(t)

	magnetUri = ourGet(uris["magnet"]).text.strip()

	t = bs4.Tag(name="url")
	t.attrs["priority"] = "0"
	t.string = magnetUri
	urisEls[0].insert_before(t)
	return meta4XML
