<!--
    =====================================
    generator=datazen
    version=3.1.3
    hash=d76a82c35bca3f5ae65a1edd4186d4af
    =====================================
-->

# conntextual ([0.2.0](https://pypi.org/project/conntextual/))

[![python](https://img.shields.io/pypi/pyversions/conntextual.svg)](https://pypi.org/project/conntextual/)
![Build Status](https://github.com/vkottler/conntextual/workflows/Python%20Package/badge.svg)
[![codecov](https://codecov.io/gh/vkottler/conntextual/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/github/vkottler/conntextual)
![PyPI - Status](https://img.shields.io/pypi/status/conntextual)
![Dependents (via libraries.io)](https://img.shields.io/librariesio/dependents/pypi/conntextual)

*A network-application TUI using textual.*

## Documentation

### Generated

* By [sphinx-apidoc](https://vkottler.github.io/python/sphinx/conntextual)
(What's [`sphinx-apidoc`](https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html)?)
* By [pydoc](https://vkottler.github.io/python/pydoc/conntextual.html)
(What's [`pydoc`](https://docs.python.org/3/library/pydoc.html)?)

## Python Version Support

This package is tested with the following Python minor versions:

* [`python3.11`](https://docs.python.org/3.11/)

## Platform Support

This package is tested on the following platforms:

* `ubuntu-latest`
* `macos-latest`

# Introduction

# Command-line Options

```
$ ./venv3.11/bin/conntextual -h

usage: conntextual [-h] [--version] [-v] [-C DIR] {ui,noop} ...

A network-application TUI using textual.

options:
  -h, --help         show this help message and exit
  --version          show program's version number and exit
  -v, --verbose      set to increase logging verbosity
  -C DIR, --dir DIR  execute from a specific directory

commands:
  {ui,noop}          set of available commands
    ui               run a user interface for runtimepy applications
    noop             command stub (does nothing)

```

# Internal Dependency Graph

A coarse view of the internal structure and scale of
`conntextual`'s source.
Generated using [pydeps](https://github.com/thebjorn/pydeps) (via
`mk python-deps`).

![conntextual's Dependency Graph](im/pydeps.svg)
