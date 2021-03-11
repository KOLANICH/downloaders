downloaders.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
~~[wheel (GitLab)](https://gitlab.com/prebuilder/downloaders.py/-/jobs/artifacts/master/raw/dist/downloaders-0.CI-py3-none-any.whl?job=build)~~
[wheel (GHA via `nightly.link`)](https://nightly.link/prebuilder/downloaders.py/workflows/CI/master/downloaders-0.CI-py3-none-any.whl)
~~![GitLab Build Status](https://gitlab.com/KOLANICH/downloaders.py/badges/master/pipeline.svg)~~
~~![GitLab Coverage](https://gitlab.com/KOLANICH/downloaders.py/badges/master/coverage.svg)~~
[![Coveralls Coverage](https://img.shields.io/coveralls/prebuilder/downloaders.py.svg)](https://coveralls.io/r/prebuilder/downloaders.py)
[![GitHub Actions](https://github.com/prebuilder/downloaders.py/workflows/CI/badge.svg)](https://github.com/prebuilder/downloaders.py/actions/)
[![Libraries.io Status](https://img.shields.io/librariesio/github/prebuilder/downloaders.py.svg)](https://libraries.io/github/prebuilder/downloaders.py)

Just an abstraction layer around various backends for downloading content **more efficiently than `requests` can**. That assummes multi-stream downloading.

In scope - everything that would have a simple abstraction "URI -> file/dir":

* `https://`
* `.torrent`
* `magnet:`

Out of scope - everything that doesn't have such a simple abstraction (see [`fetchers`](https://github.com/prebuilder/fetchers.py) and maybe other libs mentioned there for them):

* have concept of a `version`:

	* package managers
	* VCSs/SCMs



Currently implemented backends:

* `aria2c` CLI tool.

# Tutorial

See [`./tutorial.ipynb`](./tutorial.ipynb) ([NBViewer](https://nbviewer.jupyter.org/github/prebuilder/downloaders.py/blob/master/tutorial.ipynb)).
